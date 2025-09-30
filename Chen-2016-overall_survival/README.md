# General model description

Reference: Chen, Y. C., Lai, H. W., Wang, W. C., & Kuo, Y. L. (2016). Validation of breast Cancer survival prediction model
with SEER database. J Integr Oncol, 5(3), 174.
https://doi.org/10.4172/2329-6771.1000174

Outcome - overall survival

Input variables for the model 
- Age
- Tumor grade (Bloom–Richardson system)
- Tumor size (based on pathological reports)
- Lymph node status
- Hormone Receptor status (estrogen receptor (ER) status, and progesterone receptor (PR) status; 1 for negative and 0 for positive)

# To run the Chen-2016-overall_survival_SEERmodel

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_seermodel:latest

## To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size_grade": "3", "Hormone_receptor": 0}'

curl http://localhost:8000/result

The answer is 0.6200121980391241



# To run the Chen-2016-overall_survival_NCKUHmodel

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/chen_2016_overall_survival_nckuhmodel:latest

## To predict: 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size_grade": "3", "Hormone_receptor": 0}'

curl http://localhost:8000/result

The answer is 0.4229194799630965


## To test for dictionary:

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size": "3", "Hormone_receptor": 0}, {"Age": 60.2, "Tumor_grade": "II", "Node_grade": "1", "Tumor_size": "2", "Hormone_receptor": 1}}]'

The answer is [0.4229194799630965, 0.058326614022680176]
