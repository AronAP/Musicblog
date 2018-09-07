from django.urls import path, include
#from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name = 'login')
    #(r'^accounts/login/$', login),
    #(r'^accounts/logout/$', logout),
]