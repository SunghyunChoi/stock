import requests
import pandas as pd
import re  # 정규표현식


class naver_news:
    def __init__(self):
        self.client_id = "2QV1qN7c3L6Te7OJsrbi"
        self.client_secret = "yBTGdL1ezi"

        self.search_word = "코스피"
        self.encode_type = "json"  # 출력방식 json or xml
        self.max_display = 20  # 출력 뉴스수
        self.sort = "date"  # date 시간순, sim 관련도 순
        self.start = 1  # 출력 위치
        self.url = f"https://openapi.naver.com/v1/search/news.{self.encode_type}?query={self.search_word}&display={str(int(self.max_display))}&start={str(int(self.start))}&sort={self.sort}"

        # 헤더에 아이디와 키 정보 넣기
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    # 정규표현식을 이용해서 html 코드의 불필요한 항목 지우기

    # HTTP요청 보내기
    def requests(self):
        self.news_json = requests.get(self.url, headers=self.headers)
        # dataframe으로 변경 후 처리
        self.news_df = pd.DataFrame(self.news_json.json()["items"])

        def clean_html(x):
            x = re.sub("\&\w*\;", "", x)
            x = re.sub("<.*?>", "", x)
            return x

        self.news_df["title"] = self.news_df["title"].apply(lambda x: clean_html(x))
        self.news_df["description"] = self.news_df["description"].apply(
            lambda x: clean_html(x)
        )

        return self.news_df[2:3]["description"]

    def save_csv(self):
        self.news_df.to_csv(f"news_search_result_{self.search_word}.csv")


# test--------------------------
test = naver_news()
# 요청 결과 보기 200 이면 정상적으로 요청 완료
print(test.requests())
test.save_csv()
