import scrapy
import json
from autohome.items import AutohomeItem
import psycopg2

class AutoHomeSpider(scrapy.Spider):
	name = "autohome"

	def get_seriesId(self):
		conn = psycopg2.connect(database="qichezhijia201806", user="postgres", password="postgres", host="192.168.1.201", port="5432")
		cursor = conn.cursor()
		cursor.execute(r'SELECT "nSeriesIDWeb" FROM public."tSeries";')
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result

	# start_urls = [
	# 	"https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss2123-st0-p1-s20-isstruct1-o0.json"
	# ]
	def start_requests(self):
		all_series_id = self.get_seriesId()
		koubei_list_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%d-st0-p1-s20-isstruct0-o0.json"
		urls = [koubei_list_template % (series_id) for series_id in all_series_id]
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)



	def parse(self, response):
		item = AutohomeItem()
		koubei_list_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%d-st0-p%d-s20-isstruct0-o0.json"
		koubei_url_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/NewEvaluationInfo.ashx?eid=%d&useCache=1"
		alldata = json.loads(response.text)

		series_id = alldata["result"]["seriesid"]
		pagecount = alldata["result"]["pagecount"]

		for koubei in alldata["result"]["list"]:
			item["seriesId"] = series_id
			item["koubeiId"] = koubei["Koubeiid"]
			item["url"] = koubei_url_template % (koubei["Koubeiid"])
			yield item

		if pagecount>1:
			urls = [koubei_list_template % (series_id, pageindex) for pageindex in range(2, pagecount+1)]
			for url in urls:
				yield scrapy.Request(url=url,callback=self.parse)


if __name__ == '__main__':
	spider = AutoHomeSpider()
	res = spider.start_request()
	# print(res)
	# print(len(res))