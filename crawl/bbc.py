from urllib.parse import urljoin
from pprint import pprint

from bs4 import BeautifulSoup

from base import Crawler


class BBC(Crawler):
    def __init__(self):
        self.urls = [
            'http://feeds.bbci.co.uk/news/rss.xml?edition=uk',
            'http://feeds.bbci.co.uk/news/rss.xml?edition=us',
            'http://feeds.bbci.co.uk/news/rss.xml?edition=int'
        ]
        self.story_tag = 'story-body__inner'
        self.classes_to_ignore = [
            'Tweet-text'
        ]

    def crawl(self):
        for url in self.urls:
            article_rss = self.get_xml_page(url)
            for item in article_rss[0]:
                if item.tag == 'item':
                    title = item[0].text
                    original_url = item[2].text
                    story_text = self.get_details(self.get_page(original_url))
                    self.store_tfidf(title, 'bbc', original_url, story_text, 5, 'english')


    def get_details(self, soup):
        story_text = ""
        story = soup.find('div', class_=self.story_tag)
        if story:
            for p in story.find_all('p'):
                if len(p.text) > 0 and (
                            (p.has_attr('class') and p['class'][0] not in self.classes_to_ignore)
                            or not p.has_attr('class')
                ):
                    story_text += p.text
                    if p.text.endswith('.'):
                        story_text += ' '

        return story_text
