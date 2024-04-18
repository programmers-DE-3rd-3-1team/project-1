import sqlite3
import pandas as pd
import plotly.express as px

# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("select a.closing_price, a.date, b.index_price from polls_wtioilprice a inner join polls_nasdaqindex b on a.date = b.date order by a.date;") # 달러 4번째 컬럼이 날짜

data = Cur.fetchall()
con.close()

oil_data = []
nasdaq_data =[]

for i in range(len(data)):
    # 기름 가격 저장
    oil_data.append(data[i][0])
    
    # 나스닥 가격 저장
    nasdaq_data.append(data[i][2])
    
print(data[:10])

# 데이터프레임 형식으로 저장
oil_nasdaq = pd.DataFrame({'oil_data': oil_data,
                            'nasdaq_data': nasdaq_data})

# 상관계수 출력
print(oil_nasdaq.corr(method='pearson'))


# 금값 - 나스닥 산점도
fig = px.scatter(oil_nasdaq, x='oil_data', y='nasdaq_data', title='OIL-NASDAQ', size_max=1)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
# 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='OIL', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='NASDAQ', showgrid=False),
)

fig.write_html("oil_nasdaq.html")


# 나스닥값 - 금값 산점도
fig = px.scatter(oil_nasdaq, x='nasdaq_data', y='oil_data', title='NASDAQ-OIL' , size_max=1)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
# 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='NASDAQ', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='OIL', showgrid=False),
)

fig.write_html("nasdaq_oil.html")