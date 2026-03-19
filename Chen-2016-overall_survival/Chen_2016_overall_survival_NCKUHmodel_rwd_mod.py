from typing import Tuple, Any, Dict, List, Optional
from model_execution import logistic_regression

def validate_categorical_num_feature(data: Any, feature: str, categories) -> bool:
    if feature not in data:
        raise ValueError(f"Missing {feature}")
    try:
        data[feature] = int(data[feature])
    except (TypeError, ValueError):
        raise TypeError(f"Input variable {feature} must be a number")

    if data[feature] not in categories[feature]:
        raise ValueError(f"Input feature {feature} value is not allowed: {data[feature]}")
    return True

class Chen_2016_overall_survival_NCKUHmodel_rwd_mod(logistic_regression):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://www.omicsgroup.org/journals/validation-of-breast-cancer-survival-prediction-model-with-seer-database-2329-6771-1000174.php?aid=77460",
            "model_name": "Chen [2016] Breast cancer - Overall Survival Prediction Model for NCKUH data",
            "intercept": -4.725,
            "covariate_weights": {
                "Age": -0.003,
                "Tumor_grade_II": 0.975,
                "Tumor_grade_III": 1.440,
                "Tumor_grade_IV": 0,
                "Tumor_size_2": 0.228,
                "Tumor_size_3_4": 0.853,
                "Node_grade_1": 0.921,
                "Node_grade_2": 1.257,
                "Node_grade_3": 1.882,
                "Hormone_receptor": 1.001
            }
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables
            # Map raw clinical inputs to the dummy variables used in the Chen 2016 SEER model.
            # Logic follows the original R code:
            #
            #         LP = -6.115
            #              + 0.031 * Age
            #              + 0.549 * I(Diffgr == 2)
            #              + 1.162 * I(Diffgr == 3)
            #              + 1.023 * I(Diffgr == 4)
            #              + 0.765 * I(pt in {2, 2A, 2B})
            #              + 1.491 * I(pt in {3, 4, 4A, 4B, 4C, 4D})
            #              + 0.882 * I(pn in {1, 1M, 1B, 1BS, 1C, 1CS, 1M, 1MS})
            #              + 1.484 * I(pn in {2, 2A, 2B})
            #              + 2.161 * I(pn in {3, 3A, 3B, 3C})
            #              + 1.054 * I(HR == 1)

            allowed_values = {
                "ER": [0, 1],  # 0 = negative, 1 = positive
                "PR": [0, 1],  # 0 = negative, 1 = positive
                "Tumor_grade": [1, 2, 3, 4],
                "Node_hist_grade": ['0', '1', '1M', '2', '2A', '2B', '3', '3A', '3B', '3C'],  # 0 = baseline, 1/2/3 = dummies
                "Tumor_hist_grade": ['0', '1', '2', '2A', '2B', '3', '4', '4A', '4B', '4C', '4D']
                # 0–1 = baseline group
            }

            # --- Hormone receptor ---
            feature = "Hormone_receptor"
            # --- ER, PR, HER2 ---
            for marker in ["ER", "PR"]:
                validate_categorical_num_feature(entry, marker, allowed_values)

            entry[feature] = 1.0 if (
                        (entry["ER"] == 1 or entry["PR"] == 1)) else 0.0

            # if feature not in entry:
            #     raise ValueError(f"Missing {feature}")
            # try:
            #     entry[feature] = str(entry[feature])
            # except (TypeError, ValueError):
            #     raise TypeError(f"Input variable {feature} must be a string")
            #
            # if entry[feature] not in allowed_values[feature]:
            #     raise ValueError(f"Invalid {feature} value: {entry[feature]}")
            #
            # entry[feature] = 1.0 if entry[feature] == '1' else 0.0  # 1=positive, 0=negative

            # --- Tumor grade ---
            feature = "Tumor_grade"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            entry[feature] = str(entry[feature])
            if entry[feature] == 'I':
                entry[feature] = '1'
            elif entry[feature] == 'II':
                entry[feature] = '2'
            elif entry[feature] == 'III':
                entry[feature] = '3'
            elif entry[feature] == 'IV':
                entry[feature] = '4'

            # validate values against the allowed list
            validate_categorical_num_feature(entry, feature, allowed_values)

            entry["Tumor_grade_II"] = 1.0 if entry[feature] == 2 else 0.0
            entry["Tumor_grade_III"] = 1.0 if entry[feature] == 3 else 0.0
            entry["Tumor_grade_IV"] = 1.0 if entry[feature] == 4 else 0.0

            # --- Node grade ---
            feature = "Node_hist_grade"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            entry[feature] = str(entry[feature])
            if entry[feature] not in allowed_values[feature]:
                raise ValueError(f"Invalid {feature} value: {entry[feature]}")

            entry["Node_grade_1"] = 1.0 if entry[feature] in ('1', '1M') else 0.0
            entry["Node_grade_2"] = 1.0 if entry[feature] in ('2', '2A', '2B') else 0.0
            entry["Node_grade_3"] = 1.0 if entry[feature] in ('3', '3A', '3B', '3C') else 0.0

            # --- Tumor size ---
            feature = "Tumor_hist_grade"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            entry[feature] = str(entry[feature])
            if entry[feature] not in allowed_values[feature]:
                raise ValueError(f"Invalid {feature} value: {entry[feature]}")

            entry["Tumor_size_2"] = 1.0 if entry[feature] in ('2', '2A', '2B') else 0.0
            entry["Tumor_size_3_4"] = 1.0 if entry[feature] in ('3', '4', '4A', '4B', '4C', '4D') else 0.0

            # Age values expected as floats (years)
            entry['Age'] = float(entry['Age'])
            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = Chen_2016_overall_survival_NCKUHmodel_rwd_mod()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        [{'Age': 78, 'Tumor_grade': 'II', 'Tumor_hist_grade': 2, 'Node_hist_grade': '2A', 'ER': '0', 'PR':'1'},
         {'Age': 98, 'Tumor_grade': 'II', 'Tumor_hist_grade': 3, 'Node_hist_grade': 3, 'ER': '1', 'PR':'1'}]
    ))