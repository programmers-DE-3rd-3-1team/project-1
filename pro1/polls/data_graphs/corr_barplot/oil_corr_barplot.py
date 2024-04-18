import sqlite3
import pandas as pd
import plotly.express as px

#####################################################################################
oil_corr_ls = []

# 기름값-달러 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as oil_price, a.date, b.rate as USD_price
    FROM polls_wtioilprice a
    INNER JOIN polls_exchangerate b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
oil_usd = pd.DataFrame(data, columns=['oil_price', 'date', 'USD_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
oil_usd_rolling_corr = oil_usd['oil_price'].rolling(window=window_size).corr(oil_usd['USD_price'])

# print(oil_usd_rolling_corr)
oil_corr_ls.append(round(oil_usd_rolling_corr.iloc[-1], 4))

# print(oil_corr_ls)

#####################################################################################
# 기름값 - 코스피 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as oil_price, a.date, b.closing_price as kospi_price
    FROM polls_wtioilprice a
    INNER JOIN polls_kospi b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
oil_kospi = pd.DataFrame(data, columns=['oil_price', 'date', 'kospi_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
oil_kospi_rolling_corr = oil_kospi['oil_price'].rolling(window=window_size).corr(oil_kospi['kospi_price'])

# print(oil_kospi_rolling_corr)
oil_corr_ls.append(round(oil_kospi_rolling_corr.iloc[-1], 4))

# print(oil_corr_ls)
#####################################################################################

# 기름값 - 나스닥 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as oil_price, a.date, b.index_price as nasdaq_price
    FROM polls_wtioilprice a
    INNER JOIN polls_nasdaqindex b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
oil_nasdaq = pd.DataFrame(data, columns=['oil_price', 'date', 'nasdaq_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
oil_nasdaq_rolling_corr = oil_nasdaq['oil_price'].rolling(window=window_size).corr(oil_nasdaq['nasdaq_price'])

# print(oil_nasdaq_rolling_corr)
oil_corr_ls.append(round(oil_nasdaq_rolling_corr.iloc[-1], 4))

# print(oil_corr_ls)

#####################################################################################

# 기름값 - 금 상관계수
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("""
    SELECT a.closing_price as oil_price, a.date, b.closing_price as gold_price
    FROM polls_wtioilprice a
    INNER JOIN polls_goldprice b ON a.date = b.date
    ORDER BY a.date;
""")
 
data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
oil_gold = pd.DataFrame(data, columns=['oil_price', 'date', 'gold_price'])

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
oil_gold_rolling_corr = oil_gold['oil_price'].rolling(window=window_size).corr(oil_gold['gold_price'])

# print(oil_gold_rolling_corr)
oil_corr_ls.append(round(oil_gold_rolling_corr.iloc[-1], 4))

print(oil_corr_ls)

################################################## 
# 막대 그래프 그리기
import plotly.graph_objects as go

# 상관계수 값 설정

labels = ['USD', 'KOSPI', 'NASDAQ', 'GOLD']

sorted_data = sorted(zip(oil_corr_ls, labels), reverse=True)

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
    title='Oil vs. Assets Correlation',
    plot_bgcolor='white',
    yaxis=dict(title='Correlation'),
    xaxis=dict(title='Assets')
)

# 그래프 보이기
fig.write_html("Oil vs. Assets Correlation.html")