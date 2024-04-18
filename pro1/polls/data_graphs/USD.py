import sqlite3
import pandas as pd
import plotly.express as px

# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select * from polls_exchangerate order by 4;") # 달러 4번째 컬럼이 날짜

data = Cur.fetchall()
con.close()

USD_price = []
USD_date = []

for i in range(len(data)):
    # 가격 저장
    USD_price.append(data[i][1])
    
    # 날짜 저장
    USD_date.append(data[i][3])
    
# print(data[:10])




Daily_USD = pd.DataFrame({'price': USD_price,
                            'date': USD_date})
# print(Daily_USD)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
fig = px.line(Daily_USD,
              x="date",
              y="price",
              title='Daily_USD')
# fig.show()
## 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='Date', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='Price', showgrid=False),
)

fig.write_html("Daily_USD.html")



