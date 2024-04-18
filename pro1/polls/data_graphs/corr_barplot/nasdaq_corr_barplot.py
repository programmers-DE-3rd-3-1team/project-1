import sqlite3
import pandas as pd
import plotly.express as px
#####################################################################################

nasdaq_corr_ls = []

# 나스닥 - 달러 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.index_price as nasdaq_price, a.date, b.rate as USD_price
    FROM polls_nasdaqindex a
    INNER JOIN polls_exchangerate b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
nasdaq_usd = pd.DataFrame(data, columns=['nasdaq_price', 'date', 'USD_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
nasdaq_usd_rolling_corr = nasdaq_usd['nasdaq_price'].rolling(window=window_size).corr(nasdaq_usd['USD_price'])

# print(nasdaq_usd_rolling_corr)
nasdaq_corr_ls.append(round(nasdaq_usd_rolling_corr.iloc[-1], 4))
# print(nasdaq_corr_ls)
#####################################################################################

# 나스닥 - 기름값 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.index_price as nasdaq_price, a.date, b.closing_price as oil_price
    FROM polls_nasdaqindex a
    INNER JOIN polls_wtioilprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
nasdaq_oil = pd.DataFrame(data, columns=['nasdaq_price', 'date', 'oil_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
nasdaq_oil_rolling_corr = nasdaq_oil['nasdaq_price'].rolling(window=window_size).corr(nasdaq_oil['oil_price'])

# print(nasdaq_oil_rolling_corr)
nasdaq_corr_ls.append(round(nasdaq_oil_rolling_corr.iloc[-1], 4))
print(nasdaq_corr_ls)
#####################################################################################

# 나스닥 - 코스피 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.index_price as nasdaq_price, a.date, b.closing_price as kospi_price
    FROM polls_nasdaqindex a
    INNER JOIN polls_kospi b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
nasdaq_kospi = pd.DataFrame(data, columns=['nasdaq_price', 'date', 'kospi_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
nasdaq_kospi_rolling_corr = nasdaq_kospi['nasdaq_price'].rolling(window=window_size).corr(nasdaq_kospi['kospi_price'])

# print(nasdaq_kospi_rolling_corr)
nasdaq_corr_ls.append(round(nasdaq_kospi_rolling_corr.iloc[-1], 4))
print(nasdaq_corr_ls)
#####################################################################################

# 나스닥 - 금값 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.index_price as nasdaq_price, a.date, b.closing_price as gold_price
    FROM polls_nasdaqindex a
    INNER JOIN polls_goldprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
nasdaq_gold = pd.DataFrame(data, columns=['nasdaq_price', 'date', 'gold_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
nasdaq_gold_rolling_corr = nasdaq_gold['nasdaq_price'].rolling(window=window_size).corr(nasdaq_gold['gold_price'])

# print(nasdaq_gold_rolling_corr)
nasdaq_corr_ls.append(round(nasdaq_gold_rolling_corr.iloc[-1], 4))
print(nasdaq_corr_ls)
#####################################################################################

# 막대 그래프 그리기
import plotly.graph_objects as go

# 상관계수 값 설정

labels = ['USD', 'OIL', 'KOSPI', 'GOLD']

sorted_data = sorted(zip(nasdaq_corr_ls, labels), reverse=True)

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
    title='NASDAQ vs. Assets Correlation',
    plot_bgcolor='white',
    yaxis=dict(title='Correlation'),
    xaxis=dict(title='Assets')
)

# 그래프 보이기
fig.write_html("NASDAQ vs. Assets Correlation.html")