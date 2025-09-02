from django.urls import path
from . import views
app_name = 'atun'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('email_send/', views.email_send, name='email_send'),
    path('verify/', views.verify_otp, name='verify'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('tutorial/', views.tutorial, name='tutorial'),

]