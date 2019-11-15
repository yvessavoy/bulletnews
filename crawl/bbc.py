import logging

from base import Crawler


class BBC(Crawler):
    def __init__(self):
        super().__init__()
        self.urls = [
            'http://feeds.bbci.co.uk/news/rss.xml?edition=uk',
            'http://feeds.bbci.co.uk/news/rss.xml?edition=us',
            'http://feeds.bbci.co.uk/news/rss.xml?edition=int'
        ]
        self.story_tag = 'story-body__inner'
        self.classes_to_ignore = [
            'Tweet-text'
        ]

        self.base_url_cnt = len(self.urls)
        self.logger = self.get_logger(__name__)

    def crawl(self):
        for url in self.urls:
            article_rss = self.get_xml_page(url)
            self.max_articles = len(article_rss[0])
            for item in article_rss[0]:
                if item.tag == 'item':
                    title = item[0].text
                    original_url = item[2].text
                    story_text, publish_tsd = self.get_details(self.get_page(original_url))
                    self.store_tfidf(title, 'bbc', original_url, story_text, 5, 'english', publish_tsd)

    def get_details(self, soup):
        story_text = ""
        try:
            publish_tsd = soup.text.split('"datePublished":"')[1].split('","')[0]
        except IndexError:
            publish_tsd = '1990-01-01T00:00:00.000Z'
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

        return story_text, publish_tsd
