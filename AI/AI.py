import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from gensim.models import FastText
import numpy as np

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

# 결측치 및 무한대 값 처리
df_trade.replace([np.inf, -np.inf], np.nan, inplace=True)
df_trade.dropna(inplace=True)

# 단어 임베딩 모델 학습
statCd_corpus = df_trade['statCd'].tolist()
statKor_corpus = df_trade['statKor'].tolist()
fasttext_model = FastText(statCd_corpus + statKor_corpus, min_count=1, vector_size=100, window=5, workers=4)

# 데이터 분석 및 모델링
X = df_trade[['balPayments', 'expDlr', 'expWgt', 'impDlr', 'impWgt']]
y = df_trade['hsCd']
model = RandomForestRegressor()
model.fit(X, y)

# 사용자 입력 받기
user_input = input("국가 코드 또는 HS코드를 입력해주세요: ")

# 입력 데이터 기반 예측
try:
    if user_input.isdigit():  # HS코드인 경우
        hs_code = int(user_input)
        input_data = df_trade[df_trade['hsCd'] == hs_code][['balPayments', 'expDlr', 'expWgt', 'impDlr', 'impWgt']].mean().values
    else:  # 국가 코드인 경우
        country_code = user_input
        input_data = df_trade[df_trade['statCd'] == country_code][['balPayments', 'expDlr', 'expWgt', 'impDlr', 'impWgt']].mean().values
    
    # NaN 값이 있는지 확인
    if np.any(np.isnan(input_data)):
        raise ValueError("입력 데이터에 NaN 값이 포함되어 있습니다.")
    
    # 2D 배열로 변환
    input_data = np.array(input_data).reshape(1, -1)
    
    # 예측
    predictions = model.predict(input_data)
    
    # 예측 값을 정수형으로 변환
    predictions = predictions.astype(int)
    
    # 추천 결과 출력
    print(f"입력하신 {user_input}에 대한 추천 결과는 다음과 같습니다:")
    for i, pred in enumerate(predictions[:5]):  # 상위 5개의 예측 결과를 추천
        hs_code = int(pred)
        avg_exp_dlr = df_trade[df_trade['hsCd'] == hs_code]['expDlr'].mean()
        avg_exp_wgt = df_trade[df_trade['hsCd'] == hs_code]['expWgt'].mean()
        print(f"{i+1}. HS코드 {hs_code}")
        print("- 추천 이유: 해당 HS코드 제품의 수출 잠재력이 높습니다.")
        if not np.isnan(avg_exp_dlr) and not np.isnan(avg_exp_wgt):
            print(f"- 관련 통계: 최근 3년간 평균 수출액 {avg_exp_dlr}, 평균 수출량 {avg_exp_wgt}")
        else:
            print("- 관련 통계: 해당 HS코드에 대한 충분한 데이터가 없습니다.")
        print()
except Exception as e:
    print(f"오류 발생: {e}")
