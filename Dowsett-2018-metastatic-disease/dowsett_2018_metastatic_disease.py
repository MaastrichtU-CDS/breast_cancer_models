from math import exp
from model_execution import model_execution

class dowsett_2018_metastatic_disease(model_execution):
    def __init__(self):
        self._model_parameters = {
            "model_uri": "https://doi.org/10.1200/JCO.2017.76.4258",
            "model_name": "Dowsett [2018] Breast cancer - Prediction of Late Distant Recurrence in Patients With Estrogen Receptor–Positive Breast Cancer Treated With 5 Years of Endocrine Therapy"
        }

    def _preprocess(self, data):
        def preprocess_entry(entry):
            # For hormone receptor, ensure binary integer coding (0 or 1)
            # Should add data validation after we know the format of variables

            # For N_positive_node, tumor grade,
            # ensure the right coding!!!
            n = entry["N_positive_node"]
            entry["N_positive_node_cat"] = (
                0 if n == 0
                else (1 if n == 1
                      else (2 if n <= 3
                            else (3 if n <=9 else 4)))
            )
            entry["Tumor_grade"] = 1.0 if entry["Tumor_grade"] == 'I' else (2.0 if entry["Tumor_grade"] == 'II' else 3.0) # luminal-like

            entry["Age"]=float(entry["Age"])
            entry["Tumor_size"]=float(entry["Tumor_size"])

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
        """

        result=0.471 * data["N_positive_node_cat"] + 0.98 * (0.164 * data["Tumor_size"]
                                                             -0.003 * data["Tumor_size"] ** 2
                                                             + 0.312 * data["Tumor_grade"]
                                                             + 0.03 * data["Age"])

        return result

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

# if __name__ == "__main__":
#     model_obj = dowsett_2018_metastatic_disease()
#     model_obj.get_input_parameters()
#     print(model_obj.predict(
#         {
#             "N_positive_node": 2,
#             "Tumor_grade": "I",
#             "Tumor_size": "5",
#             "Age": 56
#         }
#     ))