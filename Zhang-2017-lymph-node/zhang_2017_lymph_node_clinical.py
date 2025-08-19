from math import exp
from model_execution import logistic_regression

class zhang_2017_lymph_node_clinical(logistic_regression):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://doi.org/10.18632/oncotarget.13330",
            "model_name": "Zhang [2017] Breast cancer - Prediction Model for the probability of axillary lymph node metastasis",
            "intercept": -2.483,
            "covariate_weights": {
                "Age": -0.014,
                "Topography_1": -0.944,
                "Topography_2": -0.529,
                "Topography_3": -1.444,
                "Topography_4": -0.237,
                "Topography_5": -0.642,
                "Tumor_size_2": 0.204,
                "Tumor_size_3":0.663,
                "Node_grade": 1.235,
                "Invasive_disease":0.768,
                "Pathological_type_1": 2.944,
                "Pathological_type_2": 2.884,
                "Pathological_type_3": 2.111,
                "Molecular_subtype_1": 0.322,
                "Molecular_subtype_2": 0.141,
            }
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables

            # For topography (tumor location), node grade, tumor size, pathological type and molecular subtype
            # ensure the right coding!!!
            entry["Topography_1"] = 1.0 if entry["Topography"] == 'UIQ' else 0.0 # upper inner quadrant
            entry["Topography_2"] = 1.0 if entry["Topography"] == 'UOQ' else 0.0 # upper outer quadrant
            entry["Topography_3"] = 1.0 if entry["Topography"] == 'LIQ' else 0.0 # lower inner quadrant
            entry["Topography_4"] = 1.0 if entry["Topography"] == 'LOQ' else 0.0 # lower outer quadrant
            entry["Topography_5"] = 1.0 if entry["Topography"] == 'other' else 0.0 #

            entry["Invasive_disease"] = int(entry["Invasive_disease"])
            entry["Node_grade"] = int(entry["Node_grade"])

            entry["Tumor_size_2"] = 1.0 if entry["Tumor_size"] == '2' else 0.0
            entry["Tumor_size_3"] = 1.0 if entry["Tumor_size"] == '3' else 0.0

            entry["Pathological_type_1"] = 1.0 if entry["Pathological_type"] == 'IDC' else 0.0 # invasive ductal carcinoma
            entry["Pathological_type_2"] = 1.0 if entry["Pathological_type"] == 'ILC' else 0.0 # invasive lobular carcinoma
            entry["Pathological_type_3"] = 1.0 if entry["Pathological_type"] == 'other' else 0.0

            entry["Molecular_subtype_1"] = 1.0 if entry["Molecular_subtype"] == 'LM' else 0.0 # luminal-like
            entry["Molecular_subtype_2"] = 1.0 if entry["Molecular_subtype"] == 'HER2+' else 0.0 # human epidermal growth factor receptor-2

            # Dose values expected as floats (gray units)
            entry['Age'] = float(entry['Age'])
            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = zhang_2017_lymph_node_clinical()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "Age": 45.6,
            "Node_grade": 2,
            "Tumor_size": "3",
            "Invasive_disease" : 1,
            "Topography": "UIQ",
            "Molecular_subtype": "LM",
            "Pathological_type": "ILC",
        }
    ))