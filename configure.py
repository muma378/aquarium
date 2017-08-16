#coding=utf8
'''
Created on 2015.04.09
@author: Administrator
'''
import time,string
import ConfigParser

http_header = {
"Accept":"*/*",
"Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
"Connection":"keep-alive",
"Cookie":"B=b2tl639a9oaii&b=3&s=l9; yisn=lrs=1&=undefined&h=112&d=1129x280&dwh=1286x316",
"Host":"sg.images.search.yahoo.com",
"Referer":"http://sg.images.search.yahoo.com/search/images;_ylt=A2oKiZes3slUjHYA.1gk4gt.;_ylc=X1MDMjExNDcwODAwNARfcgMyBGJjawNiMnRsNjM5YTlvYWlpJTI2YiUzRDMlMjZzJTNEbDkEZnIDBGdwcmlkA2c3TVN0ZER5U3hXbmN2bDNjWm1RWUEEbXRlc3RpZANudWxsBG5fc3VnZwMxMARvcmlnaW4Dc2cuaW1hZ2VzLnNlYXJjaC55YWhvby5jb20EcG9zAzEEcHFzdHIDZ2FveXVhbnl1YW4EcHFzdHJsAzExBHFzdHJsAzExBHF1ZXJ5A2dhb3l1YW55dWFuBHRfc3RtcAMxNDIyNTE1ODk2BHZ0ZXN0aWQDbnVsbA--?gprid=g7MStdDySxWncvl3cZmQYA&pvid=M5ZvoDEwNi6xdqYaVJwqUgGtMTE5LgAAAABJ.hR8&fr2=sa-gp-sg.images.search.yahoo.com&p=gaoyuanyuan&ei=UTF-8&iscqry=&fr=sfp",
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"
}

bing_header = {"Cookie":"SRCHUID=V=2&GUID=62D6549D938F44AE96BF0D1BA24A8AF0; SRCHUSR=AUTOREDIR=0&GEOVAR=&DOB=20141216; _EDGE_V=1; MUIDB=02BAD2F4FF3660471390D5E6FEED61C8; SRCHD=D=3662357&AF=NOFORM; _UR=OMW=1; MUID=02BAD2F4FF3660471390D5E6FEED61C8; PPLState=1; _EDGE_S=SID=3EF186EA002368513328812201826982; RMS=F=AAAAAAAw&A=gQAAEEAAAAAQ; _U=1HcrVAzQ0HXJWyzko-IV8Z7jlWphTI2svf-WD3xx7gLMnZ1120c7-uk8Gk861dNGgTe1as9c7AZGpZZ-wiv0GtfiWhcCmYFBUtd7kYaEeRsacJXKq0GeSd7aB7FBM9cqY; ANON=A=8111424AB102987E2B4A8AD3FFFFFFFF&E=1087&W=1; KievRPSAuth=FABSARRaTOJILtFsMkpLVWSG6AN6C%2fsvRwNmAAAEgAAACG6%2fNksn0gzFEAElrUKZWC0ouc0jHP5MRRTb8gn+5yzqzBzHXvMoAuUKPWE2yLCcbXsDVfuUM+ibyDJiSrD4otqiIE7gOgclU2BgZVIid+wfWQCSvBMlW6H9uF5vzNVB2Mx0jZqF8+KPhUkB+Dv%2fThKKDoWA6zxPbUBp6X8PidnlyfCk0paq8sWfmHoIkxb%2f3aN0k2%2fkD8YTCrEVilM63AJ937VlcGEFLST9XRXuMkXcRbT9P26Bye5zyS622F0GW3J7keGe%2fHL8Yz4xNJMXQCGQzFLdlwIdgtGxiWjKUFJw29jT4Z1yQCUgxVgaVs4sOfEUyLThg8CeT7TBCyHq8CMyNMHcuXK8bz8txhgjZ4cgRt+ZnLAGkg5UixQAo9RqWlviCQRoYoL2zvr1yN5TfdA%3d; KievRPSSecAuth=FABSARRaTOJILtFsMkpLVWSG6AN6C%2fsvRwNmAAAEgAAACL1pkWDZcfg6EAE7pdl13H9FfcS43ZKQBxXxn5EbbPuLm2nIKYVlINSEzN05u33zfN8vTRiZIf8aXIVenXBSR7%2fBm1m%2fjEvYSBKbLtk9gXLb8%2f+OdiTmW3ybZUot0MOj9Jprnr3ZDuPabdkri5weOkN%2f0vsyoF9EYsefgiwZtVv9X3%2f9js4o7bec3VOnIdyIVJNw3iBpOjGGDsl4BIHjsAtMp%2fdKDFD8CsjS4rhY8bH22cS1UMBLGljsEUweCWQl3id7M0OunPSGVJrdiMBOZR%2f+9a9oWbxxMMfTX2QRdedxQISxbNNA6w4FKCCGn6QvMQO7mkntpCU3t5jSwFZ+owEMQgBSixhoRO+xDJw07I7bW0mV6zKy6mvUXhQAjULTzCwS66t6I3vlsrT7OIExPEA%3d; NAP=V=1.9&E=10b2&C=NCsaqDvmfh081xOtL0NIB9z2_NLJxDYPjUjugJfdzz1h59CZNkO72w&W=1; WLS=C=3e635a95253ba87d&N=Hongwei&TS=63570015184; _HOP=; SCRHDN=ASD=0&DURL=#; _SS=SID=CCC8DECA015246A580677D3CA1351D58&HVB=1434418752333&bIm=18867:; SRCHHPGUSR=CW=1903&CH=454&DPR=1",
                "Host":"cn.bing.com",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                "X-Requested-With":"XMLHttpRequest"}

yahoo_header = {"Cookie":"B=b2tl639a9oaii&b=3&s=l9; yisn=lrs=1&=undefined&h=112&d=1129x280&dwh=1286x316",
                "Host":"sg.images.search.yahoo.com",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                "Referer":"http://sg.images.search.yahoo.com/search/images;_ylt=A2oKiZes3slUjHYA.1gk4gt.;_ylc=X1MDMjExNDcwODAwNARfcgMyBGJjawNiMnRsNjM5YTlvYWlpJTI2YiUzRDMlMjZzJTNEbDkEZnIDBGdwcmlkA2c3TVN0ZER5U3hXbmN2bDNjWm1RWUEEbXRlc3RpZANudWxsBG5fc3VnZwMxMARvcmlnaW4Dc2cuaW1hZ2VzLnNlYXJjaC55YWhvby5jb20EcG9zAzEEcHFzdHIDZ2FveXVhbnl1YW4EcHFzdHJsAzExBHFzdHJsAzExBHF1ZXJ5A2dhb3l1YW55dWFuBHRfc3RtcAMxNDIyNTE1ODk2BHZ0ZXN0aWQDbnVsbA--?gprid=g7MStdDySxWncvl3cZmQYA&pvid=M5ZvoDEwNi6xdqYaVJwqUgGtMTE5LgAAAABJ.hR8&fr2=sa-gp-sg.images.search.yahoo.com&p=gaoyuanyuan&ei=UTF-8&iscqry=&fr=sfp",
                "X-Requested-With":"XMLHttpRequest"}

baidu_header = {
    "Cookie":"AIDUPSID=DB7BB489C266482DC9FBB13965064D2A; BDUSS=1NXZGNqfldlR3k2T0N6RUkwSWRWaHRQaXozamhmVXBHUTZJckJKdVRaTWtFNjVVQVFBQUFBJCQAAAAAAAAAAAEAAAAYa5I7TmV3X3BpYW8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACSGhlQkhoZUZ; __zpspc=188.2.1420022178.1420022178.1%234%7C%7C%7C%7C%7C%23; locale=zh; BDREFER=%7Burl%3A%22http%3A//news.baidu.com/n%3Fcmd%3D4%26class%3Drolling%26pn%3D1%26from%3Dtab%26sub%3D0%22%2Cword%3A%22%22%7D; __xsptplus188=188.1.1423555632.1423555632.1%234%7C%7C%7C%7C%7C%23%23oApaXgLcSFDiLJlBO35fFagow0SPrtBL; BAIDUID=DE6C69D62DB72D74D90E85D04492344E:FG=1; BIDUPSID=DE6C69D62DB72D74D90E85D04492344E; fb=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1441_13426_12657_13074_12670_10901_12867_13321_12692_13411_8502_12722_12735_13085_13325_13210_12836_13162_13257_11299_8498_10633; userid=3hsi32ht5; Hm_lvt_737dbb498415dd39d8abf5bc2404b290=1428548423,1428559255; Hm_lpvt_737dbb498415dd39d8abf5bc2404b290=1428559260",
    "Host":"image.baidu.com",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer":"http://image.baidu.com/",
    "X-Requested-With":"XMLHttpRequest"}


google_header = {"Cookie":"NID=68=lJlA1jdn4p45a7QnA12_ugHSqieVOaiVLZitJlrytM5l8EeZpFvTYMEy5TUG9KxKCzkpLZEOMUl_eqZIoa_rf_4UjSvQuT_uwr2tSCrdGPuMZDxJRToLHNy0sIidqWVkovnUE2nvtEyPnB9jaIFKnX8xii75zmVyTA; PREF=ID=1111111111111111:U=be1aaf16c188fb61:FF=0:TM=1429004962:LM=1434422334:S=loFjMTfXaJFBQ3li",
                "Host":"www.google.com",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                "Referer":"https://www.google.com/",
                "X-Requested-With":"XMLHttpRequest"}
flickr_header ={
"accept":"*/*",
"accept-language":"zh-CN,zh;q=0.8",
"Cookie":"xb=022333; BX=ejqq76tap75ri&b=3&s=rv; current_identity=1-1435800495; ffs=134481915-9649; cookie_accid=134481915; cookie_epass=a7156771632404a145d8ce607860a684; sa=1440984495%3A134502263%40N02%3A7b84e0e8934ba15957ab5f9665f67bb8; ywandp=10001109650879%3A1393929773%3B10001561398679%3A1149402401; fpc=10001109650879%3AZcv_hnLC%7C%7C%3B10001561398679%3AZbz8cTZf%7C%7C; fltoto=0%2C0%2C0%2C0%2C1%2C0%3B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%3B0%3B0%3B08123f2b0a2673e991f1e4ce66ff5f210e6f7221; fldetectedlang=zh-hk; vp=1343%2C962%2C1%2C17%2Csearch-photos-everyone-view%3A1074; cookie_session=134481915%3Aa7156771632404a145d8ce607860a684; RT=s=1436142298908&u=&r=https%3A//www.flickr.com/services/apps/create/noncommercial/%3F; flrbp=1436150529-697faf7d5b7923283e93b1523e668605a27e8be6; flrbrp=1436150529-030b811bbb65cf188771f2798689bf1f590b572f; flrbs=1436150529-7dfadb062ecf9b3968f774d5c5a45c1f5cf28901; flrbra=1436150529-9d9bd656e86dfcf2c198fd04003afdad0884e23d; flrbrf=1436150529-ffb257c37b17b942926e0da924f86e54907648d0; flrbgrp=1436150529-ba9d726c2baf5b243ab3f6e93f7e361dea4af8d7; flrbgdrp=1436150529-960096c31ceac01c1071900ed2ec1d603320ce90; flrbgmrp=1436150529-b64351648005b01bac1e2bb702ecb31bee0df68c; flrbre=1436150529-bbbca4c7166d75ef577d4f3ed9d7e946cc9724ac; flrbras=1436150529-16b55907bf645616c7c5199e0b61698dbf34624e; flrbrgs=1436150529-48084553db7f8a88e755a39a1526947f877725b9; flrbrps=1436150529-62a38505cc40a200fa9f1fd49ece1e4fe10341df; flrbcr=1436150529-0f0db71b396905d342d9464de31a559362fc26d5; flrb=27; flrbnu=1; localization=zh-hk%3Bus%3Bus; liqpw=1362; liqph=908",
"Host": "api.flickr.com",
"User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

flickr_date = {
'user':'leonharetd',
'pass':'199281'}

twitter_header = {
"Accept":"application/json, text/javascript, */*; q=0.01",
"Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
"Connection":"keep-alive",
#"Cookie":"guest_id=v1%3A142975738289396198; eu_cn=1; _ga=GA1.2.878769378.1429758089; _gat=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIBBoSJNAToMY3NyZl9p%250AZCIlZGI1ZWU1MzQzNDEyMzkzZmI3ZWY4MTQ2NmMxODA1YjM6B2lkIiU4NTJk%250AYzE0YzcyNmZhMjc3NTM0YjZlNWRjMzgyOTc2Mw%253D%253D--1e1dc5e887cf19712578f2615661440e644aa3cc",
"Cookie":"",
"Host":"twitter.com",
"Referer":"https://twitter.com/search",
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"
}

user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
         'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0', \
         'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
         'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
         'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', \
         'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36', \
         'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

logpath = "./log/"

logfile = "%s.log" % time.strftime('%Y%m%d-%H%M',time.localtime(time.time()))

timeout = 240 #http请求的timeout(秒)

imageLoader_process_cnt = 6 #下载图片的进程数p

query_home = "./etc/query.txt" #query集合文件，一行一个query；必须是utf8编码

finished_home = "./etc/finished.txt" #完成下载的query集合文件，一行一个query；必须是utf8编码

error_image_home = "./log/unfinished.txt"#下载失败的图片写入日志

url_list = "./log/urls.txt"

time_wait = 2 #向搜索引擎发情请求的时间间隔

try_cnt = 1 #图片下载错误，重试次数

########需要配置项
conf = ConfigParser.ConfigParser()
conf.read("./etc/spider.conf")

imgdir = conf.get("Download", "download_path")

image_path = "./img_download/%s/" % imgdir
#下载图片的存储路径

image_cnt = string.atoi(conf.get("Download", "image_cnt"))
#image_cnt =10 #一个query在每个搜索引擎上请求的图片数量

face = string.atoi(conf.get("Download", "face"))
#face = 0 #下载的图片是否为人，可选值1/0；1为人脸图片，0为默认非人脸图片

spider_source_str = conf.get("Download", "spider_source_str")
spider_source = spider_source_str.split(',')

image_type_str = conf.get("Download", "image_type_str")
image_type = tuple(image_type_str.split(','))

date_min, date_max = conf.get("Download", "date_range_str").split('-')

#spider_source = ["baiduSpider", "googleSpider", "bingSpider", "yahooSpider", "flickrSpider", "twitterSpider"]#搜索引擎的可选值
#spider_source = ["flickrSpider"] #搜索引擎

#image_size = [(400,400),(500,500),(600,600),(640,480),(800,600),(1024,768),(1600,1200),(2272,1704),(1024,1024),(800,800),(900,900),(1000,1000),(450,450)]
#image_size = [('400','400'),('500','500'),('600','600'),('640','480'),('800','600'),('1024','768'),('1600','1200'),('2272','1704'),('1024','1024'),('800','800'),('900','900'),('1000','1000'),('450','450')]

image_size_str = conf.get("Download", "image_size_str")
try:
    image_size = map(lambda x: (x.split(',')[0], x.split(',')[1]), image_size_str.split(';'))
except:
    image_size = []
