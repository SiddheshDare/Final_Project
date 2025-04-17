from django.urls import path
from .views import TrainChurnModelView, PredChurnModelView, HealthCheckView

urlpatterns = [
    path('training/', TrainChurnModelView.as_view(), name='model_training'),
    path('prediction/', PredChurnModelView.as_view(), name='model_prediction'),
    path('training/health/', HealthCheckView.as_view(), name='health_check'),
]