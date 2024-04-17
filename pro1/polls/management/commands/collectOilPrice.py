from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from polls.models import OilPrice 


class Command(BaseCommand):
    help = 'Imports oil price data from an external API and stores it in the database'

    def handle(self, *args, **kwargs):
        url = 'https://apis.data.go.kr/1160100/service/GetGeneralProductInfoService/getOilPriceInfo'
        numOfRows = '300'
        params = {
            'serviceKey': '8cxuw+0na6JIn7RGEEY+raiAzFlxjgwkliFoKvswcIy+w4ktQJMkBfXOVmVEAzCKwv10AQWbSOxUQJXrqHZH2g==',
            'numOfRows': numOfRows,  # 한 페이지 결과 수
            'pageNo': '1',  # 페이지 번호 초기값 설정
            'beginBasDt': '20200101',  # 기준일자가 검색값보다 크거나 같은 데이터 검색
            'endBasDt': '20240401',  # 기준일자가 검색값보다 작은 데이터 검색
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

            # 각 item의 유종구분, 평균가격, 날짜 데이터 모델에 적재
            for item in items:
                oil_type = item.find('oilCtg').text
                date = item.find('basDt').text
                avg_price = float(item.find('wtAvgPrcCptn').text)

                # 모델에 데이터 적재
                oil_price = OilPrice(
                    date=datetime.strptime(date, '%Y%m%d'),
                    oil_type=oil_type,
                    avg_price=avg_price
                )
                oil_price.save()
