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
                "Node_hist_grade": ['0', '1', '1M','2', '2A', '2B','3', '3A', '3B', '3C'],  # 0 = baseline, 1/2/3 = dummies
                "Tumor_hist_grade": ['0', '1', '2', '2A', '2B', '3', '4', '4A', '4B', '4C', '4D']
                # 0–1 = baseline group
            }

            # --- Hormone receptor ---
            feature = "Hormone_receptor"
            # --- if either ER or PR are positive, hormone receptore is positive and
            # used as '0' in the model.
            for marker in ["ER", "PR"]:
                validate_categorical_num_feature(entry, marker, allowed_values)

            entry[feature] = 1.0 if (
                        (entry["ER"] == 0 and entry["PR"] == 0)) else 0.0

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
            validate_categorical_str_feature(entry, feature, allowed_values)
            entry["Node_grade_1"] = 1.0 if entry[feature] in ('1', '1M','1A', '1AS', '1B', '1BS', '1C', '1CS','1MS') else 0.0
            entry["Node_grade_2"] = 1.0 if entry[feature] in ('2', '2A','2AS', '2B') else 0.0
            entry["Node_grade_3"] = 1.0 if entry[feature] in ('3', '3A', '3B', '3C') else 0.0

            # --- Tumor size ---
            feature = "Tumor_hist_grade"
            validate_categorical_str_feature(entry, feature, allowed_values)
            entry["Tumor_size_2"] = 1.0 if entry[feature] in ('2', '2A', '2B') else 0.0
            entry["Tumor_size_3_4"] = 1.0 if entry[feature] in ('3', '4', '4A', '4B', '4C', '4D') else 0.0

            # Age values expected as floats (years)
            feature="Age"
            entry[feature] = float(entry[feature])
            min_f, max_f = [0, 100]
            validate_numerical_feature(entry, feature, min_f, max_f)

            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = Chen_2016_overall_survival_NCKUHmodel_rwd_mod()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        [{'Age': 45.6, 'Tumor_grade': 'II', 'Tumor_hist_grade': 3, 'Node_hist_grade': 3, 'ER': '1', 'PR': '1'},
         {'Age': 98, 'Tumor_grade': 'II', 'Tumor_hist_grade': 3, 'Node_hist_grade': 3, 'ER': '1', 'PR':'1'}]
    ))