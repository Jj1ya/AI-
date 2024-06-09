import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from gensim.models import FastText

# MongoDB 클라이언트 설정
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['export_recommendation']
trade_collection = db['TradeStatistics']

# 데이터 가져오기
data = list(trade_collection.find({}, {'statCdCntnKor1': 0}))
df_trade = pd.DataFrame(data)

# 데이터 전처리
df_trade = df_trade[['balPayments', 'expDlr', 'expWgt', 'hsCd', 'impDlr', 'impWgt', 'statCd', 'statKor', 'year']]
df_trade['balPayments'] = df_trade['balPayments'].astype(float)
df_trade['expDlr'] = df_trade['expDlr'].astype(float)
df_trade['expWgt'] = df_trade['expWgt'].astype(float)
df_trade['impDlr'] = df_trade['impDlr'].astype(float)
df_trade['impWgt'] = df_trade['impWgt'].astype(float)
df_trade['year'] = df_trade['year'].astype(str)

# 단어 임베딩 모델 학습
statCd_corpus = df_trade['statCd'].tolist()
statKor_corpus = df_trade['statKor'].tolist()
fasttext_model = FastText(statCd_corpus + statKor_corpus, min_count=1, vector_size=100, window=5, workers=4)

# 데이터 분석 및 모델링
X = df_trade[['balPayments', 'expDlr', 'expWgt', 'impDlr', 'impWgt']]
y = df_trade['hsCd']
model = RandomForestRegressor()

# 모델 학습
model.fit(X, y)
predictions = model.predict(X)

# 결과 확인
print(predictions)
