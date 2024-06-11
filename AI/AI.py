import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import re

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['export_recommendation']
trade_collection = db['TradeStatistics']

# 데이터 가져오기
data = list(trade_collection.find({}, {'_id': 0}))  # _id 필드는 가져오지 않음
df_trade = pd.DataFrame(data)

# 데이터 전처리
df_trade.dropna(inplace=True)  # 결측치 제거
df_trade['expDlr'] = df_trade['expDlr'].astype(float)
df_trade['impDlr'] = df_trade['impDlr'].astype(float)

# HS코드 기반 수출 추천 모델
def recommend_export_markets(hs_code, sort_by='export_value', reverse=True, top_n=5):
    # HS코드에 해당하는 데이터 필터링
    hs_data = df_trade[df_trade['hsCd'] == hs_code]
    
    # 수출 실적이 높은 국가 추출
    recommendations = []
    for country in hs_data['statCd'].unique():
        country_data = hs_data[hs_data['statCd'] == country]
        recommendation = {
            'country': country,
            'export_value': country_data['expDlr'].values[0],
            'export_weight': country_data['expWgt'].values[0],
            'export_growth_rate': (country_data['expDlr'].values[0] - country_data['impDlr'].values[0]) / country_data['impDlr'].values[0] * 100
        }
        recommendations.append(recommendation)
    
    # 추천 결과 정렬 및 필터링
    recommendations = sorted(recommendations, key=lambda x: x[sort_by], reverse=reverse)
    return recommendations[:top_n]

# 국가 코드 기반 수출 품목 추천 모델
def recommend_export_products(country_code, sort_by='export_value', reverse=True, top_n=5):
    # 국가 코드에 해당하는 데이터 필터링
    country_data = df_trade[df_trade['statCd'] == country_code]
    
    # 수출 실적이 높은 HS코드 품목 추출
    recommendations = []
    for hs_code in country_data['hsCd'].unique():
        product_data = country_data[country_data['hsCd'] == hs_code]
        recommendation = {
            'hs_code': hs_code,
            'export_value': product_data['expDlr'].values[0],
            'export_weight': product_data['expWgt'].values[0],
            'export_growth_rate': (product_data['expDlr'].values[0] - product_data['impDlr'].values[0]) / product_data['impDlr'].values[0] * 100
        }
        recommendations.append(recommendation)
    
    # 추천 결과 정렬 및 필터링
    recommendations = sorted(recommendations, key=lambda x: x[sort_by], reverse=reverse)
    return recommendations[:top_n]

# 예측 함수 추가
def predict_export_value(hs_code, country_code):
    X = df_trade[['hsCd', 'statCd']]
    y = df_trade['expDlr']
    
    # 훈련/테스트 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 랜덤 포레스트 회귀 모델 학습
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 예측
    X_new = pd.DataFrame({'hsCd': [hs_code], 'statCd': [country_code]})
    return model.predict(X_new)[0]

# 사용자 입력 검증
def validate_hs_code(hs_code):
    if not re.match(r'^\d{6}$', hs_code):
        return False
    return True

def validate_country_code(country_code):
    if not re.match(r'^[A-Z]{3}$', country_code):
        return False
    return True

# 사용자 입력 받기
hs_code = input("HS코드를 입력하세요: ")
country_code = input("국가 코드를 입력하세요: ")

# 입력 값 검증
if not validate_hs_code(hs_code):
    print("잘못된 HS코드 형식입니다.")
elif not validate_country_code(country_code):
    print("잘못된 국가 코드 형식입니다.")
else:
    # 추천 결과 출력
    print("HS코드 기반 수출 추천 결과:")
    print(recommend_export_markets(hs_code))
    print("국가 코드 기반 수출 품목 추천 결과:")
    print(recommend_export_products(country_code))
    
    # 수출 금액 예측
    predicted_export_value = predict_export_value(hs_code, country_code)
    print(f"예측 수출 금액: {predicted_export_value:.2f}")
