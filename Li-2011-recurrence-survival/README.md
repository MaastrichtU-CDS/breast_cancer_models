# General model description

The model source: 

Reference  Li, S., Yu, K. D., Fan, L., Hou, Y. F., & Shao, Z. M. (2011).
Predicting breast cancer recurrence following breast-conserving therapy:
a single-institution analysis consisting of 764 Chinese breast cancer
cases. Annals of surgical oncology, 18(9), 2492-2499.
https://doi.org/10.1245/s10434-011-1626-2

Model metadata: https://v3.fairmodels.org/instance/cf34c0e8-bd56-4ff8-a205-56253be44a74

Outcome: 5-year recurrence survival

Input data:

- Number of positive nodes 
  - n=0 - 0
  - n=1-3 - 1
  - n>=4 - 2
- Tumor grade
  - TI - 1
  - TII - 2
  - TIII - 3
- Molecular subtype
  - 'Luminal-A' - 1
  - others - 0

# To run the model

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/li_2011_recurrence_survival:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/li_2011_recurrence_survival:latest

# To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 3,"Tumor_grade": "II", "Molecular_subtype": "non-luminal"}, {"N_positive_node": 4,"Tumor_grade": "III", "Molecular_subtype": "non-luminal"}]'

curl http://localhost:8000/result

The answer is [0.19170025205726862,0.41994479935622686]


For the modification version of the model:

- Number of positive nodes 
  - integer number > 0
- Tumor grade
  - low Grade I - 1 or 'I' or '1'
  - intermediate Grade II - 2 or 'II' or '2'
  - high Grade III - 3 or 'III' or '3'
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

# To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 3, "Tumor_grade": 2, "ER": "0", "PR": 0, "HER2":0},{"N_positive_node": 4,"Tumor_grade": "III", "ER":0, "PR":0,"HER2":1}]

curl http://localhost:8000/result

{"prediction_0":0.19170025205726862,"prediction_1":0.41994479935622686}


