from django.urls import path
from . import views

urlpatterns = [
    # Auth paths
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Account paths
    path('myaccount/', views.myaccount, name='myaccount'),
    path('myaccount/update/', views.update_profile, name='update_profile'),
]