from django.core.management.base import BaseCommand
from polls.models import *

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        # # OilPrice.objects.all().delete()
        # all_oil_data = OilPrice.objects.all()
        # for data in all_oil_data:
        #     print(f"Oil Category: {data.oil_category}, Date: {data.date}, Average Price: {data.avg_price}")
        

        # all_gold_data = GoldPrice.objects.all()
        # for data in all_gold_data:
        #     print(f"gold Category: {data.gold_type}, Date: {data.date}, Closing Price: {data.closing_price}")
        GoldPrice.objects.all().delete()

        # all_exchange_data = ExchangeRate.objects.all()
        # for data in all_exchange_data:
        #     print(f"cur_unit: {data.cur_unit}, deal_bas_r: {data.deal_bas_r}, search_date: {data.search_date}")
   