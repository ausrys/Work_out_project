from django.db import models


class Advertiser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    company_name = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)  # 0 = low priority ads
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.email})"


class AdvertiserAPI(models.Model):
    advertiser = models.ForeignKey(
        "Advertiser", on_delete=models.CASCADE, related_name="apis")
    api_url = models.URLField()
    description = models.TextField(blank=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.api_url} ({'Accepted' if self.is_accepted else 'Pending'})"
