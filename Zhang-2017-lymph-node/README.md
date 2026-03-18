# General model description

The model source: 

Outcome Zhang, J., Li, X., Huang, R., Feng, W. L.,
Kong, Y. N., Xu, F., ... & Wang, K. (2017). A nomogram
to predict the probability of axillary lymph node metastasis
in female patients with breast cancer in China: a nationwide,
multicenter, 10-year epidemiological study. Oncotarget, 8(21), 35311.

Model metadata: https://v3.fairmodels.org/instance/23808ad3-6ab4-4af2-9f78-88e7d56a70a2

Outcome: axillary lymph node involvement

## Original model

Input data:

- age at the diagnosis
- topography 
  - Upper inner quadrant - 'UIQ'
  - upper outer quadrant - 'UOQ'
  - lower inner quadrant - 'LIQ'
  - lower outer quadrant - 'LOQ'
  - other
- Invasive disease
  - no - 0
  - yes - 1
- Node status 
  - no - 0
  - yes - 1
- Tumor size
  - T2 - 2
  - T3 - 3
- Pathological type
  - invasive ductal carcinoma - 'IDC'
  - invasive lobular carcinoma - 'ILC'
  - other 
- Molecular subtype
  - luminal-like - 'LM'
  - human epidermal growth factor receptor-2 - 'HER2'


### To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

### To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Node_grade": 2,"Tumor_size": "3","Invasive_disease" : 1, "Topography": "UIQ", "Molecular_subtype": "LM", "Pathological_type": "ILC"}, {"Age": 60.1, "Node_grade": 1, "Tumor_size": "2", "Invasive_disease": 0, "Topography": "LIQ", "Molecular_subtype": "LM", "Pathological_type": "IDC"}]'

curl http://localhost:8000/result

The answer is [0.9544184859893631,0.4048251457671075]

## The modification of the model

Input data:

- age at the diagnosis
- topography (tumor location)
  - Upper inner quadrant - 'UIQ'
  - upper outer quadrant - 'UOQ'
  - lower inner quadrant - 'LIQ'
  - lower outer quadrant - 'LOQ'
  - other
- Invasive disease
  - no - 0
  - yes - 1
- Node_clin_grade
  - Grade I - 'I' or 1 or '1'
  - Grade II - 'II' or 2 or '2'
  - Grade III - 'III' or 3 or '3'
  - Garde 0 - '0' or 0
- Tumor clinical grade (Clinical tumor size grade assessment by preoperative ultrasound)
  - T0 - 0 or '0'
  - T1 - 1 or 'I' or '1'
  - T2 - 2 or 'II' or '2'
  - T3 - 3 or 'III' or '3'
- Pathological type
  - invasive ductal carcinoma - 'IDC'
  - invasive lobular carcinoma - 'ILC'
  - other 
- Estrogen receptor
  - positive -1
  - negative -0
- Progesterone receptor
  - positive -1
  - negative -0
- HER2/neu status
  - positive -1
  - negative -0

Luminal-A =1 if ER and PR are positive (1) and HER2/neu is negative (0)


### To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical_mod:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical_mod:latest

### To predict 

curl -X POST http://localhost:8000/clin_grade": 3,"Tumor_clin_grade": "2","Invasive_disease" : 1, "Topography": "UIQ", "ER": 0, "PR":1,"HER2":0, "Pathological_type": "ILC"}, {"Age": 60.1, "Node_clin_grade": 3, "Tumor_clin_grade": "2", "Invasive_disease": 0, "Topography": "LIQ", "ER": 0, "PR":0,"HER2":1, "Pathological_type": "IDC"}]'
curl http://localhost:8000/result

The answer is {"prediction_0":0.7937369805848541,"prediction_1":0.4392023264658952}(
