from django.urls import path
from . import views

app_name = 'car'
urlpatterns = [
    path('manage_car/', views.ManageCarView.as_view(), name='manage_car'),
]