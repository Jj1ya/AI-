import pandas as pd
from pymongo import MongoClient

# MongoDB 연결
client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
db = client['국제시장_분석데이터']
collection = db['홍콩']

# 필드 선택
fields = {'_id': 0}

# 몽고DB에서 데이터 불러오기
cursor = collection.find({}, fields)  # 모든 필드 선택하여 데이터 가져오기
data = list(cursor)  # 가져온 문서들을 리스트로 변환

# 첫 번째와 두 번째 행 제거
data = data[2:]

# 데이터프레임 생성
df = pd.DataFrame(data)

# 열 이름 설정
new_columns = df.iloc[0]  # 첫 번째 행을 열 이름으로 설정
df = df[1:]  # 첫 번째 행 제거
# 실제 데이터에 맞는 열 이름으로 수정
df.columns = new_columns  

# 열 이름 수정
df.columns = ['년월', '수출_금액', '수출_증감률', '수출_중량', '수출_중량_증감률', '수입_금액', '수입_증감률', '수입_중량', '수입_중량_증감률', '수지']

# '수지' 열 추가
df['수지'] = df['수출_금액'] - df['수입_금액']

# MongoDB에 데이터 저장
collection_preprocessed = db['홍콩_전처리된데이터']
collection_preprocessed.insert_many(df.to_dict('records'))

print("전처리된 데이터를 몽고DB에 저장하였습니다.")

# 데이터프레임의 열 이름과 일부 데이터 출력
print(df.columns)
print(df.head())
