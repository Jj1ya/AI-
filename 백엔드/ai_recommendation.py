import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

# HS코드를 범주형으로 인코딩
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 모델 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("모델 정확도:", accuracy)

def predict_market(input_data):
    try:
        # NaN 값이 있는지 확인
        if np.any(np.isnan(input_data)):
            raise ValueError("입력 데이터에 NaN 값이 포함되어 있습니다.")
        
        # 2D 배열로 변환
        input_data = np.array(input_data).reshape(1, -1)
        
        # 예측
        prediction = model.predict(input_data)
        
        # 예측된 클래스를 다시 범주형으로 디코딩
        predicted_label = label_encoder.inverse_transform(prediction)
        
        return predicted_label.tolist()
    
    except Exception as e:
        return str(e)
