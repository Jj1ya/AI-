import pymongo
import pandas as pd
from pymongo import MongoClient

# MongoDB 클라이언트 연결
client = pymongo.MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')

# 데이터베이스 선택
db = client["your_database"]

# 모든 컬렉션 이름을 리스트로 저장
collection_names = [f"collection{i+1}" for i in range(17)]

# 모든 컬렉션 데이터를 저장할 딕셔너리
dataframes = {}

# 반복문을 통해 각 컬렉션의 데이터를 가져와서 데이터프레임으로 변환
for name in collection_names:
    collection = db[name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    dataframes[name] = df

# 예시로 첫 번째 두 컬렉션의 'user_id'로 결합 (필요에 따라 다른 컬렉션도 결합)
df_combined = dataframes[collection_names[0]]
for name in collection_names[1:]:
    df_combined = pd.merge(df_combined, dataframes[name], on="user_id", how="inner")

# 결합된 데이터프레임 확인
print("Combined DataFrame:")
print(df_combined.head())
