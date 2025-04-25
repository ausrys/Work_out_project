from django.urls import path
from . import views

urlpatterns = [
    path('program/', views.program_list, name='program_list'),
    path('registration/', views.registration, name='registration'),
    path('programs/create', views.program_registration,
         name="program_registration")
]
