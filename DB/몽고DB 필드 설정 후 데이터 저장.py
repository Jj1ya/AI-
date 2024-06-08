from pymongo import MongoClient
import requests
import xml.etree.ElementTree as ET

# MongoDB에 연결
client = MongoClient("mongodb+srv://ltfc83:Chlwldnd1220@cluster0.lp68icz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['export_recommendation']
collection = db['TradeStatistics']

# API 호출 및 데이터 가져오기
url = 'https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList?serviceKey=6mxlnmF2RW8P0hqL52XMnCQ3LxEjCv5lUeischYP8jDaV1f3DL4J4xQ5HC%2BfupUDW7tiHADCftmhbL8gi2bjnQ%3D%3D&strtYymm=202208&endYymm=202212&cntyCD=TW'
response = requests.get(url)
root = ET.fromstring(response.content)

# 데이터를 저장할 스키마 정의
def parse_item(item):
    return {
        "balPayments": item.find('balPayments').text,
        "expDlr": item.find('expDlr').text,
        "expWgt": item.find('expWgt').text,
        "hsCd": item.find('hsCd').text,
        "impDlr": item.find('impDlr').text,
        "impWgt": item.find('impWgt').text,
        "statCd": item.find('statCd').text,
        "statCdCntnKor1": item.find('statCdCntnKor1').text,
        "statKor": item.find('statKor').text,
        "year": item.find('year').text
    }

# 데이터 저장
items = root.findall('.//item')
for item in items:
    data = parse_item(item)
    collection.insert_one(data)

print('데이터가 MongoDB에 저장되었습니다.')
