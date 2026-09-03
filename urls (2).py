from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='deploy_home'),
    path('webhook/<str:token>/', views.hook_trigger, name='hook_trigger'),
]
