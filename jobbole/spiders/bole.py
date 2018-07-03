# -*- coding: utf-8 -*-
import scrapy
from jobbole.items import JobboleArticleItemLoader, JobboleArticleItem
from jobbole.utils.md5 import get_md5

class BoleSpider(scrapy.Spider):
    name = 'bole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        url_list = response.xpath('//div[@class="grid-8"]//div[@class="post-thumb"]')
        for url in url_list:
            article_url = url.xpath("./a/@href").extract_first("")
            img_url = url.xpath("./a/img/@src").extract_first("")
            yield scrapy.Request(url=article_url, meta={"img_url":img_url}, callback=self.parse_article)

        next_page = response.xpath('//div[@class="navigation margin-20"]//a[contains(@class,"next")]/@href').extract_first("")
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        load_item = JobboleArticleItemLoader(item=JobboleArticleItem(), response=response)
        img_url = response.meta.get("img_url", "")
        load_item.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        load_item.add_value("url", response.url)
        load_item.add_value("url_object_id", get_md5(response.url))
        load_item.add_value("front_image_url", [img_url])
        load_item.add_xpath("praise_nums", '//div[@class="post-adds"]/span/h10/text()')
        load_item.add_xpath("fav_nums", '//div[@class="post-adds"]/span[2]/text()')
        load_item.add_xpath("comment_nums", '//a[@href="#article-comment"]/span/text()')
        load_item.add_xpath("tags", '//div[@class="entry-meta"]/p/a/text()')
        # load_item.add_xpath("create_date", '//p[@class="entry-meta-hide-on-mobile"]/text()')
        load_item.add_xpath("content", '//div[@class="entry"]')
        item = load_item.load_item()
        yield item