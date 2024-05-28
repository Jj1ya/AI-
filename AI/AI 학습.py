# 필요한 라이브러리 임포트
from pymongo import MongoClient
import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import numpy as np


# MongoDB 클라이언트 설정
client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
db = client['국제시장_분석데이터']

# 여러 컬렉션에서 데이터 로드
collections = ['미국_전처리된데이터', '베트남_전처리된데이터', '일본_전처리된데이터', '홍콩_전처리된데이터', '중국_전처리된데이터']  # 실제 컬렉션 이름으로 변경
data_frames = []

for collection_name in collections:
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    # 각 컬렉션의 데이터 프레임을 리스트에 추가
    data_frames.append(df)

# 여러 데이터 프레임을 하나로 합치기 (예: '년월'과 '수출_금액'을 기준으로)
combined_df = pd.concat(data_frames).groupby('년월')['수출_금액'].sum().reset_index()

combined_df['수출_금액'] = combined_df['수출_금액'].replace(0, np.nan)  # 먼저 0의 값을 NaN으로 변경
combined_df['수출_금액'].interpolate(inplace=True)  # 선형 보간 수행


# '년월'을 datetime 타입으로 변환하기 전에 형식을 맞추기
combined_df['년월'] = pd.to_datetime(combined_df['년월'], format='%Y년%m월')

# '년월'을 datetime 타입으로 변환
combined_df['년월'] = pd.to_datetime(combined_df['년월'])

# 시계열 데이터 설정
timeseries_data = combined_df.set_index('년월')['수출_금액']

# ARIMA 모델 학습
model = auto_arima(timeseries_data, seasonal=True, m=12)

# 예측 (여기서는 앞으로 12개월 예측)
forecast = model.predict(n_periods=12)

# 예측 결과 시각화
plt.figure(figsize=(10, 6))
plt.plot(timeseries_data.index, timeseries_data, label='Actual')
plt.plot(pd.date_range(timeseries_data.index[-1], periods=12, freq='M'), forecast, label='Forecast')
plt.title('Export Amount Forecast')
plt.xlabel('Year-Month')
plt.ylabel('Export Amount')
plt.legend()
plt.show()
