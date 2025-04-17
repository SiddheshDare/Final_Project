import os
import pandas as pd
import numpy as np
from rest_framework import status
import pickle
import json
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score,recall_score,accuracy_score,precision_score,confusion_matrix,classification_report

base_path = os.getcwd()
pickle_path = os.path.normpath(base_path + os.sep + 'pickle')
log_path = os.path.normpath(base_path + os.sep + 'log')
file_path = os.path.join(base_path, "data", "Employee_Attrition_Prediction.csv")

# Data Processing and Model Training
class Training:
    def accuracymeasures(self,y_test,predictions,avg_method):
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average=avg_method)
        recall = recall_score(y_test, predictions, average=avg_method)
        f1score = f1_score(y_test, predictions, average=avg_method)
        target_names = ['0','1']
        print("Classification report")
        print("---------------------","\n")
        print(classification_report(y_test, predictions,target_names=target_names),"\n")
        print("Confusion Matrix")
        print("---------------------","\n")
        print(confusion_matrix(y_test, predictions),"\n")

        print("Accuracy Measures")
        print("---------------------","\n")
        print("Accuracy: ", accuracy)
        print("Precision: ", precision)
        print("Recall: ", recall)
        print("F1 Score: ", f1score)

        return accuracy,precision,recall,f1score


    def load_data(self,attrition):
        target_map = {'Yes': 1, 'No': 0}
        attrition["Attrition_numerical"] = attrition["Attrition"].apply(lambda x: target_map[x])

        if 'Attrition_numerical' in attrition.columns:
            attrition = attrition.drop(['Attrition_numerical'], axis=1)

        categorical = [col for col in attrition.columns if attrition[col].dtype == 'object']
        numerical = attrition.columns.difference(categorical)

        attrition_cat = attrition[categorical].drop(['Attrition'], axis=1)
        attrition_cat = pd.get_dummies(attrition_cat)
        attrition_num = attrition[numerical]

        attrition_final = pd.concat([attrition_num, attrition_cat], axis=1)
        target = attrition["Attrition"].apply(lambda x: target_map[x])

        return attrition_final, target

    def train(self, request):
        return_dict=dict()
        try:
            attrition = pd.read_csv(file_path)
            attrition_final,target=self.load_data(attrition)
            train, test, target_train, target_val = train_test_split(attrition_final, target, train_size= 0.55, random_state=0);
            oversampler = SMOTE(random_state=0)
            smote_train, smote_target = oversampler.fit_resample(train,target_train)

            rf_params = {
                'n_jobs': -1,
                'n_estimators': 1000,
                'max_features': 0.3,
                'max_features': 'sqrt',
                'max_depth': 4,
                'min_samples_leaf': 2,
                'random_state': 0,
                'verbose': 0
            }

            rf = RandomForestClassifier(**rf_params)
            rf.fit(smote_train, smote_target)
            rf_predictions = rf.predict(test)
            accuracy,precision,recall,f1score = self.accuracymeasures(target_val,rf_predictions,'weighted')

            os.makedirs(pickle_path, exist_ok=True) 
            pickle_file = os.path.join(pickle_path, 'model.sav')
            with open(pickle_file, 'wb') as model_file:
                pickle.dump(rf, model_file) 

            
            
            return_dict['response']='Model Train Successfully'
            return_dict['status']=status.HTTP_200_OK
        
        except Exception as e: 
            return_dict['response']=f"Exception when training the module:{str(e)}"
            return_dict['status']=status.HTTP_500_INTERNAL_SERVER_ERROR

        return return_dict