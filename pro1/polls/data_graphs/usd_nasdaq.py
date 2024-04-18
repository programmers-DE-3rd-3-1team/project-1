import sqlite3
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px

# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select a.rate, a.date from polls_exchangerate a inner join polls_nasdaqindex b on a.date = b.date order by a.date;") 

data = Cur.fetchall()
con.close()

USD_price = []
USD_date = []

for i in range(len(data)):
    # 가격 저장
    USD_price.append(data[i][0])
    
    # 날짜 저장
    USD_date.append(data[i][1])
    
# print(data[:10])
# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select a.index_price, a.date from polls_nasdaqindex a inner join polls_exchangerate b on a.date = b.date order by a.date;") 

data = Cur.fetchall()
con.close()

# print(data[:10])

nasdaq_price = []
nasdaq_date = []

for i in range(len(data)):
    # 가격 저장
    nasdaq_price.append(data[i][0])
    
    # 날짜 뒤에 시간 빼고 연도-월-일 으로 저장
    nasdaq_date.append(data[i][1])


usd_nasdaq = pd.DataFrame({'usd_data': USD_price
                        ,'nasdaq_data': nasdaq_price})

# 상관계수 출력
#print(usd_gold.corr(method='pearson'))

fig = px.scatter(usd_nasdaq, x='usd_data', y='nasdaq_data', title='USD-NSADAQ', size_max=1)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
# 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='USD', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='NSADAQ', showgrid=False),
)

fig.write_html("usd_nasdaq.html")