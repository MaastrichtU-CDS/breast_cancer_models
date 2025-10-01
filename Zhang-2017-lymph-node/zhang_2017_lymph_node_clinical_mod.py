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
            allowed_values = {
                "Topography": ['UIQ', 'UOQ', 'LIQ', 'LOQ', 'other'],
                "Invasive_disease": [0, 1],
                "Node_grade": [0, 1],  # adjust max nodes if needed
                "Tumor_size_grade": ['1', '2', '3'],  # assume 1 = baseline
                "Pathological_type": ['IDC', 'ILC', 'other'],
                # "Molecular_subtype": ['LM', 'HER2+', 'other']
                "ER": [0, 1],  # 0 = negative, 1 = positive
                "PR": [0, 1],  # 0 = negative, 1 = positive
                "HER2": [0, 1]  # 0 = negative, 1 = positive
            }
            # For topography (tumor location), node grade, tumor size, pathological type and molecular subtype
            # ensure the right coding!!!

            # Age expected as floats
            entry['Age'] = float(entry['Age'])

            # --- Topography ---
            if "Topography" not in entry:
                raise ValueError("Missing Topography")
            if entry["Topography"] not in allowed_values["Topography"]:
                raise ValueError(f"Invalid Topography value: {entry['Topography']}")

            entry["Topography_1"] = 1.0 if entry["Topography"] == 'UIQ' else 0.0
            entry["Topography_2"] = 1.0 if entry["Topography"] == 'UOQ' else 0.0
            entry["Topography_3"] = 1.0 if entry["Topography"] == 'LIQ' else 0.0
            entry["Topography_4"] = 1.0 if entry["Topography"] == 'LOQ' else 0.0
            entry["Topography_5"] = 1.0 if entry["Topography"] == 'other' else 0.0

            # --- Invasive_disease ---
            if "Invasive_disease" not in entry:
                raise ValueError("Missing Invasive_disease")
            try:
                entry["Invasive_disease"] = int(entry["Invasive_disease"])
            except ValueError:
                raise ValueError(f"Invasive_disease must be integer, got {entry['Invasive_disease']}")
            if entry["Invasive_disease"] not in allowed_values["Invasive_disease"]:
                raise ValueError(f"Invalid Invasive_disease value: {entry['Invasive_disease']}")

            # --- Node_grade ---
            if "Node_grade" not in entry:
                raise ValueError("Missing Node_grade")
            try:
                entry["Node_grade"] = int(entry["Node_grade"])
            except ValueError:
                raise ValueError(f"Node_grade must be integer, got {entry['Node_grade']}")
            if entry["Node_grade"] not in allowed_values["Node_grade"]:
                raise ValueError(f"Invalid Node_grade value: {entry['Node_grade']}")

            # --- Tumor_size ---
            if "Tumor_size_grade" not in entry:
                raise ValueError("Missing Tumor_size")
            if str(entry["Tumor_size_grade"]) not in allowed_values["Tumor_size_grade"]:
                raise ValueError(f"Invalid Tumor_size value: {entry['Tumor_size_grade']}")
            entry["Tumor_size_2"] = 1.0 if entry["Tumor_size_grade"] == '2' else 0.0
            entry["Tumor_size_3"] = 1.0 if entry["Tumor_size_grade"] == '3' else 0.0

            # --- Pathological_type ---
            if "Pathological_type" not in entry:
                raise ValueError("Missing Pathological_type")
            if entry["Pathological_type"] not in allowed_values["Pathological_type"]:
                raise ValueError(f"Invalid Pathological_type value: {entry['Pathological_type']}")
            entry["Pathological_type_1"] = 1.0 if entry["Pathological_type"] == 'IDC' else 0.0
            entry["Pathological_type_2"] = 1.0 if entry["Pathological_type"] == 'ILC' else 0.0
            entry["Pathological_type_3"] = 1.0 if entry["Pathological_type"] == 'other' else 0.0

            # --- Molecular_subtype ---
            # --- ER, PR, HER2 ---
            for marker in ["ER", "PR", "HER2"]:
                if marker not in entry:
                    raise ValueError(f"Missing {marker}")
                if entry[marker] not in allowed_values[marker]:
                    raise ValueError(f"Invalid {marker} value: {entry[marker]}")
                entry[marker] = int(entry[marker])

            entry["Molecular_subtype_1"] = 1.0 if ((entry["ER"] == 1 or entry["PR"] == 1)) else 0.0
            entry["Molecular_subtype_2"] = 1.0 if ((entry["ER"] == 0 or entry["PR"] == 0) and entry["HER2"] == 1) else 0.0

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
            "Node_grade": 1,
            "Tumor_size_grade": 3,
            "Invasive_disease" : 1,
            "Topography": "UIQ",
            "ER": 0,
            "PR": 1,
            "HER2": 0,
            "Pathological_type": "ILC",
        }
    ))