# General model description

The model source: 

Reference  Dowsett, M., Sestak, I., Regan, M. M., Dodson, A., Viale, G.,
Thürlimann, B., ... & Cuzick, J. (2018). Integration of clinical variables for
the prediction of late distant recurrence in patients with estrogen
receptor–positive breast cancer treated with 5 years of endocrine therapy:
CTS5. Journal of Clinical Oncology, 36(19), 1941.
https://doi.org/10.1200/JCO.2017.76.4258

Outcome: 5 to 10 years distant recurrence (metastatic disease?)
The model calculates the 

Input data: Clinical Treatment Score post–5 years [CTS5] to estimate risk of late distant recurrence

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

# To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/dowsett_2018_metastatic_disease:latest

# To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 2,"Tumor_grade": "I", "Tumor_size": "5", "Age": 56}, {"N_positive_node": 9,"Tumor_grade": "III", "Tumor_size": "15", "Age": 78}]'

curl http://localhost:8000/result

The answer is [3.6242599999999996,6.37278]
