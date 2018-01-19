import json
import math
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta

class BoxOffice(object):
    # 영화진흥위원회 요청 URL
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    def __init__(self, api_key):    # 생성자
        self.api_key = api_key

    def get_movies(self):   # 일일 박스오피스 정보 얻기
        target_dt = datetime.now() - timedelta(days=1)  # 현재날짜 -1일
        target_dt_str = target_dt.strftime('%Y%m%d')    # 날짜를 문자열로 변환
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str) # 영화진흥위원회 응답 URL
        # http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json
        # ?key=9132dfdc71c366819908f2fdc442187f&targetDt=20180111
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))   # json 결과 데이터를 파이썬에서 활용한 객체로 변형

    def simplify(self, result): # 필요 정보 가져오기
        return [
           {
              '순위': entry.get('rank'),    # 해당일자의 박스오피스 순위
              '영화명': entry.get('movieNm'), # 영화명(국문)
              '금일 관객수' : entry.get('audiCnt'), # 금일 관객수
              '누적 관객수': entry.get('audiAcc')  # 누적 관객수
           }
           for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList') # 응답 결과 중 일일 박스오피스 리스트
        ]

box = BoxOffice('9132dfdc71c366819908f2fdc442187f') # 영화진흥위원회 API 키
movies = box.get_movies()   # 일일 박스오피스 정보 얻기
print(box.simplify(movies)) # 일일 박스오피스 정보 출력
