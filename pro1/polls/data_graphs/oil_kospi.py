import sqlite3
import pandas as pd
import plotly.express as px

# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("select a.closing_price, a.date, b.closing_price from polls_wtioilprice a inner join polls_kospi b on a.date = b.date order by a.date;") # 달러 4번째 컬럼이 날짜

data = Cur.fetchall()
con.close()

oil_data = []
kospi_data =[]

for i in range(len(data)):
    # 기름 가격 저장
    oil_data.append(data[i][0])
    
    # 코스피 가격 저장
    kospi_data.append(data[i][2])
    
print(data[:10])

# 데이터프레임 형식으로 저장
oil_kospi = pd.DataFrame({'oil_data': oil_data,
                            'kospi_data': kospi_data})

# 상관계수 출력
print(oil_kospi.corr(method='pearson'))


# 금값 - 나스닥 산점도
fig = px.scatter(oil_kospi, x='oil_data', y='kospi_data', title='OIL-KOSPI', size_max=1)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
# 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='OIL', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='KOSPI', showgrid=False),
)

fig.write_html("oil_kospi.html")


# 나스닥값 - 금값 산점도
fig = px.scatter(oil_kospi, x='kospi_data', y='oil_data', title='KOSPI-OIL' , size_max=1)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
# 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    # title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='KOSPI', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='OIL', showgrid=False),
)

fig.write_html("kospi_oil.html")