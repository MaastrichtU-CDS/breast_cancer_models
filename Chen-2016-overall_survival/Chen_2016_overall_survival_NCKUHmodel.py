from math import exp
from model_execution import logistic_regression

class Chen_2016_overall_survival_NCKUHmodel(logistic_regression):
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
            entry['Hormone_receptor'] = 1.0 if entry['Hormone_receptor'] == 0 else 0  # 0=positive, 1=negative

            # For tumor grade, node grade and tumor size, ensure the right coding
            entry["Tumor_grade_II"] = 1.0 if entry["Tumor_grade"] == 'II' else 0.0
            entry["Tumor_grade_III"] = 1.0 if entry["Tumor_grade"] == 'III' else 0.0
            entry["Tumor_grade_IV"] = 1.0 if entry["Tumor_grade"] == 'IV' else 0.0

            entry["Node_grade_1"] = 1.0 if entry["Node_grade"] == '1' else 0.0
            entry["Node_grade_2"] = 1.0 if entry["Node_grade"] == '2' else 0.0
            entry["Node_grade_3"] = 1.0 if entry["Node_grade"] == '3' else 0.0

            entry["Tumor_size_2"] = 1.0 if entry["Tumor_size"] == '2' else 0.0
            entry["Tumor_size_3_4"] = 1.0 if (entry["Tumor_size"] == '3' or entry["Tumor_size"] == '4') else 0.0

            # Dose values expected as floats (gray units)
            entry['Age'] = float(entry['Age'])
            return entry

        if isinstance(data, list):
            return [preprocess_entry(d) for d in data]
        else:
            return preprocess_entry(data)

if __name__ == "__main__":
    model_obj = Chen_2016_overall_survival_NCKUHmodel()
    model_obj.get_input_parameters()
    print(model_obj.predict(
        [
            {"Age": 45.6, "Tumor_grade": "III", "Node_grade": "2", "Tumor_size": "3", "Hormone_receptor": 0},
            {"Age": 60.2, "Tumor_grade": "II", "Node_grade": "1", "Tumor_size": "2", "Hormone_receptor": 1}
        ]
    ))