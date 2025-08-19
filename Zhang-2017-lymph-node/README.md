# General model description

The model source: 

Outcome Zhang, J., Li, X., Huang, R., Feng, W. L.,
Kong, Y. N., Xu, F., ... & Wang, K. (2017). A nomogram
to predict the probability of axillary lymph node metastasis
in female patients with breast cancer in China: a nationwide,
multicenter, 10-year epidemiological study. Oncotarget, 8(21), 35311.


Outcome: axillary lymph node involvement

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


# To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

# To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Node_grade": 2,"Tumor_size": "3","Invasive_disease" : 1, "Topography": "UIQ", "Molecular_subtype": "LM", "Pathological_type": "ILC"}, {"Age": 60.1, "Node_grade": 1, "Tumor_size": "2", "Invasive_disease": 0, "Topography": "LIQ", "Molecular_subtype": "LA", "Pathological_type": "IDC"}]'

curl http://localhost:8000/result

The answer is [0.9544184859893631,0.4048251457671075]
