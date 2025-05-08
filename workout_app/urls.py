from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('user/programs/', views.get_user_programs, name='user_programs'),
    path('user-info/', views.get_user_profile,
         name='user-profile'),
    path('coaches/', views.get_all_coaches, name='get_all_coaches'),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhooks/stripe/', views.stripe_webhook),
    path('payments/', views.user_payments),
    path('get-advertiser-data/', views.get_advertiser_data)
]
