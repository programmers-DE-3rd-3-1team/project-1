import sqlite3
from matplotlib import pyplot as plt
import pandas as pd
# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM polls_kospi;", con)
con.close()
# 날짜를 datetime 형식으로 변환하고, 시간을 제거
df['date'] = pd.to_datetime(df['date']).dt.date

# 날짜가 비어있는 행 제거
df = df.dropna(subset=['date'])

# 날짜를 인덱스로 설정
df = df.set_index('date')

# 일주일 단위로 평균 계산
weekly_avg = df['price'].resample('W').mean()

# 결과 출력
print(weekly_avg)
    