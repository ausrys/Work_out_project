from django.db import models


class UserPayment(models.Model):

    user = models.ForeignKey('Sportsman', on_delete=models.CASCADE)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_value} USD"
