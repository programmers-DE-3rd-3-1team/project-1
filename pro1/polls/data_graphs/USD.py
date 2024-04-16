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

# 그래프 그리는 코드
plt.figure(figsize=(8, 3))
plt.plot(date, price, marker='o', linestyle='-')
plt.title('USD price by date')
plt.xticks(rotation=90)
plt.xlabel('Date')
plt.ylabel('USD Price')
plt.grid(True)
plt.show()

# 저장
# plt.savefig('my_plot.png')

# 그림 저장은 제가 일단 파일에 올려두었습니다 서버 화면에 올라가도록 설정은 해두었으나 디자인을 좀 변경할 필요가 있어보입니다. 
