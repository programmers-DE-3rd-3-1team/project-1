# from .USD import date, price
import pandas as pd
import plotly.express as px

# 예시 데이터 생성
date = pd.date_range(start='2024-01-01', end='2024-01-05')
price = [100, 110, 105, 108, 102]
print(date)

# 데이터프레임 생성
# Daily_USD = pd.DataFrame({'date': date, 'price': price})

# # 꺾은선 그래프 그리기
# fig = px.line(Daily_USD, x='date', y='price', title='Price over Time')
# # fig.show()
# # fig.write_image("price_over_time.png")
# fig.write_html("test.html")