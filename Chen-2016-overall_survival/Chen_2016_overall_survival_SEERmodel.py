from math import exp
from model_execution import logistic_regression

class Chen_2016_overall_survival_SEERmodel(logistic_regression):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://www.omicsgroup.org/journals/validation-of-breast-cancer-survival-prediction-model-with-seer-database-2329-6771-1000174.php?aid=77460",
            "model_name": "Chen [2016] Breast cancer - Overall Survival Prediction Model for SEER data",
            "intercept": -6.115,
            "covariate_weights": {
                "Age": 0.031,
                "Tumor_grade_II": 0.549,
                "Tumor_grade_III": 1.162,
                "Tumor_grade_IV": 1.023,
                "Tumor_size_2": 0.765,
                "Tumor_size_3_4": 1.491,
                "Node_grade_1": 0.882,
                "Node_grade_2": 1.484,
                "Node_grade_3": 2.161,
                "Hormone_receptor": 1.054
            }
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables

            allowed_values = {
                "Hormone_receptor": ['0', '1'],  # 0 = positive, 1 = negative
                "Tumor_grade": ['I', 'II', 'III', 'IV'],
                "Node_grade": ['0', '1', '2', '3'],  # 0 = baseline, 1/2/3 = dummies
                "Tumor_size_grade": ['0', '1', '2', '3', '4']  # 0–1 = baseline group
            }

            # --- Hormone receptor ---
            if "Hormone_receptor" not in entry:
                raise ValueError("Missing Hormone_receptor")
            if str(entry["Hormone_receptor"]) not in allowed_values["Hormone_receptor"]:
                raise ValueError(f"Invalid Hormone_receptor value: {entry['Hormone_receptor']}")

            entry["Hormone_receptor"] = 1.0 if str(entry["Hormone_receptor"]) == '0' else 0.0 # 0=positive, 1=negative

            # --- Tumor grade ---
            if "Tumor_grade" not in entry:
                raise ValueError("Missing Tumor_grade")
            if entry["Tumor_grade"] not in allowed_values["Tumor_grade"]:
                raise ValueError(f"Invalid Tumor_grade value: {entry['Tumor_grade']}")

            entry["Tumor_grade_II"] = 1.0 if entry["Tumor_grade"] == 'II' else 0.0
            entry["Tumor_grade_III"] = 1.0 if entry["Tumor_grade"] == 'III' else 0.0
            entry["Tumor_grade_IV"] = 1.0 if entry["Tumor_grade"] == 'IV' else 0.0

            # --- Node grade ---
            if "Node_grade" not in entry:
                raise ValueError("Missing Node_grade")
            if str(entry["Node_grade"]) not in allowed_values["Node_grade"]:
                raise ValueError(f"Invalid Node_grade value: {entry['Node_grade']}")

            entry["Node_grade_1"] = 1.0 if str(entry["Node_grade"]) == '1' else 0.0
            entry["Node_grade_2"] = 1.0 if str(entry["Node_grade"]) == '2' else 0.0
            entry["Node_grade_3"] = 1.0 if str(entry["Node_grade"]) == '3' else 0.0

            # --- Tumor size ---
            if "Tumor_size_grade" not in entry:
                raise ValueError("Missing Tumor_size_grade")
            if str(entry["Tumor_size_grade"]) not in allowed_values["Tumor_size_grade"]:
                raise ValueError(f"Invalid Tumor_size_grade value: {entry['Tumor_size_grade']}")

            entry["Tumor_size_2"] = 1.0 if str(entry["Tumor_size_grade"]) == '2' else 0.0
            entry["Tumor_size_3_4"] = 1.0 if str(entry["Tumor_size_grade"]) in ('3', '4') else 0.0

            # Dose values expected as floats (gray units)
            entry['Age'] = float(entry['Age'])
            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = Chen_2016_overall_survival_SEERmodel()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "Age": 45.6,
            "Tumor_grade": "III",
            "Node_grade": "2",
            "Tumor_size_grade": "3",
            "Hormone_receptor": '0'
        }
    ))