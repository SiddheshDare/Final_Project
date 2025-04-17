from django.urls import path
from .views import TrainChurnModelView, PredChurnModelView

urlpatterns = [
    path('training/', TrainChurnModelView.as_view(), name='model_training'),
    path('prediction/', PredChurnModelView.as_view(), name='model_prediction'),
]