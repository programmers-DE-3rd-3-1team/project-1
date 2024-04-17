import sqlite3
from matplotlib import pyplot as plt

# 데이터 연결해서 가져오기

con = sqlite3.connect("db.sqlite3")
Cur = con.cursor()

Cur.execute("select * from polls_exchangerate where cur_unit = 'USD' order by 4;") 

data = Cur.fetchall()
con.close()

price = []
date = []

for i in range(len(data)):
    # 가격 저장
    price.append(data[i][2])
    
    # 날짜 뒤에 시간 빼고 연도-월-일 으로 저장
    a = data[i][3]
    b = a.split(' ')
    date.append(b[0])

    
    
# print(date)
# # print(data)

# # 그래프 그리는 코드
# plt.figure(figsize=(8, 3))
# plt.plot(date, price, marker='o', linestyle='-')
# plt.title('USD price by date')
# plt.xticks(rotation=90)
# plt.xlabel('Date')
# plt.ylabel('USD Price')
# plt.grid(True)
# plt.show()

# 저장
# plt.savefig('my_plot.png')

# 그림 저장은 제가 일단 파일에 올려두었습니다 서버 화면에 올라가도록 설정은 해두었으나 디자인을 좀 변경할 필요가 있어보입니다. 


# 이 아래 주석은 반응형 그래프 적용 해보려고 하는 중 입니다!
import plotly.io as pio

pio.renderers.default = 'browser'
# fig = dict({ #plotly를 사용하는 첫번쨰 방법 - dict
#     "data": [{"type": "bar",
#               "x": [1,2,3,4,5],
#               "y": [5,4,3,2,1]}],
#     "layout": {"title": {"text": "딕셔너리로 그린 그래프"}} # 제목을 제시하려면?
# })
# pio.show(fig) #모아보여주기

# print(type(date[1]), type(price[1]))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


Daily_USD = pd.DataFrame({'price': price,
                            'date':date})
# print(Daily_USD)

# ImportError: Plotly express requires pandas to be installed. >> 오류 발생 시 pip install pandas
fig = px.line(Daily_USD,
              x="date",
              y="price",
              title='DaliY_USD')
# fig.show()
## 레이아웃 업데이트
fig.update_layout(
    plot_bgcolor='white',  # 배경색을 하얀색으로 설정
    title_font_size=24,    # 제목의 폰트 크기 설정
    xaxis=dict(title='Date', showgrid=True),  # x축 레이블 설정
    yaxis=dict(title='Price', showgrid=False),
)

# fig.update_layout(go.Layout(title={'text':'Title',
#                                    'font':{'color':'blue', 'size':40}}, # 타이틀
#                             xaxis={'title': {'text': 'X 축'}, # x축 라벨 추가, 그리드 숨김
#                                    'gridwidth':1, 'showgrid':False},
#                             yaxis={'title': {'text': 'Y 축'}, # y축 라벨 추가
#                                    'gridwidth':1}, # grid line style은 바꿀수 없다.
#                             legend ={'borderwidth':2, # 범례 테두리 두께
#                                      'bordercolor':'black', # 범례 테두리 색
#                                      'bgcolor':'#faf7af', # 범례 배경색
#                                      'font':{'color':'black'}, # 범례 글자 색}
#                                      paper_bgcolor='#7d7c7c', # 차트 바깥쪽 배경색
#                                      plot_bgcolor='#080808', # 차트 안쪽 배경색
#                                      font = {'color':'white'} # 전체 글자(폰트) 색상))


fig.write_html("Daily_USD.html")