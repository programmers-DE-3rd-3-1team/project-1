from django.core.management.base import BaseCommand
from polls.models import ExchangeRate
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import requests
import json

class Command(BaseCommand):
    help = 'Collect exchange rate data from API'

    def handle(self, *args, **kwargs):
        URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        API_KEY = 'f8w4rCzj8xk38bdsBlSOi1EWpoWSJVWP'
        # 60일간의 날짜 생성

        dates = []
        for i in range(60):
            dates.append((datetime.now() - timedelta(days = i)).strftime('%Y%m%d'))

        data = []
        for date in dates:
            urs = '{URL}?authkey={API_KEY}&searchdate={date}&data=AP01'.format(URL=URL, API_KEY=API_KEY, date=date)
            rq = requests.get(urs)
            # JSON을 파이썬 객체로 변환
            response_data = json.loads(rq.text)
            for item in response_data:
                # USD, JPY(100) 환율만 추출
                if item['cur_unit'] == 'USD' or item['cur_unit'] == 'JPY(100)':
                    new_item = {key: item[key] for key in ['cur_unit', 'deal_bas_r']}
                    new_item['deal_bas_r'] = float(new_item['deal_bas_r'].replace(',', ''))
                    naive_datetime = datetime.strptime(date, "%Y%m%d")
                    my_timezone = pytz.timezone('Asia/Seoul')
                    new_item['search_date'] = timezone.make_aware(naive_datetime, timezone=my_timezone)
                    exchange_rate = ExchangeRate(**new_item)
                    exchange_rate.save()
        