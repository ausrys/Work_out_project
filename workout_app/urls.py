from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    # path('user/programs/', views.user_programs, name='user_programs'),
]
