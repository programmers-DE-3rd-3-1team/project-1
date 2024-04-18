import sqlite3
import pandas as pd
import plotly.express as px

# 데이터 연결해서 가져오기
con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

# 서로 데이터가 존재하는 날짜만 매핑하여 추출
Cur.execute("""
    SELECT a.index_price AS nasdaq_price, a.date, b.rate AS usd_price
    FROM polls_nasdaqindex a
    INNER JOIN polls_exchangerate b ON a.date = b.date
    ORDER BY a.date;
""")

data = Cur.fetchall()
con.close()

# 데이터프레임 형식으로 저장
gold_kospi = pd.DataFrame(data, columns=['nasdaq_price', 'date', 'usd_price'])

# 상관계수 출력 (전체 기간)
print(gold_kospi[['nasdaq_price', 'usd_price']].corr(method='pearson'))

# 시간에 따른 상관계수 계산 (롤링 윈도우 사용)
window_size = 60  # 예: 30일 윈도우
rolling_corr = gold_kospi['nasdaq_price'].rolling(window=window_size).corr(gold_kospi['usd_price'])

# 롤링 상관계수 그래프
fig = px.line(x=gold_kospi['date'], y=rolling_corr, title='Rolling Correlation: NASDAQ vs USD')
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Rolling Correlation Coefficient')
fig.update_layout(plot_bgcolor='white')

fig.write_html("nasdaq_usd.html")