import scrapy
import json
from autohome.items import AutohomeItem
import psycopg2

class AutoHomeSpider(scrapy.Spider):
	name = "autohome"

	def get_seriesId(self):
		"""链接数据库后，所有的获得车系Id"""
		conn = psycopg2.connect(database="qichezhijia201806", user="postgres", password="postgres", host="192.168.1.201", port="5432")
		cursor = conn.cursor()
		cursor.execute(r'SELECT "nSeriesIDWeb" FROM public."tSeries";')
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result

	# 	测试链接
	#	start_urls = [
	# 	"https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss2123-st0-p1-s20-isstruct1-o0.json"
	# ]

	def start_requests(self):
		all_series_id = self.get_seriesId()
		# 口碑目录网页链接的模板
		koubei_list_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%d-st0-p1-s20-isstruct0-o0.json"
		
		urls = [koubei_list_template % (series_id) for series_id in all_series_id]
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)



	def parse(self, response):
		"""通过第一请求，根据返回的信息，判断此车系一共有多少页口碑列表，和每一条口碑的id，然后每一页递进抓取。"""
		item = AutohomeItem()
		koubei_list_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%d-st0-p%d-s20-isstruct0-o0.json"
		# 口碑评论的网页链接模板
		koubei_url_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/NewEvaluationInfo.ashx?eid=%d&useCache=1"
		alldata = json.loads(response.text)
		# 从返回的json中获得车系id，省去了参数传递
		series_id = alldata["result"]["seriesid"]
		# 从返回的json中获得口碑列表一共多少页。
		pagecount = alldata["result"]["pagecount"]

		# 拼接完口碑评论链接并且组装item
		for koubei in alldata["result"]["list"]:
			item["seriesId"] = series_id
			item["koubeiId"] = koubei["Koubeiid"]
			item["url"] = koubei_url_template % (koubei["Koubeiid"])
			yield item
		# 如果口碑列表的总页数大于1页，则从第二页开始继续进行解析
		if pagecount>1:
			urls = [koubei_list_template % (series_id, pageindex) for pageindex in range(2, pagecount+1)]
			for url in urls:
				yield scrapy.Request(url=url,callback=self.parse)


if __name__ == '__main__':
	spider = AutoHomeSpider()
	res = spider.start_request()
	# print(res)
	# print(len(res))