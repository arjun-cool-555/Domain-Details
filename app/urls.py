from django.urls import path
from . import views

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('details/',views.DetailsPage,name='details'),
    path('logout/',views.LogoutPage,name='logout'),
]

