import sqlite3
import pandas as pd
import plotly.express as px
#####################################################################################

kospi_corr_ls = []

# 코스피 - 달러 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as kospi_price, a.date, b.rate as USD_price
    FROM polls_kospi a
    INNER JOIN polls_exchangerate b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
kospi_usd = pd.DataFrame(data, columns=['kospi_price', 'date', 'USD_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
kospi_usd_rolling_corr = kospi_usd['kospi_price'].rolling(window=window_size).corr(kospi_usd['USD_price'])

# print(kospi_usd_rolling_corr)
kospi_corr_ls.append(round(kospi_usd_rolling_corr.iloc[-1], 4))
#####################################################################################

# 코스피 - 금 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as kospi_price, a.date, b.closing_price as gold_price
    FROM polls_kospi a
    INNER JOIN polls_goldprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
kospi_gold = pd.DataFrame(data, columns=['kospi_price', 'date', 'gold_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
kospi_gold_rolling_corr = kospi_gold['kospi_price'].rolling(window=window_size).corr(kospi_gold['gold_price'])

# print(kospi_gold_rolling_corr)
kospi_corr_ls.append(round(kospi_gold_rolling_corr.iloc[-1], 4))
#####################################################################################

# 코스피 - 나스닥 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as kospi_price, a.date, b.index_price as nasdaq_price
    FROM polls_kospi a
    INNER JOIN polls_nasdaqindex b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
kospi_nasdaq = pd.DataFrame(data, columns=['kospi_price', 'date', 'nasdaq_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
kospi_nasdaq_rolling_corr = kospi_nasdaq['kospi_price'].rolling(window=window_size).corr(kospi_nasdaq['nasdaq_price'])

# print(kospi_nasdaq_rolling_corr)
kospi_corr_ls.append(round(kospi_nasdaq_rolling_corr.iloc[-1], 4))
#####################################################################################

# 코스피 - 기름값 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as kospi_price, a.date, b.closing_price as oil_price
    FROM polls_kospi a
    INNER JOIN polls_wtioilprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
kospi_oil = pd.DataFrame(data, columns=['kospi_price', 'date', 'oil_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
kospi_oil_rolling_corr = kospi_oil['kospi_price'].rolling(window=window_size).corr(kospi_oil['oil_price'])

# print(kospi_oil_rolling_corr)
kospi_corr_ls.append(round(kospi_oil_rolling_corr.iloc[-1], 4))
print(kospi_corr_ls)

################################################## 
# 막대 그래프 그리기
import plotly.graph_objects as go

# 상관계수 값 설정

labels = ['USD', 'GOLD', 'NASDAQ', 'OIL']

sorted_data = sorted(zip(kospi_corr_ls, labels), reverse=True)

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
    title='KOSPI vs. Assets Correlation',
    plot_bgcolor='white',
    yaxis=dict(title='Correlation'),
    xaxis=dict(title='Assets')
)

# 그래프 보이기
fig.write_html("KOSPI vs. Assets Correlation.html")