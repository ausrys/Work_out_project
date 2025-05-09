from celery import shared_task
from django.core.cache import cache
from .models import Advertiser
import requests


@shared_task
def fetch_all_advertiser_data():
    advertisers = Advertiser.objects.all()

    for advertiser in advertisers:
        accepted_apis = advertiser.apis.filter(is_accepted=True)

        for api_entry in accepted_apis:
            try:
                response = requests.get(api_entry.api_url, timeout=5)
                response.raise_for_status()
                data = response.json()
                cache_key = f"advertiser_data_{api_entry.id}"
                cache.set(cache_key, {
                    "company": advertiser.company_name,
                    "priority": advertiser.priority,
                    "description": api_entry.description,
                    "data": data
                }, timeout=60 * 10)  # 10 minutes
            except Exception as e:
                cache.set(f"advertiser_data_{api_entry.id}", {
                    "company": advertiser.company_name,
                    "priority": advertiser.priority,
                    "error": str(e)
                }, timeout=60 * 5)
