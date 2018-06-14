import psycopg2

conn = psycopg2.connect(database="qichezhijia201806", user="postgres", password="postgres", host="192.168.1.201", port="5432")
cur = conn.cursor()

#cursor.execute('insert into xiangou.test ("seriesId", "koubeiId", url) values (1, 2, "3")')
# cur.execute("""CREATE TABLE xiangou.test ("seriesId" int,"koubeiId" int, url text);""")
cur.execute("""SELECT "nSeriesIDWeb" FROM public."tSeries"; """)
all_series_id = cur.fetchall()
koubei_list_template = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%d-st0-p1-s20-isstruct0-o0.json"
urls = [koubei_list_template % (series_id) for series_id in all_series_id]
print(urls)


# insert one item
# cur.execute("""INSERT INTO xiangou.test("seriesId", "koubeiId", url)VALUES(%s, %s, %s)""" , (100, 101, "突突突"))
# cur.execute("INSERT INTO xiangou.test(num, data)VALUES(%s, %s)", (2, 'bbb'))
# cur.execute("INSERT INTO xiangou.test(num, data)VALUES(%s, %s)", (3, 'ccc'))
print("结束")