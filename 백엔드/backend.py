from flask import Flask, jsonify, request
from ai_recommendation import predict_market

app = Flask(__name__)

# 추천 국가 기능
@app.route('/recommend_country', methods=['POST'])
def recommend_country():
    try:
        # 입력된 품목을 가져옵니다.
        item = request.form['item']
        # AI 모델을 사용하여 추천 국가를 예측합니다.
        recommended_countries = predict_market(item, mode='country')
        return jsonify(recommended_countries)
    except Exception as e:
        return jsonify(error=str(e)), 400

# 추천 품목 기능
@app.route('/recommend_item', methods=['POST'])
def recommend_item():
    try:
        # 입력된 국가를 가져옵니다.
        country = request.form['country']
        # AI 모델을 사용하여 추천 품목을 예측합니다.
        recommended_items = predict_market(country, mode='item')
        return jsonify(recommended_items)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
