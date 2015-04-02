# -*- coding:utf-8 -*-
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64)"
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    # print response.read()
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
f = open("qiubai.txt", "w+")
content = response.read().decode('utf-8')
# pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
# '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
# item[0]:用户名 item[1]:发布时间 item[2]:段子 item[3]:图片 item[4]:点赞数
pattern = re.compile(
    '<div class="article .*?>(.*?)<div class="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
    re.S)
items = re.findall(pattern, content)
username = ""
try:
    for item in items:
        # 解析用户名
        hasname = re.search("img", item[0])
        if hasname:
            pattern1 = re.compile('<img src=.*?/>.*?<a href=.*?>(.*?)</a>', re.S)
            username = re.findall(pattern1, item[0])[0]
        else:
            username = u"匿名"
        # 如果有图就不要了，无图的记录到文件中
        haspic = re.search('img', item[3])
        if haspic:
            continue

        name = u'用户名：' + username.strip() + '\n'
        time = u'时间：' + item[1] + '\n'
        f.write(name.encode('utf-8'))
        f.write(time.encode('utf-8'))
        f.write(item[2].strip().encode('utf-8') + '\n')
        f.write(u'点赞数：'.encode('utf-8') + item[4].strip().encode('utf-8') + '\n')
        f.write("###########################################\n")
finally:
    f.close()