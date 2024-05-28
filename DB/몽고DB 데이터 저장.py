import pandas as pd
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/국제시장_분석데이터")

# 데이터베이스와 컬렉션 선택
db = client["국제시장_분석데이터"]
collection = db["클러스터0"]

# 엑셀 파일 읽기
df = pd.read_excel("C:/Users/user/Desktop/일본.xlsx")


# 데이터프레임을 딕셔너리 리스트로 변환
data = df.to_dict(orient="records")

# 데이터 삽입
collection.insert_many(data)

print("데이터가 성공적으로 MongoDB에 저장되었습니다.")
