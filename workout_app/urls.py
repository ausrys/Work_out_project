from django.urls import path
from workout_app.views import *


urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', login_view, name='login'),
    path('user/programs/', get_user_programs, name='user_programs'),
    path('user-info/', get_user_profile,
         name='user-profile'),
    path('coaches/', get_all_coaches, name='get_all_coaches'),
    path('create-checkout-session/', create_checkout_session),
    path('webhooks/stripe/', stripe_webhook),
    path('payments/', user_payments),
    path('get-advertiser-data/', get_advertiser_data),
    path('advertisers/register/', advertiser_register),
    path('advertisers/login/', advertiser_login),
    path('blogs/', get_all_articles),
    path('logout/', logout_user, name='logout')
]
