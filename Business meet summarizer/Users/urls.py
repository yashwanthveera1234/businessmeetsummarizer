from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .decorators import unAuthenticatedUser, authenticatedUser

app_name = 'Users'

urlpatterns = [
    path('', views.homeView, name = 'homeView'),
    path('login/', unAuthenticatedUser(auth_views.LoginView.as_view(template_name='login.html', redirect_field_name = 'homeView')), name='loginView'),
    path('logout/', authenticatedUser(auth_views.LogoutView.as_view(template_name='logout.html')), name='logoutView'),
    path('register/', unAuthenticatedUser(views.registerView), name='registerView'),
    path('profile/', authenticatedUser(views.profileView), name='profileView'),
    path('del/<int:id>', authenticatedUser(views.delReceiverView), name='delReceiverView'),
]