import sqlite3
from matplotlib import pyplot as plt

# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select * from polls_kospi order by 2;") # 2가 날짜임

data = Cur.fetchall()
con.close()

# print(data[:10])

price = []
date = []

for i in range(len(data)):
    # 가격 저장
    price.append(data[i][2])
    
    # 날짜 뒤에 시간 빼고 연도-월-일 으로 저장
    date.append(data[i][1])



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




Daily_KOSPI = pd.DataFrame({'price': price,
                            'date': date})
# print(Daily_KOSPI)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
fig = px.line(Daily_KOSPI,
              x="date",
              y="price",
              title='Daily_KOSPI')
# fig.show()
## 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='Date', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='Price', showgrid=False),
)

fig.write_html("Daily_KOSPI.html")