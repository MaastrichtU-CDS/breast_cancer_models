from math import exp
from model_execution import logistic_regression

class li_2011_recurrence_survival(logistic_regression):
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

            # For N_positive_node, tumor grade, nd molecular subtype
            # ensure the right coding!!!
            entry["N_positive_node_cat"] = 0 if entry["N_positive_node"] == 0 else (1 if entry["N_positive_node"] <= 3 else 2)
            entry["Tumor_grade"] = 1.0 if entry["Tumor_grade"] == 'I' else (2.0 if entry["Tumor_grade"] == 'II' else 3.0)
            entry["Molecular_subtype"] = 1.0 if ((entry["ER"] == '1' or entry["PR"] == '1') and entry["HER2"] =='0') else 0.0 # luminal-like

            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = li_2011_recurrence_survival()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "N_positive_node": 24,
            "Tumor_grade": "III",
            "ER": "1",
            "PR": "1",
            "HER2": "0"
        }
    ))