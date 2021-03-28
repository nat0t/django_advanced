from django.urls import path

from authapp.views import Login, Register, logout, profile, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('verify/<email>/<activation_key>/', verify, name='verify'),
]
