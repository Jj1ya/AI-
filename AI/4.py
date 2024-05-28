import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import pickle

# 데이터 로드 함수
def load_data(국제시장_분석데이터):
    client = MongoClient('mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/')
    db = client[국제시장_분석데이터]
    collections = db.list_collection_names()

    all_data = []
    for collection_name in collections:
        collection = db[collection_name]
        fields = {'_id': 0}
        cursor = collection.find({}, fields)
        data = list(cursor)
        all_data.extend(data)

    df = pd.DataFrame(all_data)
    return df



# 데이터 전처리 함수
def preprocess_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df

# 모델 훈련 함수
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    return model

# 메인 실행 부분
if __name__ == "__main__":
    # 1. 데이터 로드
    df = load_data("국제시장_분석데이터")
    print(df.columns)  # 데이터프레임의 열 이름 출력

    # 2. 데이터 전처리
    df = preprocess_data(df)


    # 3. 특징과 타겟 설정
    X = df[['수출_금액']]
    y = df['수입_금액']

    # 4. 모델 훈련
    model = train_model(X, y)

    print("모델 훈련 완료 및 저장되었습니다.")
