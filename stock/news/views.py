from django.shortcuts import render
from django.http import HttpResponse
import requests

# ---
import pandas as pd
import re  # 정규표현식
from .models import News


def index(request):
    keyword = request.GET.get("keyword")
    if keyword:
        # 키워드 검색 결과가 없을 때만 작동합니다.
        result = News.objects.filter(keyword=keyword)
        if not result:
            test = naver_news(keyword)
            test.requests()
            test.save_db()

    """
    여기에 서버사이드 렌더링을 위한 데이터 받아오기
    """
    results = News.objects.filter(keyword=keyword)
    newses = []
    for result in results:
        news = {
            "subject": result.subject,
            "content": result.content,
            "created_date": result.created_date,
            "url": result.url,
        }
        newses.append(news)
    context = {
        "keyword": keyword,
        "newses": newses,
    }
    return render(request, "base.html", context)


class naver_news:
    def __init__(self, keyword_recieved):
        self.client_id = "2QV1qN7c3L6Te7OJsrbi"
        self.client_secret = "yBTGdL1ezi"

        self.search_word = keyword_recieved
        self.encode_type = "json"  # 출력방식 json or xml
        self.max_display = 20  # 출력 뉴스수, 나중에 환경변수로 바꾸기
        self.sort = "sim"  # date 시간순, sim 관련도 순
        self.start = 1  # 출력 위치
        self.url = f"https://openapi.naver.com/v1/search/news.{self.encode_type}?query={self.search_word}&display={str(int(self.max_display))}&start={str(int(self.start))}&sort={self.sort}"

        # 헤더에 아이디와 키 정보 넣기
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    # HTTP요청 보내기
    def requests(self):
        self.news_json = requests.get(self.url, headers=self.headers)
        # dataframe으로 변경 후 처리
        self.news_df = pd.DataFrame(self.news_json.json()["items"])

        # 정규표현식을 이용해서 html 코드의 불필요한 항목 지우기
        def clean_html(x):
            x = re.sub("\&\w*\;", "", x)
            x = re.sub("<.*?>", "", x)
            return x

        self.news_df["title"] = self.news_df["title"].apply(lambda x: clean_html(x))
        self.news_df["description"] = self.news_df["description"].apply(
            lambda x: clean_html(x)
        )

        # return self.news_df
        return self.news_json

    def save_csv(self):
        self.news_df.to_csv(f"news_search_result_{self.search_word}.csv")

    def save_db(self):
        for i in range(self.max_display):
            news = News()
            news.subject = str(self.news_df.iloc[i]["title"])
            news.content = self.news_df.iloc[i]["description"]
            news.created_date = self.news_df.iloc[i]["pubDate"]
            news.url = self.news_df.iloc[i]["originallink"]
            news.keyword = self.search_word
            news.save()