import os
import requests
import json
from datetime import datetime

# 1. 환경 변수에서 키 로드 (GitHub Secrets 설정 필요)
WEATHER_KEY = 'tuMy7IwZEcZDUDNlbvVcvwPCeGsWU93jRV3fVFa0jWLjf1SQDfxWwJumex/vTz80+koLNADSBBZ+Npa4TGb0uA=='
KAKAO_REST_KEY = '58fb217bafb7314b5e8434b26d8c5637'
KAKAO_REFRESH_TOKEN = "VVbvMKcClQSwr_fXflJ7lIudEer0pUkbAAAAAgoXACcAAAGdJTY9Oqew61y3DOUZ"

# 2. 기상청 단기예보 조회 (서울 기준 nx=60, ny=127)
def get_weather():
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    # 단기예보는 특정 시간에만 업데이트됨 (0500 예보 사용 예시)
    params = {
        'serviceKey': WEATHER_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'JSON',
        'base_date': '20260324',
        'base_time': '0500',
        'nx': '60', 
        'ny': '127'
    }
    
    # print(f"Requesting URL: {url}")
    # print(f"Requesting params: {params}")
    
    res = requests.get(url, params=params)
    # [디버깅용 추가] 서버가 준 실제 텍스트를 로그에 찍어봅니다.
    # print("Full Response:", res.text) 
    
    sky_map = {'1': '☀️맑음', '3': '☁️구름많음', '4': '☁️흐림'}
                
    data = res.json()
    
    items = data['response']['body']['items']['item']
    weather_info = {}
    for item in items:
        if item['category'] == 'TMP': # 기온
            weather_info['temp'] = item['fcstValue']
            print("weather_info['temp']", weather_info['temp']) 
        if item['category'] == 'SKY': # 하늘상태 (1:맑음, 3:구름많음, 4:흐림)
            weather_info['sky'] = sky_map.get(item['fcstValue'], '알수없음')
            print("weather_info['sky']", weather_info['sky'])
            
    return f"오늘의 날씨: {weather_info['sky']}, 기온: {weather_info['temp']}도 입니다."

# 3. 카카오 Access Token 갱신 (Refresh Token 활용)
def refresh_kakao_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_REST_KEY,
        "refresh_token": KAKAO_REFRESH_TOKEN,
        "client_secret": "NYQQRu2cqvBuVa9DBpWXL3jcZLS9Isks"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    print("1")
    res = requests.post(url, data=data, headers=headers)
    print("2", res.text) 
    return res.json()['access_token']

# 4. 나에게 카톡 보내기
def send_kakao_msg(text):
    access_token = refresh_kakao_token()
    url = "https://kapi.kakao.com"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    template = {
        "object_type": "text",
        "text": text,
        "link": {"web_url": "https://www.weather.go.kr"},
        "button_title": "날씨 확인"
    }
    
    res = requests.post(url, headers=headers, data={'template_object': json.dumps(template)})
    return res.status_code

# 5. 
def get_kakao_token():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_KEY,
        "redirect_uri": "http://localhost:8080",
        "code": KAKAO_REFRESH_TOKEN,
        "client_secret": "NYQQRu2cqvBuVa9DBpWXL3jcZLS9Isks"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    print("1")
    res = requests.post(url, data=data, headers=headers)
    print("2", res.text) 
    return res.status_code
    
def get_kakao_authorize():
    url = "https://kauth.kakao.com/oauth/authorize"
    data = {
        "response_type": "code",
        "client_id": KAKAO_REST_KEY,
        "redirect_uri": "http://localhost:8080"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    print("1")
    res = requests.get(url, data=data, headers=headers)
    print("2", res.text)     
    return res.status_code

# 메인 실행
if __name__ == "__main__":
    try:
        # msg = get_weather()
        # status = send_kakao_msg(msg)
        status = refresh_kakao_token()
        # status = get_kakao_token()
        if status == 200:
            print("메시지 전송 성공!")
    except Exception as e:
        print(f"오류 발생: {e}")
