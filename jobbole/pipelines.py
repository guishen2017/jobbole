# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.conf import settings
from scrapy.pipelines.images import ImagesPipeline
import pymysql
import pymongo


class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item

class JoboleArticleJsonPipeline(object):
    def __init__(self):
        self.file = open("jobbole.json", "wb")
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "/n"
        self.file.write(content.encode("utf-8"))
        return item
    def close_spider(self, spider):
        self.file.close()

class JoboleArticleMysqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host=settings['MYSQL_HOST'], user=settings['MYSQL_USER'],
                                       password = settings['MYSQL_PASSWORD'],database = settings['MYSQL_DB'], port = 3306,
                                       charset="utf8", use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole(title, url, create_date, url_object_id, tags, comment_nums,fav_nums,praise_nums) values (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['url_object_id'],
                                         item['tags'], item['comment_nums'], item['fav_nums'], item['praise_nums']))
        self.connect.commit()

class JobboleArticleMongodbPipeline(object):
    def __init__(self, table):
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MONGODB_HOST')
        dbname = crawler.settings.get('MONGODB_DBNAME')
        tablename = crawler.settings.get('MONGODB_SHEETNAME')
        client = pymongo.MongoClient(host)
        db = client[dbname]
        table = db[tablename]
        return cls(table)

    def process_item(self, item, spider):
        data = dict(item)
        self.table.insert(data)
        return item

class JobboleArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            item['front_image_path'] = value['path']
        return item
