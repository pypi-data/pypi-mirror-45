# UConnMLHI_UKBiobankProject


## Installation
### Installation via pip (Not done yet)
* For local installation
```
    $ pip install UConnMLHI_UKBiobankProject --user
```

* For global installation
```
    $ sudo pip install UConnMLHI_UKBiobankProject
```
### Manual Installation
```
    $ git clone https://github.com/xinyuwang1209/UConnMLHI_UKBiobankProject
    $ cd UConnMLHI_UKBiobankProject
```
* For local installation
```
    $ python setup.py install --user
```

* For global installation
```
    $ sudo python setup.py install
```


## Usage
### Load the module
```
    import UConnMLHI_UKBiobankProject as UKB
```

### Data_Process
#### dta2csv: convert dta file into csv format
* Set return_df = True, if you want to get the dataframe file beside saving it in csv
```    
    df = UKB.Data_Process.dta2csv('/path/to/file',return_df=True)
```

* Set return_df = False if you only want to save the data into csv format
```
    UKB.Data_Process.dta2csv('/path/to/file',return_df)
```

#### ICD_parser: Select Disease IDs from ICD9/ICD10 using keywords or nodes
* File 'coding87.tsv' is the hierarchical tree-structured dictionary for ICD9
  * https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=87&nl=1
* File 'coding19.tsv' is the hierarchical tree-structured dictionary for ICD10
  * https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=19&nl=1
* For example, to get all diseases in ICD10 with keyword 'alzheimer' plus all diseases in node 6 (the category of all the diseases of the nervous system):
```
    ICDs, keyword_dict, node_dict = UKB.Data_Process.ICD_parser('/path/to/coding19.tsv',keywords=['alzheimer'],nodes=[6])
```

#### select_healthy_subjects: Select healthy subject using disease IDs from ICD_parser
* For example, to get the subjects who does not have alzheimer or any other nervous system diseases:
```
import numpy as np
import pandas as pd
import UConnMLHI_UKBiobankProject as UKB

df = pd.read_csv('Data_Diagnosis.csv', low_memory=False)

icd = 10
ICDs, _,_ = UKB.Data_Process.ICD_parser('coding19.tsv',keywords=['alzheimer'],nodes=[6])
healthy_subjects, unhealthy_subjects = UKB.Data_Process.select_healthy_subjects(df,ICDs,icd=icd)
```
