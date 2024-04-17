from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from polls.models import NasdaqIndex
from django.core.management.base import BaseCommand

# 나오는 사트의 날짜를 수동으로 설정해줘야합니다.
class Command(BaseCommand):
    help = 'Collect exchange rate data from API'
    def handle(self, *args, **kwargs):

      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
      driver.get("https://kr.investing.com/indices/nq-100-historical-data")
      driver.implicitly_wait(30)
      # 데이터가 안나올떄까지 루프를 돌립니다.
      i = 1
      while True:
          try:
              new_element = {'date': None, 'index': None}
              new_element['date'] = datetime.strptime(driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[{i}]/td[1]/time').text, '%Y- %m- %d')
              price_text = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[{i}]/td[2]').text
              new_element['index'] = float(price_text.replace(',', ''))
              NasdaqIndex(**new_element).save()
              i += 1
          except NoSuchElementException:
              break
      driver.quit()