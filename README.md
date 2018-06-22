# autohome_spider
利用Scrapy框架爬取汽车之家口碑的链接。

利用Fiddler，从汽车之家安卓客户端抓包，发现如下类型的链接：

> https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss3170-st0-p1-s20-isstruct0-o0.json

其中：
* pm2:不知道什么意思
* ss3170:是车系id，3170表示奥迪A3
* st0:不知道什么意思
* p1:当前为第一页
* p20:（可能是20也）没有实际意义
* isstruct1:一种结构，也就是第一次请求，返回的json中包括标签（如：空间大，外观漂亮，耗油大）
* isstruct0:另一种结果，没有用户设定的标签

## 抓取口碑的url
抓包汽车之家App里的请求, 获得所有口碑的id,从而拼接出所有口碑的url
