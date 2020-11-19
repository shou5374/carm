from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('manage_book/', views.ManageBookView.as_view(), name='manage_book'),
    path('add_info/', views.AddInfoView.as_view(), name='add_info'),
]