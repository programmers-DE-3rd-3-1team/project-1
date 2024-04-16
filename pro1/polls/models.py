from django.db import models

class OilPrice(models.Model):
    date = models.DateField()
    oil_category = models.CharField(max_length=100)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)