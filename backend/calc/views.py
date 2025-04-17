from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from calc.services.prediction import Prediction
from calc.services.training import Training 

class TrainChurnModelView(APIView): 
    def get(self,request):
        train_obj=Training()
        response_dict=train_obj.train(request)
        response=response_dict['response']
        status_value=response_dict['status']
        return Response(response,status_value)

class PredChurnModelView(APIView): 
    def post(self,request):
        pred_obj=Prediction()
        response_dict=pred_obj.predict(request)
        response=response_dict['response']
        status_value=response_dict['status']
        return Response(response,status_value)

from rest_framework import status

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)