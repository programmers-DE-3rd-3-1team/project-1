from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from polls.models import GoldPrice 


class Command(BaseCommand):
    help = 'Imports gold price data from an external API and stores it in the database'

    def handle(self, *args, **kwargs):
        url = 'https://apis.data.go.kr/1160100/service/GetGeneralProductInfoService/getGoldPriceInfo'
        numOfRows = '300'
        params = {
            'serviceKey': '8cxuw+0na6JIn7RGEEY+raiAzFlxjgwkliFoKvswcIy+w4ktQJMkBfXOVmVEAzCKwv10AQWbSOxUQJXrqHZH2g==',
            'numOfRows': numOfRows,  # 한 페이지 결과 수
            'pageNo': '1',  # 페이지 번호 초기값 설정
            'beginBasDt' : '20200101',  # 기준일자가 검색값보다 크거나 같은 데이터 검색
            'endBasDt' : '20240401',  # 기준일자가 검색값보다 작은 데이터 검색
            'itmsNm' : '금 99.99_1Kg'
        }

        # 첫 번째 요청을 보내서 전체 결과 수를 얻기
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'xml')

        # 전체 결과 수를 가져오기
        total_count = int(soup.find('totalCount').text)

        # 모든 페이지에 대해 요청을 보내고 데이터 수집
        for page_number in range(1, (total_count // int(numOfRows)) + 2):  # 전체 결과 수를 페이지당 결과 수로 나눈 몫에 1을 더한만큼의 페이지를 요청
            params['pageNo'] = str(page_number)
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.text, 'xml')

            items = soup.find_all('item')

            # 각 페이지의 데이터를 gold_data에 추가
            for item in items:
                gold_type = item.find('itmsNm').text
                date = item.find('basDt').text
                closing_price = float(item.find('clpr').text)  # 종가를 기준으로 데이터 저장

                # 모델에 데이터 적재
                gold_price = GoldPrice(
                    date=datetime.strptime(date, '%Y%m%d'),
                    gold_type=gold_type,
                    closing_price=closing_price
                )
                gold_price.save()

