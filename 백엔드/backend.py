from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, InternalServerError
from AI import predict_market
import logging
import os

app = Flask("졸업작품")
CORS(app)

# 로깅 설정
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 추천 국가 기능
@app.route('/recommend_country', methods=['POST'])
def recommend_country():
    item = request.form.get('item')
    if not item:
        logging.error('품목을 입력하지 않았습니다.')
        return jsonify({'error': '품목을 입력해주세요.'}), 400
    try:
        recommended_countries = predict_market(item, mode='country')
        return jsonify(recommended_countries)
    except Exception as e:
        logging.error(f'추천 국가 기능 중 오류 발생: {str(e)}')
        return jsonify({'error': '서버 오류가 발생했습니다.'}), 500

# 추천 품목 기능
@app.route('/recommend_item', methods=['POST'])
def recommend_item():
    country = request.form.get('country')
    if not country:
        logging.error('국가를 입력하지 않았습니다.')
        return jsonify({'error': '국가를 입력해주세요.'}), 400
    try:
        recommended_items = predict_market(country, mode='item')
        return jsonify(recommended_items)
    except Exception as e:
        logging.error(f'추천 품목 기능 중 오류 발생: {str(e)}')
        return jsonify({'error': '서버 오류가 발생했습니다.'}), 500

# 실행
if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_ENV') == 'development',
        host='127.0.0.1',
        port=5000
    )
