from django.urls import path

from authapp.views import Login, Register, logout, profile

app_name = 'authapp'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]