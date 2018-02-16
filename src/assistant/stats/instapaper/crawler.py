import logging
import os

import scrapy
from scrapy.crawler import CrawlerProcess

logger = logging.getLogger(__name__)


class InstapaperSpider(scrapy.Spider):
    name = 'Instapaper'
    start_urls = ['https://www.instapaper.com/u']

    def make_requests_from_url(self, url):
        request = super(InstapaperSpider, self).make_requests_from_url(url)
        for pair in os.environ['COOKIES'].split(';'):
            key, value = pair.split('=')
            request.cookies[key] = value
        return request

    def parse(self, response):
        yield response.follow('/archive', callback=self._parse_page_factory('archive'))

        for folder in response.css('ul.folders li'):
            name = ''.join(i.strip() for i in folder.css('.folder_link::text').extract())
            link = folder.css('.folder_link::attr(href)').get()
            logger.info('Found folder: {}'.format(name))
            yield response.follow(link, callback=self._parse_page_factory(name))

    def parse_page(self, response, tag):
        logger.info('Parse page: {} with tag: {}'.format(response.url, tag))
        for post in response.css('article.article_item'):
            starred = 'starred' in list(post.root.classes)

            title = post.css('a.article_title::attr(title)').get().strip()
            url = post.css('a.js_domain_linkout::attr(href)').get().strip()
            preview = post.css('.article_preview').get().strip()
            date_shift = post.css('.article_item_footer .meta_date::text').get().strip()
            read_time = post.css('.article_item_footer .meta_read_time::text').get()
            if read_time:
                read_time = read_time.replace('·', '').strip()

            yield {
                'title': title,
                'url': url,
                'preview': preview,
                'date_shift': date_shift,
                'read_time_raw': read_time,
                'starred': starred,
                'tag': tag
            }

        if response.css('.paginate_older::attr(href)').get():
            next_page = response.css('.paginate_older::attr(href)').get()
            yield response.follow(next_page, callback=self._parse_page_factory(tag))

    def _parse_page_factory(self, tag):
        return lambda r: self.parse_page(r, tag)


if __name__ == '__main__':
    process = CrawlerProcess({
        'FEED_URI': 'Instapaper.json',
        'FEED_FORMAT': 'json',
        'LOG_FILE': 'Instapaper.log',
        'LOG_LEVEL': 'INFO',
    })

    process.crawl(InstapaperSpider)
    process.start()
