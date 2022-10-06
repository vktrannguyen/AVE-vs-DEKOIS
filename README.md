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
   
For more information, please contact **Dr. Viet-Khoa Tran-Nguyen** (khoatnv1993@gmail.com) or **Dr. Pedro J. Ballester** (p.ballester@imperial.ac.uk).
