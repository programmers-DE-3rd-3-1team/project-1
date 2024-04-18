import sqlite3
import pandas as pd

#####################################################################################
usd_corr_ls = []

# 달러 - 금 상관계수
# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.rate as USD_price, a.date, b.closing_price as gold_price
    FROM polls_exchangerate a
    INNER JOIN polls_goldprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
usd_gold = pd.DataFrame(data, columns=['USD_price', 'date', 'gold_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
usd_gold_rolling_corr = usd_gold['USD_price'].rolling(window=window_size).corr(usd_gold['gold_price'])

# print(usd_gold_rolling_corr)

# `pandas.core.series.Series`의 타입에서는 인덱싱을 .iloc를 사용한다.
usd_corr_ls.append(round(usd_gold_rolling_corr.iloc[-1], 4))
print(usd_corr_ls)
#############################################################################

# 달러-코스피 상관계수

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.rate as USD_price, a.date, b.closing_price as kospi_price
    FROM polls_exchangerate a
    INNER JOIN polls_kospi b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
usd_kospi = pd.DataFrame(data, columns=['USD_price', 'date', 'kospi_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
usd_kospi_rolling_corr = usd_kospi['USD_price'].rolling(window=window_size).corr(usd_kospi['kospi_price'])

# print(usd_kospi_rolling_corr)
usd_corr_ls.append(round(usd_kospi_rolling_corr.iloc[-1], 4))
#############################################################################

# 달러-나스닥 상관계수

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.rate as USD_price, a.date, b.index_price as nasdaq_price
    FROM polls_exchangerate a
    INNER JOIN polls_nasdaqindex b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
usd_nasdaq = pd.DataFrame(data, columns=['USD_price', 'date', 'nasdaq_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
usd_nasdaq_rolling_corr = usd_nasdaq['USD_price'].rolling(window=window_size).corr(usd_nasdaq['nasdaq_price'])

# print(usd_nasdaq_rolling_corr)
usd_corr_ls.append(round(usd_nasdaq_rolling_corr.iloc[-1], 4))
#############################################################################

# 달러-기름값 상관계수

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.rate as USD_price, a.date, b.closing_price as oil_price
    FROM polls_exchangerate a
    INNER JOIN polls_wtioilprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
usd_oil = pd.DataFrame(data, columns=['USD_price', 'date', 'oil_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
usd_oil_rolling_corr = usd_oil['USD_price'].rolling(window=window_size).corr(usd_oil['oil_price'])

# print(usd_oil_rolling_corr)
usd_corr_ls.append(round(usd_oil_rolling_corr.iloc[-1], 4))

print(usd_corr_ls)

################################################## 
# 막대 그래프 그리기
import plotly.graph_objects as go

# 상관계수 값 설정

labels = ['GOLD', 'KOSPI', 'NASDAQ', 'OIL']

sorted_data = sorted(zip(usd_corr_ls, labels), reverse=True)

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
    title='Dollar vs. Assets Correlation',
    plot_bgcolor='white',
    yaxis=dict(title='Correlation'),
    xaxis=dict(title='Assets')
)

# 그래프 보이기
fig.write_html("Dollar vs. Assets Correlation.html")