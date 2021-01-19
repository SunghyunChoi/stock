from news.models import Column
from bs4 import BeautifulSoup
import requests


class LG:
    def __init__(self):
        self.url = "https://www.mk.co.kr/opinion/editorial/"
        self.name = "name"

    def req(self):
        report_html = requests.get(self.url)
        soup = BeautifulSoup(
            report_html.content.decode("euc-kr", "replace"), "html.parser"
        )
        lists = soup.select("#container_left > div.list_area > dl.article_list")

        articles = []
        for article in lists:
            a_tag = article.select("dt > a")
            title = a_tag[0].getText()
            url = a_tag[0]["href"]
            articles.append({"title": title, "url": url})
        return articles

    def save_db(self):
        articles = self.req()
        for article in articles:
            column = Column()
            column.title = article["title"]
            column.url = article["url"]
            column.save()
        return 0
