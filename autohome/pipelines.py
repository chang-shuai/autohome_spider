# -*- coding: utf-8 -*-
import psycopg2
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutohomePipeline(object):

	def __init__(self, kargs):
		self.conn = psycopg2.connect(database=kargs["pg_dbname"], user=kargs["pg_user"], password=kargs["pg_password"], host=kargs["pg_host"], port=kargs["pg_port"])
		self.cursor = self.conn.cursor()
		self.sql = """INSERT INTO autohome_koubei.koubei_url("seriesId", "koubeiId", url)VALUES(%s, %s, %s)"""

	@classmethod
	def from_crawler(cls, crawler):
		pg_param = dict(
				pg_host = crawler.settings.get("PG_HOST"),
				pg_port = crawler.settings.get("PG_PORT"),
				pg_user = crawler.settings.get("PG_USER"),
				pg_password = crawler.settings.get("PG_PASSWORD"),
				pg_dbname = crawler.settings.get("PG_DBNAME"),
			)
		return cls(pg_param)

	def process_item(self, item, spider):
		self.cursor.execute(self.sql , (item["seriesId"], item["koubeiId"], item["url"]))
		self.conn.commit()
		return item

	def close_spider(self, spider):
		self.cursor.close()
		self.conn.close()

		
