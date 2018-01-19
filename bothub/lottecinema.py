import json
import math
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode


class LotteCinema(object):
    #base_url = 'http://www.lottecinema.co.kr'   # 롯데시네마 URL
    base_url = 'http://moviefriend.cafe24.com'
    base_url_cinema_data = '{}/LCWS/Cinema/CinemaData.aspx'.format(base_url)    # 영화관 정보 요청 URL
    base_url_movie_list = '{}/LCWS/Ticketing/TicketingData.aspx'.format(base_url)   # 예매 정보 요청 URL

    def make_payload(self, **kwargs):
        param_list = {'channelType': 'MW', 'osType': '', 'osVersion': '', **kwargs} # 파라미터 데이터
        data = {'ParamList': json.dumps(param_list)}    # JSON 인코딩
        payload = urlencode(data).encode('utf8')    # Object를 JSON 문자열로 변경
        return payload

    def byte_to_json(self, fp):
        content = fp.read().decode('utf8')  # JSON 문자열을 Python 타입으로 변환
        return json.loads(content)  # JSON 디코딩

    def get_theater_list(self): # 영화관 정보 얻기
        url = self.base_url_cinema_data # 영화관 정보 요청 URL
        payload = self.make_payload(MethodName='GetCinemaItems')
        with urlopen(url, data=payload) as fin:
            json_content = self.byte_to_json(fin)
            return [
                {
                    'TheaterName': '{} 롯데시네마'.format(entry.get('CinemaNameKR')),    # 영화관 한글이름
                    # 영화관 분할코드, 정렬순서,  영화관ID
                    'TheaterID': '{}|{}|{}'.format(entry.get('DivisionCode'), entry.get('SortSequence'), entry.get('CinemaID')),
                    'Longitude': entry.get('Longitude'),    # 영화관 경도
                    'Latitude': entry.get('Latitude')       # 영화관 위도
                }
                # 영화관 정보 요청 URL 중 Cinemas 하위 Items 목록에서 선출
                for entry in json_content.get('Cinemas').get('Items')
            ]

    def distance(self, x1, x2, y1, y2): # 영화관 위치 계산
        dx = float(x1) - float(x2)
        dy = float(y1) - float(y2)
        distance = math.sqrt(dx**2 + dy**2)
        return distance

    def filter_nearest_theater(self, theater_list, pos_latitude, pos_longitude, n=3):   # 근처 위치의 상영관 3개 정보
        distance_to_theater = []
        for theater in theater_list:
            # 현재 위치와 영화관 위치 좌표 계산
            distance = self.distance(pos_latitude, theater.get('Latitude'), pos_longitude, theater.get('Longitude'))
            distance_to_theater.append((distance, theater))

        return [theater for distance, theater in sorted(distance_to_theater, key=lambda x: x[0])[:n]]

    def get_movie_list(self, theater_id):   # 영화 제목과 상영시간, 남은 좌석
        url = self.base_url_movie_list  # 예매 정보 요청 URL
        target_dt = datetime.now()  # 현재 시각
        target_dt_str = target_dt.strftime('%Y-%m-%d')  # 현재날짜 년월일 형식으로 변환
        # 파라미터 구분
        # 현재 날짜와 영화관 ID, 영화 ID
        payload = self.make_payload(MethodName='GetPlaySequence', playDate=target_dt_str, cinemaID=theater_id, representationMovieCode='')
        with urlopen(url, data=payload) as fin:
            json_content = self.byte_to_json(fin)
            movie_id_to_info = {}

            # 예매 정보 요청 URL 중 PlaySeqsHeader 하위 Items 목록에서 산출
            for entry in json_content.get('PlaySeqsHeader', {}).get('Items', []):
                # 영화코드, 영화 한글이름
                movie_id_to_info.setdefault(entry.get('MovieCode'), {})['Name'] = entry.get('MovieNameKR')

            # 예매 정보 요청 URL 중 PlaySeqs 하위 Items 목록에서 열거
            for order, entry in enumerate(json_content.get('PlaySeqs').get('Items')):
                # 영화코드에 따른 스케쥴
                schedules = movie_id_to_info[entry.get('MovieCode')].setdefault('Schedules', [])
                schedule = {
                    'StartTime': '{}'.format(entry.get('StartTime')),   # 영화 시작 시간
                    'RemainingSeat': int(entry.get('TotalSeatCount')) - int(entry.get('BookingSeatCount'))  # 남아있는 좌석 수 계산
                }
                schedules.append(schedule)  # 스케쥴 표시
            return movie_id_to_info

cinema = LotteCinema()

print(cinema.filter_nearest_theater(cinema.get_theater_list(), 35.145, 126.881))    # 광주광역시 서구 화정2동 기준
print(cinema.get_movie_list('1|106|9047'))   # 충장로 롯데시네마 기준
