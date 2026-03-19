# General model description

Reference: Chen, Y. C., Lai, H. W., Wang, W. C., & Kuo, Y. L. (2016). Validation of breast Cancer survival prediction model
with SEER database. J Integr Oncol, 5(3), 174.
https://doi.org/10.4172/2329-6771.1000174

Outcome - overall survival

## Original models
Input variables for the model 
- Age
- Tumor grade (Bloom–Richardson system)
- Tumor size (based on pathological reports)
- Lymph node status
- Hormone Receptor status (estrogen receptor (ER) status, and progesterone receptor (PR) status; 1 for negative and 0 for positive)

### To run the Chen-2016-overall_survival_SEERmodel

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel:latest

### To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size_grade": "3", "Hormone_receptor": 0}'

curl http://localhost:8000/result

The answer is 0.6200121980391241


### To run the Chen-2016-overall_survival_NCKUHmodel

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_nckuhmodel:latest

### To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size_grade": "3", "Hormone_receptor": 0}'

curl http://localhost:8000/result

The answer is 0.4229194799630965


### To test for dictionary:

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size": "3", "Hormone_receptor": 0}, {"Age": 60.2, "Tumor_grade": "II", "Node_grade": "1", "Tumor_size": "2", "Hormone_receptor": 1}}]'

The answer is [0.4229194799630965, 0.058326614022680176]

## Modification of the model

Input variables for the model 
- Age 
- Tumor grade (Bloom–Richardson system)
  - Grade I - 1 or 'I' or '1'
  - Grade II - 2 or 'II' or '2'
  - Grade III - 3 or 'III' or '3'
  - Grade IV - 4 or 'IV' or '4'
- Tumor size (based on pathological reports)
  - Grade 1 - 1 
  - Grade 2 - '2', '2A', '2B'
  - Grade 3 - '3'
  - Grade 4 - '4', '4A', '4B', '4C', '4D'
- Lymph node grade (based on pathological reports)
  - Grade 1 - '1', '1M', '1A', '1AS', '1B', '1BS', '1C', '1CS','1MS'
  - Grade 2 - '2', '2A', '2AS', '2B'
  - Grade 3 - '3', '3A', '3B', '3C'
- Hormone Receptor status is derived from estrogen receptor (ER) status, and progesterone receptor (PR) status
  for ER and PR:
  - negative - 0 
  - positive - 1


### To run the Chen-2016-overall_survival_SEERmodel_mod

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel_mod:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel_mod:latest
### To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Tumor_grade": "II", "Tumor_hist_grade":3, "Node_hist_grade":3,"ER":"1","PR":"1"},{"Age": 98, "Tumor_grade": "II", "Tumor_hist_grade":3, "Node_hist_grade":3,"ER":"0","PR":"0"}]'
curl http://localhost:8000/result

The answer is {"prediction_0":0.37744667191883613,"prediction_1":0.8982564340112952}

### To run the Chen-2016-overall_survival_NCKUHmodel

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_nckuhmodel_mod:latest

### To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Tumor_grade": "II", "Tumor_hist_grade":3, "Node_hist_grade":3,"ER":"1","PR":"1"},{"Age": 98, "Tumor_grade": "II", "Tumor_hist_grade":3, "Node_hist_grade":3,"ER":"0","PR":"0"}]'
curl http://localhost:8000/result

The answer is {"prediction_0":0.24016045929505975,"prediction_1":0.4236029910972445}