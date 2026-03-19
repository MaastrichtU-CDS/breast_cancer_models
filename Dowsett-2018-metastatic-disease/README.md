# General model description

The model source: 

Reference  Dowsett, M., Sestak, I., Regan, M. M., Dodson, A., Viale, G.,
Thürlimann, B., ... & Cuzick, J. (2018). Integration of clinical variables for
the prediction of late distant recurrence in patients with estrogen
receptor–positive breast cancer treated with 5 years of endocrine therapy:
CTS5. Journal of Clinical Oncology, 36(19), 1941.
https://doi.org/10.1200/JCO.2017.76.4258

Model metadata: https://v3.fairmodels.org/instance/05568731-ee03-4642-8cf6-bae9d25ab4d1

Outcome: 5 to 10 years distant recurrence (metastatic disease?)
The model calculates the Clinical Treatment Score post–5 years [CTS5] to estimate risk of late distant recurrence

## Original model
Input data:
- Number of positive nodes
  - negative - 0
  - one positive - 1
  - 2-3 positive - 2
  - 4-9 positive - 3
  - n>9 positive - 4
- Tumor grade
  - TI - 1
  - TII - 2
  - TIII - 3
- Tumor size (in millimeters)
- Age (at start of endocrine therapy, years)

### To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease:latest

### To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 2,"Tumor_grade": "I", "Tumor_size": "5", "Age": 56}, {"N_positive_node": 9,"Tumor_grade": "III", "Tumor_size": "15", "Age": 78}]'

curl http://localhost:8000/result

The answer is [2.621796, 4.891548]

## Modification of the model
Input data:
- Number of positive nodes - an integer number >0
- Tumor grade
  - Low grade I (well differentiated) - 1 or 'I' or '1'
  - Intermediate grade II (Moderately differentiated) - 2 or 'II' or '2'
  - High grade III (Poorly differentiated) - 3 or 'III' or '3'
  - For same cases undifferentiated / anaplastic (high grade) - IV - 4 or 'IV' or '4' (model uses like Grade III)
- Tumor size (in millimeters, no more than 100 mm)
- Age (at start of endocrine therapy, years)

### To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease_rwd_mod:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease_rwd_mod:latest

### To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 2,"Tumor_grade": "I", "Tumor_size": "5", "Age": 56}, {"N_positive_node": 9,"Tumor_grade": "III", "Tumor_size": "15", "Age": 78}]'

curl http://localhost:8000/result

The answer is {"prediction_0":2.621796,"prediction_1":4.891548}

