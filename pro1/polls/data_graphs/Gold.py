import sqlite3
from matplotlib import pyplot as plt

# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select * from polls_goldprice order by 2;") # 금값 2번째 컬럼이 날짜

data = Cur.fetchall()
con.close()

# print(data[:10])

gold_price = []
gold_date = []

for i in range(len(data)):
    # 가격 저장
    gold_price.append(data[i][2])
    
    # 날짜 뒤에 시간 빼고 연도-월-일 으로 저장
    gold_date.append(data[i][1])



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




Daily_GOLD = pd.DataFrame({'price': gold_price,
                            'date': gold_date})
# print(Daily_GOLD)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
fig = px.line(Daily_GOLD,
              x="date",
              y="price",
              title='Daily_GOLD')
# fig.show()
## 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='Date', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='Price', showgrid=False),
)

fig.write_html("Daily_GOLD.html")