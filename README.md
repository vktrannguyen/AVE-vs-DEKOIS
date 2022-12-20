# AVE-vs-DEKOIS

You will find herein the files related to our JCIM short communication paper "**The Impact of AVE Split on Virtual Screening Performance**". Two targets namely **ACHE** (acetylcholinesterase) and **HMGR** (HMG-CoA reductase) are involved. Each target corresponds to a folder. Inside each folder, you will find the following sub-folders and files:

- **DEKOIS sub-folder**: training-test partition that employs a DEKOIS2.0 benchmark as test set, experimental data retrieved from PubChem/ChEMBL as training set. AVE split is not involved. Inside this sub-folder are the following files:
   - **Mol2** files with the word **docked** in their names: docked poses of training/test molecules inside their receptor
   - **Mol2** files with the word **protein** in their names: structure of the target used for docking
   - **CSV** files: information regarding all training/test molecules
   
- **AVE sub-folder**: training-test partition that does not employ any pre-existing public benchmark (such as DEKOIS2.0), but only contains experimental data retrieved from PubChem/ChEMBL and DeepCoy-generated decoys property-matched to PubChem/ChEMBL actives. This training-test partition was issued by AVE. Inside this sub-folder are the following files:
   - **Mol2** and **CSV** files: similarly to those in the **DEKOIS** sub-folder
   - **SMI** files: the input and output files of AVE
   - **TXT** file: information regarding the AVE split process
   
- **DEKOIS-AVE sub-folder**: training-test partition issued by the AVE script from the combined training and test data of the corresponding **DEKOIS sub-folder**, such that the training-to-test ratio of the new split is approximately that of ACHE-DEKOIS2.0 (365/1240) and HMGR-DEKOIS2.0 (1036/1240). Inside this sub-folder are **Mol2**, **CSV**, **SMI** and **TXT** files with the same descriptions as those provided for the above **AVE sub-folder**.
   
We also provide herein the two AVE scripts originally written by AVE authors (https://doi.org/10.1021/acs.jcim.7b00403), one for carrying out AVE split (**Remove_AVE_Python3.py**), one for computing the AVE bias of any training-test partition (**Analyze_AVE_Python3.py**). These scripts have been modified from the original scripts to be able to run in Python 3.

For more information, please contact **Dr. Viet-Khoa Tran-Nguyen** (khoatnv1993@gmail.com) or **Dr. Pedro J. Ballester** (p.ballester@imperial.ac.uk).
