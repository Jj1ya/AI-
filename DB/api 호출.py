import requests
import pandas as pd

def fetch_data(strtYymm, endYymm, hsSgn, cntyCd):
    url = "https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList"
    params = {
        "serviceKey": "6mxlnmF2RW8P0hqL52XMnCQ3LxEjCv5lUeischYP8jDaV1f3DL4J4xQ5HC+fupUDW7tiHADCftmhbL8gi2bjnQ==",
        "strtYymm": strtYymm,
        "endYymm": endYymm,
        "hsSgn": hsSgn,
        "cntyCd": cntyCd,
    }
    response = requests.get(url, params=params)
    # 여기서는 XML 데이터를 처리하는 예시 코드를 생략합니다.
    # 실제로는 응답 데이터를 파싱하여 필요한 데이터를 추출해야 합니다.
    return response.text  # 예시로 응답 텍스트를 반환

# 간단한 예시로, 여러 HS 코드에 대한 데이터를 순차적으로 요청
hs_codes = ["854232"]  # 실제 HS 코드 예시
results = []
for hs_code in hs_codes:
    data = fetch_data("202001", "202012", hs_code, "US")
    results.append(data)

# 결과 데이터를 합치는 로직 구현 필요
