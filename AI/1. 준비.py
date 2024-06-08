import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# MongoDB에서 데이터 불러오기
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['export_recommendation']
collection = db['TradeStatistics']
data = pd.DataFrame(list(collection.find()))

# 데이터 필터링 및 타입 변환
data = data[['year', 'balPayments', 'expDlr', 'expWgt', 'hsCd', 'impDlr', 'impWgt', 'statCd', 'statCdCntnKor1', 'statKor']]
data['year'] = pd.to_datetime(data['year'], format='%Y.%m')
numeric_columns = ['balPayments', 'expDlr', 'expWgt', 'hsCd', 'impDlr', 'impWgt']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
data = data.fillna(method='ffill')

# 텍스트 데이터 변환을 위한 함수
def transform_text_columns(df, text_columns):
    for column in text_columns:
        # 특정 단어를 명시적으로 포함하기 위해 stop_words를 사용하지 않음
        tfidf = TfidfVectorizer(max_features= 5572)  # stop_words='english' 제거
        tfidf_result = tfidf.fit_transform(df[column].astype('U')).toarray()
        tfidf_df = pd.DataFrame(tfidf_result, columns=[f"tfidf_{column}_{feature}" for feature in tfidf.get_feature_names_out()])
        tfidf_df.index = df.index
        df = pd.concat([df, tfidf_df], axis=1, copy=False).drop(column, axis=1)
    return df

# 변환할 텍스트 컬럼들
text_columns = ['statCd', 'statCdCntnKor1', 'statKor']

# 텍스트 데이터 변환
data = transform_text_columns(data, text_columns)

# 데이터 확인
print(data.head())
