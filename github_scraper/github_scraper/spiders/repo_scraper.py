import scrapy
import links_from_header
import json
import os

class Repo(scrapy.Item):
    id = scrapy.Field()
    languages_url = scrapy.Field()
    name = scrapy.Field()

class Scraper(scrapy.Spider):
    name = "github"
    access_token = os.environ['github_token']

    def __init__(self):
        self.count = 0

    start_urls = ['https://api.github.com/repositories?since=76761293&access_token={}'.format(access_token)]
    
    def parse(self, response):
        
        self.logger.info(self.count)
        if self.count == 100:
            return
        
        self.count += 1

        json_body = json.loads(response.body.decode('utf-8'))

        for item in json_body:
            current_item = Repo()
            current_item['id'] = item['id']
            current_item['name'] = item['name']
            current_item['languages_url'] = item['languages_url']
            yield current_item
        
        link_header = links_from_header.extract(response.headers['Link'].decode('utf-8'))
        if 'next' in link_header:
            next_page = link_header['next']
            yield scrapy.Request(next_page, callback=self.parse)