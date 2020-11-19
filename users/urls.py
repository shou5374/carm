from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_up/', views.SignUpView.as_view(template_name='users/sign_up.html'), name='sign_up'),
    path('create_group/', views.CreateGroupView.as_view(), name='create_group'),
    path('manage_and_search_group/', views.ManageAndSearchGroupView.as_view(), name='manage_and_search_group'),
    path('manage_group/<str:group_name>', views.ManageGroupView.as_view(), name='manage_group'),
]