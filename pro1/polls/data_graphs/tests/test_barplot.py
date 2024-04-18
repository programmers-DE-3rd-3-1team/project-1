import plotly.graph_objects as go

# 상관계수 값 설정
correlation_values = [0.6, 0.4, -0.7, 0.1]
labels = ['Correlation 1', 'Correlation 2', 'Correlation 3', 'Correlation 4']

# 상관계수를 막대그래프로 그리기
fig = go.Figure(go.Bar(
    x=labels,
    y=correlation_values,
    text=[f'{value:.2f}' for value in correlation_values],
    textposition='auto',
    marker_color=['lightblue' if value >= 0 else 'lightcoral' for value in correlation_values]
))

# 그래프 제목 및 축 레이블 설정
fig.update_layout(
    title='Correlation Coefficients',
    yaxis=dict(title='Value'),
    xaxis=dict(title='Correlation')
)

# 그래프 보이기
fig.write_html("test.html")