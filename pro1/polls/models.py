from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=10)
    deal_bas_r = models.FloatField()
    search_date = models.DateTimeField()

    def __str__(self):
        return self.cur_unit

class OilPrice(models.Model):
    oil_category = models.CharField(max_length=100)
    date = models.DateField()
    avg_price = models.DecimalField(max_digits=10, decimal_places=2) # 평균 가격

class GoldPrice(models.Model):
    gold_type = models.CharField(max_length=100)  # 금 종류
    date = models.DateField()  # 날짜
    closing_price = models.DecimalField(max_digits=10, decimal_places=2)  # 종가
class NasdaqIndex(models.Model):
    date = models.DateField()
    index = models.FloatField()