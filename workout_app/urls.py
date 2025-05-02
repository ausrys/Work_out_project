from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('user/programs/<int:user_id>', views.get_user_programs, name='user_programs'),
    path('user-info/<int:user_id>/', views.get_user_profile, name='user-profile'),
    path('coaches/', views.get_all_coaches, name='get_all_coaches'),
]
