#
# Copyright 2017 Atomwise Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
from random import shuffle
import os
import random
from multiprocessing import Pool
import argparse

import numpy as np
from scipy.spatial.distance import cdist, is_valid_dm
from sklearn.metrics import roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from scipy import stats
from sklearn import svm
from sklearn import neighbors, datasets

from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem.rdMolDescriptors import GetHashedAtomPairFingerprint,GetHashedAtomPairFingerprintAsBitVect
from rdkit.Chem import AllChem
from rdkit import Chem
from rdkit import DataStructs

def readMols( file ) :
  fileName, fileExtension = os.path.splitext( file )
  mols = []
  if( fileExtension == ".smi" ) :
    f = open( file, 'r' )
    l = f.readline()
    f.close()
    if '\t' in l :
      mols = Chem.SmilesMolSupplier( file, delimiter='\t', titleLine=False )
    else :
      mols = Chem.SmilesMolSupplier( file, delimiter=' ', titleLine=False ) 
  elif( fileExtension == ".sdf" ) : 
    mols = Chem.SDMolSupplier( file )
  else: 
    raise Exception( "un-supported input file format: "+fileExtension + " . ")
  return mols


def get_fp( mols ):
  fps=[]
  if( args.fpType == 'ECFP4' ) : 
    for x in  mols :
      if( x ):
        z=AllChem.GetMorganFingerprintAsBitVect( x, 2 )
        fps.append(z)
  if( args.fpType == 'ECFP6' ) : 
    for x in  mols :
      if( x ):
        z=AllChem.GetMorganFingerprintAsBitVect( x, 3 ) 
        fps.append(z)
  if( args.fpType == 'ECFP12' ) : 
    for x in  mols :
      if( x ):
        z=AllChem.GetMorganFingerprintAsBitVect( x, 6 )
        fps.append(z)
  if( args.fpType == 'MACCS' ) : 
    for x in  mols :
      if( x ):
        z = Chem.MACCSkeys.GenMACCSKeys( x )
        fps.append(z)
  if( args.fpType == 'Daylight' ) :
    for x in  mols :
      if( x ) :
        z = FingerprintMols.FingerprintMol( x )
        fps.append(z)
  if (args.fpType == 'AP'):
    for x in mols:
      if (x):
        z=GetHashedAtomPairFingerprintAsBitVect( x, nBits=4096 )
        fps.append(z)
  return fps


def gen_eval( train_data, train_labels, test_data, test_labels, method="knn1"):
  probs=None
  if method[:3]=="knn":
    k=int(method[3:])
    classifier = neighbors.KNeighborsClassifier( k, metric=args.metric, algorithm='brute' )
    classifier.fit( train_data, train_labels )
    probs = classifier.predict_proba( test_data )[:,1]
  elif method=="lr":
    classifier = LogisticRegression()
    classifier.fit( train_data, train_labels )
    probs = classifier.predict_proba( test_data )[:,1]
  elif method=="rf":
    classifier = RandomForestClassifier( n_estimators=100 )
    classifier.fit( train_data,train_labels )
    probs = classifier.predict_proba( test_data )[:,1]
  elif method=="svm" :
    classifier = svm.SVC( probability=True )
    classifier.fit( train_data, train_labels )
    probs = classifier.predict_proba( test_data )[:,1]
  
  fpr, tpr, thresholds = roc_curve( test_labels, probs )
  roc_auc = auc(fpr, tpr)
  return roc_auc

def Cdist( params ) :
  return cdist( params[0], params[1], params[2] ) 

def calcDistMat( fp1, fp2, distType ) :
  if( args.numWorkers > 1 ) :
    interval, reminder = divmod( len(fp1), min( len(fp1), args.numWorkers-1 ) )
    interval = max( interval, 1 )
    chuncks = pool.map( Cdist, [ (fp1[r:min(r+interval, len(fp1) ) ], fp2, distType) for r in range( 0, len(fp1), interval ) ] ) 
    return np.vstack( chuncks ) 
  else :
    return cdist( fp1, fp2, distType )



parser = argparse.ArgumentParser( description='' )
parser.add_argument( '-fpType', default="ECFP4", choices=['DayLight', 'ECFP4', 'ECFP6', 'ECFP12', 'AP','MACCS' ] )
parser.add_argument( '-activeMolsTraining' , required=True )
parser.add_argument( '-inactiveMolsTraining' , required=True )
parser.add_argument( '-activeMolsTesting' , required=True )
parser.add_argument( '-inactiveMolsTesting' , required=True )
parser.add_argument( '-outFile' , required=True )
parser.add_argument( '-metric', type=str, default='jaccard', choices=['jaccard','dice','euclidean'] )
parser.add_argument( '-numWorkers', default=1, type=int )
args = parser.parse_args()

pool = None
if( args.numWorkers > 1 ) :
  print("init",args.numWorkers,"workers")
  pool = Pool( processes = args.numWorkers )

activesTrain = [ m for m in readMols( args.activeMolsTraining ) if m is not None ]
inactivesTrain = [ m for m in readMols( args.inactiveMolsTraining ) if m is not None ]
activesTest = [ m for m in readMols( args.activeMolsTesting ) if m is not None ]
inactivesTest = [ m for m in readMols( args.inactiveMolsTesting ) if m is not None ]

activesTrainFP = get_fp( activesTrain ) 
inactivesTrainFP = get_fp( inactivesTrain ) 
activesTestFP = get_fp( activesTest )
inactivesTestFP = get_fp( inactivesTest )

train_data = activesTrainFP + inactivesTrainFP 
train_labels = [1]*len( activesTrainFP ) + [0]*len( inactivesTrainFP )
test_data = activesTestFP + inactivesTestFP 
test_labels = [1]*len( activesTestFP ) + [0]*len( inactivesTestFP )

combT = list(zip( train_data, train_labels ))
combV = list(zip( test_data, test_labels ))
shuffle( combT )
shuffle( combV )
train_data, train_labels = zip( *combT )
test_data, test_labels = zip( *combV )

aTest_aTrain_D = calcDistMat( activesTestFP, activesTrainFP, args.metric )
aTest_iTrain_D = calcDistMat( activesTestFP, inactivesTrainFP, args.metric )
iTest_iTrain_D = calcDistMat( inactivesTestFP, inactivesTrainFP, args.metric )
iTest_aTrain_D = calcDistMat( inactivesTestFP, activesTrainFP, args.metric )

aTest_aTrain_S = np.mean( [ np.mean( np.any( aTest_aTrain_D < t, axis=1 ) ) for t in np.linspace( 0, 1.0, 50 ) ] )
aTest_iTrain_S = np.mean( [ np.mean( np.any( aTest_iTrain_D < t, axis=1 ) ) for t in np.linspace( 0, 1.0, 50 ) ] )
iTest_iTrain_S = np.mean( [ np.mean( np.any( iTest_iTrain_D < t, axis=1 ) ) for t in np.linspace( 0, 1.0, 50 ) ] )
iTest_aTrain_S = np.mean( [ np.mean( np.any( iTest_aTrain_D < t, axis=1 ) ) for t in np.linspace( 0, 1.0, 50 ) ] )

outFH = open( args.outFile, 'w' )
print (outFH, "#ActTrain=",len( activesTrainFP ), "#InactTrain=",len( inactivesTrainFP ),\
    "#ActTest=",len( activesTestFP ), "#InactTest=", len( inactivesTestFP ),\
    "knn1=", gen_eval( train_data, train_labels, test_data, test_labels, "knn1" ),\
    "lr=", gen_eval( train_data, train_labels, test_data, test_labels, "lr" ),\
    "rf=", gen_eval( train_data, train_labels, test_data, test_labels, "rf" ),\
    "svm=", gen_eval( train_data, train_labels, test_data, test_labels, "svm" ),\
    "AA",aTest_aTrain_S,\
    "II",iTest_iTrain_S,\
    "AA-AI=",aTest_aTrain_S-aTest_iTrain_S,\
    "II-IA=",iTest_iTrain_S-iTest_aTrain_S,\
    "(AA-AI)+(II-IA)=",aTest_aTrain_S-aTest_iTrain_S+iTest_iTrain_S-iTest_aTrain_S)
outFH.close()

