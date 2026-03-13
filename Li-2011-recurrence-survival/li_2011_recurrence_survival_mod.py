from math import exp
from model_execution import logistic_regression
from typing import Tuple, Any, Dict, List, Optional

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

class li_2011_recurrence_survival_mod(logistic_regression):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://doi.org/10.1245/s10434-011-1626-2",
            "model_name": "Li [2011] Breast cancer - Evaluate recurrence risk of a woman treated with breast-conserving therapy in Chinese population",
            "intercept": -3.124,
            "covariate_weights": {
                "Tumor_grade": 0.569,
                "N_positive_node_cat": 0.547,
                "Molecular_subtype": -1.034,
            }
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables
            allowed_values = {
                "Tumor_grade": [1, 2, 3, 4],
                "ER": [0,1],  # 0 = negative, 1 = positive
                "PR": [0,1],  # 0 = negative, 1 = positive
                "HER2": [0,1]  # 0 = negative, 1 = positive
            }
            # For N_positive_node, tumor grade, nd molecular subtype
            # ensure the right coding!!!
            # entry["N_positive_node_cat"] = 0 if entry["N_positive_node"] == 0 else (1 if entry["N_positive_node"] <= 3 else 2)
            # entry["Tumor_grade"] = 1.0 if entry["Tumor_grade"] == 'I' else (2.0 if entry["Tumor_grade"] == 'II' else 3.0)
            # entry["Molecular_subtype"] = 1.0 if ((entry["ER"] == 1 or entry["PR"] == 1) and entry["HER2"] ==0) else 0.0 # luminal-like

            # --- N_positive_node ---
            feature="N_positive_node"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            try:
                entry[feature] = int(entry[feature])
            except ValueError:
                raise ValueError(f"{feature} must be an integer number, got {entry[feature]}")
            # if n < 0 or n > 50:  # adjustable upper bound
            #     raise ValueError(f"N_positive_node out of allowed range (0–50), got {n}")

            entry["N_positive_node_cat"] = 0 if entry[feature] == 0 else (1 if entry[feature] <= 3 else 2)

            # --- Tumor_grade ---
            # By the model:
            # - grade (three groups: I: 1; II: 2; III: 3)
            # By https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade:
            # Grade I - Well differentiated (low grade)
            # Grade II 	- Moderately differentiated (intermediate grade)
            # Grade III - Poorly differentiated (high grade)
            # Grade IV - undifferentiated / anaplastic (high grade)
            # diffgrtxt	9	Differentiatiegraad  onbekend / n.v.t.
            feature="Tumor_grade"
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

            validate_categorical_num_feature(entry, feature, allowed_values)

            # --- ER, PR, HER2 ---
            for marker in ["ER", "PR", "HER2"]:
                if marker not in entry:
                    raise ValueError(f"Missing {marker}")
                if str(entry[marker]) not in allowed_values[marker]:
                    raise ValueError(f"Invalid {marker} value: {entry[marker]}")
                entry[marker] = int(entry[marker])

            # --- Molecular subtype ---
            entry["Molecular_subtype"] = 1.0 if ((entry["ER"] == 1 or entry["PR"] == 1) and entry["HER2"] == 0) else 0.0

            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = li_2011_recurrence_survival_mod()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "N_positive_node": 4,
            "Tumor_grade": '3',
            "ER": 1,
            "PR": 0,
            "HER2": 0
        }
    ))