import sqlite3
import pandas as pd
import plotly.express as px

#####################################################################################

gold_corr_ls = []

# 달러 - 금 상관계수
# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.closing_price as gold_price, a.date, b.rate as usd_price
    FROM polls_goldprice a
    INNER JOIN polls_exchangerate b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
gold_usd = pd.DataFrame(data, columns=['gold_price', 'date', 'usd_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
gold_usd_rolling_corr = gold_usd['gold_price'].rolling(window=window_size).corr(gold_usd['usd_price'])

# print(gold_usd_rolling_corr)

# `pandas.core.series.Series`의 타입에서는 인덱싱을 .iloc를 사용한다.
gold_corr_ls.append(round(gold_usd_rolling_corr.iloc[-1], 4))
print(gold_corr_ls)
#####################################################################################

# 달러 - 기름 상관계수
# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.closing_price as gold_price, a.date, b.closing_price as oil_price
    FROM polls_goldprice a
    INNER JOIN polls_wtioilprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
gold_oil = pd.DataFrame(data, columns=['gold_price', 'date', 'oil_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
gold_oil_rolling_corr = gold_oil['gold_price'].rolling(window=window_size).corr(gold_oil['oil_price'])

# print(gold_oil_rolling_corr)

# `pandas.core.series.Series`의 타입에서는 인덱싱을 .iloc를 사용한다.
gold_corr_ls.append(round(gold_oil_rolling_corr.iloc[-1], 4))
print(gold_corr_ls)
#####################################################################################

# 달러 - 코스피 상관계수
# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.closing_price as gold_price, a.date, b.closing_price as kospi_price
    FROM polls_goldprice a
    INNER JOIN polls_kospi b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
gold_kospi = pd.DataFrame(data, columns=['gold_price', 'date', 'kospi_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
gold_kospi_rolling_corr = gold_kospi['gold_price'].rolling(window=window_size).corr(gold_kospi['kospi_price'])

# print(gold_kospi_rolling_corr)

# `pandas.core.series.Series`의 타입에서는 인덱싱을 .iloc를 사용한다.
gold_corr_ls.append(round(gold_kospi_rolling_corr.iloc[-1], 4))
print(gold_corr_ls)
#####################################################################################

# 달러 - 나스닥 상관계수
# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.closing_price as gold_price, a.date, b.index_price as nasdaq_price
    FROM polls_goldprice a
    INNER JOIN polls_nasdaqindex b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
gold_nasdaq = pd.DataFrame(data, columns=['gold_price', 'date', 'nasdaq_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
gold_nasdaq_rolling_corr = gold_nasdaq['gold_price'].rolling(window=window_size).corr(gold_nasdaq['nasdaq_price'])

# print(gold_nasdaq_rolling_corr)

# `pandas.core.series.Series`의 타입에서는 인덱싱을 .iloc를 사용한다.
gold_corr_ls.append(round(gold_nasdaq_rolling_corr.iloc[-1], 4))
print(gold_corr_ls)
#####################################################################################

# 막대 그래프 그리기
import plotly.graph_objects as go

# 상관계수 값 설정

labels = ['USD', 'OIL', 'KOSPI', 'NASDAQ']

sorted_data = sorted(zip(gold_corr_ls, labels), reverse=True)

sorted_correlation_values = [item[0] for item in sorted_data]
sorted_labels = [item[1] for item in sorted_data]

# 정렬된 상관계수를 막대그래프로 그리기
fig = go.Figure(go.Bar(
    x=sorted_labels,
    y=sorted_correlation_values,
    text=[f'{value:.2f}' for value in sorted_correlation_values],
    textposition='auto',
    marker_color=['lightblue' if value >= 0 else 'lightcoral' for value in sorted_correlation_values]
))

# 그래프 제목 및 축 레이블 설정
fig.update_layout(
    title='GOLD vs. Assets Correlation',
    plot_bgcolor='white',
    yaxis=dict(title='Correlation'),
    xaxis=dict(title='Assets')
)

# 그래프 보이기
fig.write_html("GOLD vs. Assets Correlation.html")