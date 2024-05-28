import pandas as pd
from pymongo import MongoClient

# MongoDB 연결
client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
db = client['국제시장_분석데이터']
collection = db['국가별 수출입 통계']

# 필드 선택
fields = {'_id': 0}

# MongoDB에서 데이터 불러오기
cursor = collection.find({}, fields)
data = list(cursor)

# 데이터프레임 생성
df = pd.DataFrame(data)

# 열 이름 설정
new_columns = df.iloc[1]  # 두 번째 행을 열 이름으로 설정
df = df[2:]  # 첫 번째와 두 번째 행 제거
df.columns = new_columns  # 열 이름 설정

# 필요 없는 열과 행 제거
df = df.dropna(how='all', axis=1)  # 모든 값이 NaN인 열 제거
df = df.dropna(how='all', axis=0)  # 모든 값이 NaN인 행 제거

# 열 이름을 적절하게 변경
df.columns = ['순번', '국가명', '수출금액_2023', '수출증감률_2023', '수입금액_2023','수입증감률_2023', '수지_2023', '수출금액_2024', '수출증감률_2024', '수입금액_2024', '수입증감률_2024', '수지_2024'][:len(df.columns)]

# 필요없는 열 제거 (기타_로 시작하는 열 제거)
df = df[['순번', '국가명', '수출금액_2023', '수출증감률_2023', '수입금액_2023', '수입증감률_2023', '수지_2023', '수출금액_2024', '수출증감률_2024', '수입금액_2024', '수입증감률_2024', '수지_2024']]

# 데이터 타입 변환
df['수출금액_2023'] = pd.to_numeric(df['수출금액_2023'], errors='coerce')
df['수출증감률_2023'] = pd.to_numeric(df['수출증감률_2023'], errors='coerce')
df['수입금액_2023'] = pd.to_numeric(df['수입금액_2023'], errors='coerce')
df['수입증감률_2023'] = pd.to_numeric(df['수입금액_2024'], errors='coerce')
df['수지_2023'] = pd.to_numeric(df['수입금액_2024'], errors='coerce')
df['수출금액_2024'] = pd.to_numeric(df['수출금액_2024'], errors='coerce')
df['수출증감률_2024'] = pd.to_numeric(df['수출증감률_2024'], errors='coerce')
df['수입금액_2024'] = pd.to_numeric(df['수입금액_2024'], errors='coerce')
df['수입증감률_2024'] = pd.to_numeric(df['수입금액_2024'], errors='coerce')
df['수지_2024'] = pd.to_numeric(df['수입금액_2024'], errors='coerce')

# MongoDB에 데이터 저장
collection_preprocessed = db['국가별 수출입 통계_전처리된데이터']
collection_preprocessed.insert_many(df.to_dict('records'))

print("전처리된 데이터를 몽고DB에 저장하였습니다.")

# 데이터프레임의 열 이름과 일부 데이터 출력
print(df.columns)
print(df.head())
