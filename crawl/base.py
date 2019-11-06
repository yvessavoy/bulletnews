from urllib import parse
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

import web.models as models
from tfidf import tfidf


class Crawler:
    def __init__(self \
               , origin=None
               , base_url=None
               , list_url=None
               , article_url_class=None
               , article_url_tle=None
               , article_url_tle_class=None
               , article_title_in_head=None
               , article_detail_title_tag=None
               , article_detail_title_class=None
               , article_detail_text_tag=None
               , article_detail_text_class=None):
        self.origin = origin
        self.base_url = base_url
        self.list_url = list_url
        self.article_url_class = article_url_class
        self.article_url_tle = article_url_tle
        self.article_url_tle_class = article_url_tle_class
        self.article_detail_title_tag = article_detail_title_tag
        self.article_detail_title_class = article_detail_title_class
        self.article_detail_text_tag = article_detail_text_tag
        self.article_detail_text_class = article_detail_text_class
        self.article_title_in_head = article_title_in_head

    def crawl(self):
        page = self.get_article_page()
        article_urls = self.get_article_list(page)
        for article_url in article_urls:
            (title, text) = self.get_article(article_url)
            top_sents = tfidf(text, 5, 'english')
            self.store(title, top_sents, article_url)

    def store(self, title, sents, url):
        article = models.Article(title=title,
                                 origin=self.origin,
                                 insert_tsd=timezone.now(),
                                 original_url=url,
                                 bp1=sents[0]['sentence'],
                                 bp2=sents[1]['sentence'],
                                 bp3=sents[2]['sentence'],
                                 bp4=sents[3]['sentence'],
                                 bp5=sents[4]['sentence'])
        article.save()

    def get_article(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        if self.article_title_in_head:
            title = soup.title.string    
        else:
            title = soup.find(self.article_detail_title_tag, class_=self.article_details_title_class).text

        text = ""
        for text_part in soup.find_all(self.article_detail_text_tag, class_=self.article_detail_text_class):
            formatted_text = text_part.text.strip()
            text += formatted_text
            if formatted_text[-1:] == '.':
                text += " "

        return (title, text)

    def get_article_page(self):
        r = requests.get(parse.urljoin(self.base_url, self.list_url))
        return BeautifulSoup(r.text, 'html.parser')

    def get_article_list(self, article_page):
        if self.article_url_class:
            return self.get_article_list_by_class(article_page)
        elif self.article_url_tle_class:
            return self.get_article_list_by_tle_class(article_page)
        elif self.article_url_tle:
            return self.get_article_list_by_tle(article_page)

    def get_article_list_by_class(self, page):
        articles = []
        for article in page.find_all('a', class_=self.article_url_class):
            url = parse.urljoin(self.base_url, article.get('href'))
            if url not in articles:
                articles.append(url)

        return articles

    def get_article_list_by_tle_class(self, page):
        articles = []
        for article in page.find_all(self.article_url_tle, class_=self.article_url_tle_class):
            a_el = article.find('a')
            url = parse.urljoin(self.base_url, a_el.get('href'))
            if url not in articles:
                articles.append(url)

        return articles

    def get_article_list_by_tle(self, page):
        articles = []

        for article in page.find_all(self.article_url_tle):
            a_el = article.find('a')
            url = parse.urljoin(self.base_url, a_el.get('href'))
            if url not in articles:
                articles.append(url)

        return articles