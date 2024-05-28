import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd

# 몽고DB 클라이언트 설정
client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
db = client['국제시장_분석데이터']  # 실제 데이터베이스 이름으로 변경

# '미국_전처리된데이터' 컬렉션에서 데이터 가져오기
collection = db['미국_전처리된데이터']
data = list(collection.find())

# 데이터를 pandas DataFrame으로 변환
df = pd.DataFrame(data)

# '년월'로 그룹화하고 '수출_금액'을 합계
# 여기서는 '년월' 컬럼에서 연도만 추출하여 그룹화하기 위해 추가적인 처리가 필요합니다.
# '년월'에서 연도만 추출
df['년'] = df['년월'].apply(lambda x: x[:4])

# 연도별 '수출_금액' 합계
yearly_sales = df.groupby('년')['수출_금액'].sum().reset_index()

# 년도별 수출 금액 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(yearly_sales['년'], yearly_sales['수출_금액'], marker='o')
plt.title('년도별 수출 금액')
plt.xlabel('년도')
plt.ylabel('수출 금액')
plt.grid(True)
plt.xticks(rotation=45)  # x축 레이블 회전
plt.show()
