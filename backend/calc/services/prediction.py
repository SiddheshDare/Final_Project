import os
import pandas as pd
import json
import pickle
from rest_framework import status

base_path = os.getcwd()
pickle_path = os.path.normpath(base_path + os.sep + 'pickle')

class Prediction:
    def predict(self, request):
        return_dict = {}

        try:
            # Load the trained model
            pickle_file = os.path.normpath(pickle_path + os.sep + 'model.sav')
            if not os.path.exists(pickle_file):
                return {
                    "response": "Error: Model file not found!",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }

            model = pickle.load(open(pickle_file, 'rb'))

            # Load request data
            input_data = json.loads(request.body.decode('utf-8'))
            df_pred = pd.json_normalize(input_data)

            # **Manually define categorical columns (these were one-hot encoded in training)**
            categorical_features = ["BusinessTravel", "Department", "EducationField", "Gender", "JobRole", "MaritalStatus", "OverTime"]

            # **One-hot encode categorical features**
            df_pred = pd.get_dummies(df_pred)

            # **Ensure all required features exist and fill missing ones with 0**
            expected_features = model.feature_names_in_  # Features used during training
            for col in expected_features:
                if col not in df_pred.columns:
                    df_pred[col] = 0  # Assign 0 to missing one-hot encoded features

            # **Ensure proper feature order**
            df_pred = df_pred[expected_features]

            # Make prediction
            prediction = model.predict(df_pred)
            probability = model.predict_proba(df_pred)[:, 1]  # Probability of "Yes"

            input_data.clear()

            input_data["prediction"] = "Yes" if prediction[0] == 1 else "No"
            input_data["probability"] = float(probability[0])

            return_dict["response"] = input_data
            return_dict["status"] = status.HTTP_200_OK
            return return_dict

        except Exception as e:
            return_dict["response"] = f"Exception when prediction: {str(e)}"
            return_dict["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            return return_dict
