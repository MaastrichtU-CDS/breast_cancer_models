from math import exp
from pyexpat import features
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

def validate_categorical_str_feature(data: Any, feature: str, categories) -> bool:
    if feature not in data:
        raise ValueError(f"Missing {feature}")
    try:
        data[feature] = str(data[feature])
    except (TypeError, ValueError):
        raise TypeError(f"Input variable {feature} must be string")

    if data[feature] not in categories[feature]:
        raise ValueError(f"Input feature {feature} value is not allowed: {data[feature]}")
    return True

def validate_numerical_feature(data: Any, feature: str, min_value: float, max_value: float) -> bool:
  """
  Validates a numerical feature in a dictionary or list of dictionaries.

  Parameters:
  - data: dict or list of dicts containing the input data
  - feature: str, the name of the feature to validate
  - min_value: float, minimum allowed value (must not be None)
  - max_value: float, maximum allowed value (must not be None)

  Raises:
  - ValueError if the feature is missing or out of range
  - TypeError if the feature is not a number (rejects bools)
  """
  # Guard against missing range bounds
  if min_value is None or max_value is None:
    raise ValueError(f"Allowed range for feature '{feature}' is not available")

  def _check_value(val: Any, idx: Optional[int] = None):
    label = f"item {idx}" if idx is not None else "object"
    # Reject booleans explicitly: isinstance(True, int) == True, so check bool first
    if isinstance(val, bool) or not isinstance(val, (int, float)):
      raise TypeError(f"Invalid {feature} type in {label}, expected a number")
    if not (min_value <= val <= max_value):
      raise ValueError(f"Invalid {feature} value in {label}: {val} (Allowed range: {min_value}-{max_value})")

  if isinstance(data, list):
    for i, item in enumerate(data):
      if not isinstance(item, dict):
        raise TypeError(f"Invalid input at item {i}: expected a dict")
      if feature not in item:
        raise ValueError(f"Missing {feature} in item {i}")
      # safe get, avoid raising KeyError
      try:
          item[feature] = float(item.get(feature))
      except (TypeError, ValueError):
          raise TypeError(f"Input variable {feature} must be a number")
      val = item.get(feature)
      _check_value(val, i)
  else:
    if not isinstance(data, dict):
      raise TypeError("Input data must be a dict or list of dicts")
    if feature not in data:
      raise ValueError(f"Missing {feature}")
    try:
        data[feature] = float(data.get(feature))
    except (TypeError, ValueError):
        raise TypeError(f"Input variable {feature} must be a number")
    val = data.get(feature)
    _check_value(val, None)

  return True

class zhang_2017_lymph_node_clinical_mod(logistic_regression):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://doi.org/10.18632/oncotarget.13330",
            "model_name": "Zhang [2017] Breast cancer - Prediction Model for the probability of axillary lymph node metastasis",
            "intercept": -2.483,
            "covariate_weights": {
                "Age": -0.014,
                "Topography_1": -0.944, # mediaal boven
                "Topography_2": -0.529, # lateraal boven
                "Topography_3": -1.444, # mediaal onder  locatie
                "Topography_4": -0.237, # Lateraal onder
                "Topography_5": -0.642, # Axillaire uitloper | NNO | Overlappend | Tepel
                "Tumor_size_2": 0.204, #ct=2
                "Tumor_size_3":0.663, # ct=3
                "Node_clin_grade": 1.235,
                "Invasive_disease":0.768,
                "Pathological_type_1": 2.944, # ductaal
                "Pathological_type_2": 2.884, # Lobulair
                "Pathological_type_3": 2.111, # Other
                "Molecular_subtype_1": 0.322, #Luminal
                "Molecular_subtype_2": 0.141, #HER2+
            }
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables
            allowed_values = {
                "Topography": ['UIQ', 'UOQ', 'LIQ', 'LOQ', 'other'],
                "Invasive_disease": [0, 1],
                "Node_clin_grade": [0, 1,2,3],  # adjust max nodes if needed
                "Tumor_clin_grade": [0,1,2,3],  # assume 1 = baseline
                "Pathological_type": ['IDC', 'ILC','DCIS-Mi', 'other'],
                "ER": [0, 1],  # 0 = negative, 1 = positive
                "PR": [0, 1],  # 0 = negative, 1 = positive
                "HER2": [0, 1]  # 0 = negative, 1 = positive
            }
            # For topography (tumor location), node grade, tumor size, pathological type and molecular subtype
            # ensure the right coding!!!

            # Age expected as floats
            feature='Age'
            min_f, max_f = [0, 100]
            validate_numerical_feature(entry,feature,min_f, max_f)

            # --- Topography ---
            feature="Topography"
            validate_categorical_str_feature(entry,feature,allowed_values)
            entry["Topography_1"] = 1.0 if entry[feature] == 'UIQ' else 0.0 # upper inner
            entry["Topography_2"] = 1.0 if entry[feature] == 'UOQ' else 0.0 # upper outer
            entry["Topography_3"] = 1.0 if entry[feature] == 'LIQ' else 0.0 # lower inner
            entry["Topography_4"] = 1.0 if entry[feature] == 'LOQ' else 0.0 # lower outer
            entry["Topography_5"] = 1.0 if entry[feature] == 'other' else 0.0

            # --- Invasive_disease ---
            feature="Invasive_disease"
            validate_categorical_num_feature(entry,feature,allowed_values)

            # --- Node_grade ---
            feature="Node_clin_grade"
            entry[feature] = str(entry[feature])
            if entry[feature] == 'I':
                entry[feature] = '1'
            elif entry[feature] == 'II':
                entry[feature] = '2'
            elif entry[feature] == 'III':
                entry[feature] = '3'
            validate_categorical_num_feature(entry,feature,allowed_values)
            entry[feature]=1.0 if entry[feature] > 0 else 0.0

            # --- Tumor_size ---
            feature="Tumor_clin_grade"
            entry[feature] = str(entry[feature])
            if entry[feature] == 'I':
                entry[feature] = '1'
            elif entry[feature] == 'II':
                entry[feature] = '2'
            elif entry[feature] == 'III':
                entry[feature] = '3'
            validate_categorical_num_feature(entry,feature,allowed_values)
            entry["Tumor_size_2"] = 1.0 if entry[feature] == 2 else 0.0
            entry["Tumor_size_3"] = 1.0 if entry[feature] == 3 else 0.0

            # --- Pathological_type ---
            feature="Pathological_type"
            validate_categorical_str_feature(entry,feature,allowed_values)
            entry["Pathological_type_1"] = 1.0 if entry[feature] == 'IDC' else 0.0 # invasive ductal carcinoma
            entry["Pathological_type_2"] = 1.0 if entry[feature] == 'ILC' else 0.0 # invasive lobular carcinoma
            entry["Pathological_type_3"] = 1.0 if entry[feature] == 'other' else 0.0

            # --- Molecular_subtype ---
            # --- ER, PR, HER2 ---
            for marker in ["ER", "PR", "HER2"]:
                validate_categorical_num_feature(entry,marker,allowed_values)

            entry["Molecular_subtype_1"] = 1.0 if ((entry["ER"] == 1 or entry["PR"] == 1) and entry["HER2"] == 0) else 0.0 #Luminal
            entry["Molecular_subtype_2"] = 1.0 if ((entry["ER"] == 0 or entry["PR"] == 0) and entry["HER2"] == 1) else 0.0 #HER2+

            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = zhang_2017_lymph_node_clinical_mod()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "Age": 45.6,
            "Node_clin_grade": 3,
            "Tumor_clin_grade": 2,
            "Invasive_disease" : 1,
            "Topography": "UIQ",
            "ER": 0,
            "PR": 0,
            "HER2": 1,
            "Pathological_type": "ILC",
        }
    ))