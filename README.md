# AVE-vs-DEKOIS

![Graphical-Abstract](https://github.com/vktrannguyen/AVE-vs-DEKOIS/blob/main/Graphical-Abstract.png)

You will find herein the files related to our JCIM viewpoint paper "**Beware of Simple Methods for Structure-Based Virtual Screening: The Critical Importance of Broader Comparisons**". 

Please cite: Tran-Nguyen, V. K.; Ballester, P. J. Beware of Simple Methods for Structure-Based Virtual Screening: The Critical Importance of Broader Comparisons. *J. Chem. Inf. Model.* **2023**, *63*, 1401-1405. https://doi.org/10.1021/acs.jcim.3c00218

Two targets namely **ACHE** (acetylcholinesterase) and **HMGR** (HMG-CoA reductase) are involved. Each target corresponds to a folder. Inside each folder, you will find the following sub-folders and files:

- **DEKOIS sub-folder**: training-test partition that employs a DEKOIS2.0 benchmark as test set, experimental data retrieved from PubChem/ChEMBL as training set. AVE split is not involved. Inside this sub-folder are the following files:
   - **Mol2** files with the word **docked** in their names: docked poses of training/test molecules inside their receptor
   - **Mol2** files with the word **protein** in their names: structure of the target used for docking
   - **CSV** files: information regarding all training/test molecules
   
- **AVE sub-folder**: training-test partition that does not employ any pre-existing public benchmark (such as DEKOIS2.0), but only contains experimental data retrieved from PubChem/ChEMBL and DeepCoy-generated decoys property-matched to PubChem/ChEMBL actives. This training-test partition was issued by AVE. Inside this sub-folder are the following files:
   - **Mol2** and **CSV** files: similarly to those in the **DEKOIS** sub-folder
   - **SMI** files: the input and output files of AVE
   - **TXT** file: information regarding the AVE split process
   
We also provide herein the script for carrying out AVE split (**Remove_AVE_Python3.py**). This script has been modified from the original version written by AVE authors (https://doi.org/10.1021/acs.jcim.7b00403) to be able to run in Python 3.

For more information, please contact **Dr. Viet-Khoa Tran-Nguyen** (khoatnv1993@gmail.com) or **Dr. Pedro J. Ballester** (p.ballester@imperial.ac.uk).
