from math import exp
from model_execution import model_execution
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

class dowsett_2018_metastatic_disease_rwd_mod(model_execution):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://doi.org/10.1200/JCO.2017.76.4258",
            "model_name": "Dowsett [2018] Breast cancer - Prediction of Late Distant Recurrence in Patients With Estrogen Receptor–Positive Breast Cancer Treated With 5 Years of Endocrine Therapy"
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            """
            This function is used to convert the input data into the correct format for the model.

            Parameters:
            - input_object: a dictionary, or list with multiple dictionaries, containing the input data

            Returns:
            - preprocessed_data: a dictionary, or list with multiple dictionaries, containing the preprocessed data
            """

            # For N_positive_node, tumor grade,
            feature="N_positive_node"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            try:
                n = int(entry[feature])
            except ValueError:
                raise ValueError(f"{feature} must be an integer number, got {entry[feature]}")

            # normalise number of positive nodes to model requirements
            entry[feature] = n
            entry["N_positive_node_cat"] = (
                0 if n == 0
                else (1 if n == 1
                      else (2 if n <= 3
                            else (3 if n <= 9 else 4)))
            )

            # --- Tumor_grade ---
            allowed_values = {
                "Tumor_grade": [1, 2, 3, 4]}
            # By the model:
            # - grade (three groups: 1, low; 2, intermediate; and 3, high)
            # By https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade:
            # Grade I - Well differentiated (low grade)
            # Grade II 	- Moderately differentiated (intermediate grade)
            # Grade III - Poorly differentiated (high grade)
            # Grade IV - undifferentiated / anaplastic (high grade)
            # diffgrtxt	9	Differentiatiegraad  onbekend / n.v.t.

            feature = "Tumor_grade"
            if feature not in entry:
                raise ValueError(f"Missing {feature}")
            entry[feature]=str(entry[feature])
            if entry[feature]=='I':
                entry[feature]='1'
            elif entry[feature]=='II':
                entry[feature]='2'
            elif entry[feature] == 'III':
                entry[feature] = '3'
            elif entry[feature]=='IV':
                entry[feature]='4'

            # validate values against the allowed list
            validate_categorical_num_feature(entry, feature, allowed_values)

            # normalise Tumor_grade to model requirements
            entry["Tumor_grade"] = (
                1.0 if entry["Tumor_grade"] == 1
                else (2.0 if entry["Tumor_grade"] == 2 else 3.0)
            )

            # --- Age ---
            feature="Age"
            min_f, max_f = [0, 100]
            validate_numerical_feature(entry, feature, min_f,max_f)

            # --- Tumor_size ---
            feature="Tumor_size"
            min_f,max_f=[0,100]
            validate_numerical_feature(entry, feature, min_f, max_f)

            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

    def _calculate_probability_single(self, data):
        """
        Calculate the probability of 2-year survival for a patient with given covariates.

        Parameters:
        - input_object: a dictionary containing the input data

        result I: coefficients are based on the Clinical Treatment Score post–5 years CTS5 (ATAC) dataset
        result II: coefficients are based on the combined CTS5 ATAC and BIG 1-98 datasets
        """

        # result I
        resultI=0.471 * data["N_positive_node_cat"] + 0.98 * (0.164 * data["Tumor_size"]
                                                             -0.003 * data["Tumor_size"] ** 2
                                                             + 0.312 * data["Tumor_grade"]
                                                             + 0.03 * data["Age"])

        # result II
        resultII = 0.438 * data["N_positive_node_cat"] + 0.988 * (0.093 * data["Tumor_size"]
                                                               - 0.001 * data["Tumor_size"] ** 2
                                                               + 0.375 * data["Tumor_grade"]
                                                               + 0.017 * data["Age"])

        return resultII

    def predict(self, data):
        """
                Calculate the probability of 2-year survival for a patient with given covariates.

                Parameters:
                - input_object: a dictionary or list containing the input data
                """

        # Preprocess the input data
        input_object = self._preprocess(data)

        # Calculate the probability
        if isinstance(input_object, dict):
            return self._calculate_probability_single(input_object)
        elif isinstance(input_object, list):
            results = {}
            # loop over numeric index of item list
            for i in range(len(input_object)):
                item = input_object[i]
                if "id" in item:
                    results[item["id"]] = self._calculate_probability_single(item)
                else:
                    results[f"prediction_{str(i)}"] = self._calculate_probability_single(item)
            return results

if __name__ == "__main__":
    model_obj = dowsett_2018_metastatic_disease_rwd_mod()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        {
            "N_positive_node": 9,
            "Tumor_grade": 3,
            "Tumor_size": "15",
            "Age": 78
        }
    ))