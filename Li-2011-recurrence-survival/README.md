# General model description

The model source: 

Reference  Li, S., Yu, K. D., Fan, L., Hou, Y. F., & Shao, Z. M. (2011).
Predicting breast cancer recurrence following breast-conserving therapy:
a single-institution analysis consisting of 764 Chinese breast cancer
cases. Annals of surgical oncology, 18(9), 2492-2499.
https://doi.org/10.1245/s10434-011-1626-2

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

docker pull ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

docker run --rm -p 8000:8000 ghcr.io/maastrichtu-cds/breast_cancer_models/zhang_2017_lymph_node_clinical:latest

# To predict 

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '[{"N_positive_node": 3,"Tumor_grade": "II", "Molecular_subtype": "non-luminal"}, {"N_positive_node": 4,"Tumor_grade": "III", "Molecular_subtype": "non-luminal"}]'

curl http://localhost:8000/result

The answer is [0.19170025205726862,0.41994479935622686]
