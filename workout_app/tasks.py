from celery import shared_task
from django.core.cache import cache
from .models import Advertiser
import requests


@shared_task
def fetch_all_advertiser_data():

    advertisers = Advertiser.objects.all()

    for advertiser in advertisers:
        try:
            response = requests.get(advertiser.api_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            cache_key = f"advertiser_data_{advertiser.id}"
            cache.set(cache_key, {
                "company": advertiser.company_name,
                "priority": advertiser.priority,
                "description": advertiser.description,
                "data": data
            }, timeout=60 * 10)  # 10 minutes

        except Exception as e:
            cache.set(f"advertiser_data_{advertiser.id}", {
                "company": advertiser.company_name,
                "priority": advertiser.priority,
                "error": str(e)
            }, timeout=60 * 5)
