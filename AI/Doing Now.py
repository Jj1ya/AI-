import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['export_recommendation']
trade_collection = db['TradeStatistics']

# 데이터 가져오기
data = list(trade_collection.find({}, {'_id': 0}))  # _id 필드는 가져오지 않음
df_trade = pd.DataFrame(data)

# 데이터 전처리
df_trade.dropna(inplace=True)  # 결측치 제거

# 특성과 타겟 데이터 나누기
X = df_trade[['balPayments', 'expDlr', 'expWgt', 'impDlr', 'impWgt']]
y = df_trade['hsCd']

# 모델 학습
model = RandomForestRegressor()
model.fit(X, y)

def predict_market(input_data):
    try:
        # NaN 값이 있는지 확인
        if np.any(np.isnan(input_data)):
            raise ValueError("입력 데이터에 NaN 값이 포함되어 있습니다.")
        
        # 2D 배열로 변환
        input_data = np.array(input_data).reshape(1, -1)
        
        # 예측
        predictions = model.predict(input_data)
        
        # 예측 값을 정수형으로 변환
        predictions = predictions.astype(int)
        
        # 추천 결과 반환
        return predictions.tolist()
    
    except Exception as e:
        return str(e)
