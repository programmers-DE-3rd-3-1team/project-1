import sqlite3
from matplotlib import pyplot as plt

# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select * from polls_wtioilprice order by 3") # 기름값 3번째 컬럼이 날짜

data = Cur.fetchall()
con.close()

# print(data[:10])

oil_price = []
oil_date = []

for i in range(len(data)):
    # 가격 저장
    oil_price.append(data[i][3])
  
    oil_date.append(data[i][2])



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




Daily_OIL = pd.DataFrame({'price': oil_price,
                            'date': oil_date})
# print(Daily_OIL)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
fig = px.line(Daily_OIL,
              x="date",
              y="price",
              title='Daily_OIL')
# fig.show()
## 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='Date', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='Price', showgrid=False),
)

fig.write_html("Daily_OIL.html")