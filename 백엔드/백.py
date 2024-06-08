from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB 클라이언트 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['economic_data']
collection = db['economicIndicators']

@app.route('/api/economic-data/<country>', methods=['GET'])
def get_economic_data(country):
    data = collection.find_one({"country": country})
    if data:
        data.pop('_id')  # MongoDB의 ObjectId는 JSON 직렬화 불가하므로 제거
        return jsonify(data)
    else:
        return jsonify({"error": "Data not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
