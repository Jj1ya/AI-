import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

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
def recommend_export_markets(hs_code):
    # HS코드에 해당하는 데이터 필터링
    hs_data = df_trade[df_trade['hsCd'] == hs_code]
    
    # 수출 실적이 높은 국가 추출
    top_export_countries = hs_data.sort_values('expDlr', ascending=False)['statCd'].unique()[:5]
    
    # 추천 결과 생성
    recommendations = []
    for country in top_export_countries:
        country_data = hs_data[hs_data['statCd'] == country]
        recommendation = {
            'country': country,
            'export_value': country_data['expDlr'].values[0],
            'export_weight': country_data['expWgt'].values[0],
            'export_growth_rate': (country_data['expDlr'].values[0] - country_data['impDlr'].values[0]) / country_data['impDlr'].values[0] * 100
        }
        recommendations.append(recommendation)
    
    return recommendations

# 국가 코드 기반 수출 품목 추천 모델
def recommend_export_products(country_code):
    # 국가 코드에 해당하는 데이터 필터링
    country_data = df_trade[df_trade['statCd'] == country_code]
    
    # 수출 실적이 높은 HS코드 품목 추출
    top_export_products = country_data.sort_values('expDlr', ascending=False)['hsCd'].unique()[:5]
    
    # 추천 결과 생성
    recommendations = []
    for hs_code in top_export_products:
        product_data = country_data[country_data['hsCd'] == hs_code]
        recommendation = {
            'hs_code': hs_code,
            'export_value': product_data['expDlr'].values[0],
            'export_weight': product_data['expWgt'].values[0],
            'export_growth_rate': (product_data['expDlr'].values[0] - product_data['impDlr'].values[0]) / product_data['impDlr'].values[0] * 100
        }
        recommendations.append(recommendation)
    
    return recommendations

# 사용자 입력 받기
hs_code = input("HS코드를 입력하세요: ")
country_code = input("국가 코드를 입력하세요: ")

# 추천 결과 출력
print("HS코드 기반 수출 추천 결과:")
print(recommend_export_markets(hs_code))
print("국가 코드 기반 수출 품목 추천 결과:")
print(recommend_export_products(country_code))
