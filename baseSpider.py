#coding=utf8
'''
Created on 2015.4.9
@author: Administrator
'''
import re
import time
import json
import random
import urllib
import urllib2
import cookielib

import lxml
import lxml.html as HTML
import flickrapi


import configure
from configure import image_size
from cookielib import CookieJar
from mylog import logger

class spider(object):
	def __init__(self, timeout=configure.timeout, kwargs={}):
		self.http_header = configure.http_header
		self.http_header.update(kwargs)
		self.timeout = timeout
		cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
		opener = urllib2.build_opener(cookie_support)
		urllib2.install_opener(opener)
		'''
		self.http_header = configure.http_header
		self.http_header.update(kwargs)
		self.timeout = timeout
		cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
		httpHandler = urllib2.HTTPHandler(debuglevel=0)      #
		httpsHandler = urllib2.HTTPSHandler(debuglevel=0)    #
		proxy = urllib2.ProxyHandler({'http': '169.55.141.101:8080'})
		opener = urllib2.build_opener(cookie_support, proxy)
		urllib2.install_opener(opener)
		'''

	def get_image_url_list(self, pattern, url):
		logger.debug("get_image_url_list 1")
		logger.info("get url : %s" % url)

		time.sleep(configure.time_wait)

		req = urllib2.Request(url, None, self.http_header)
		try:
			http_response = urllib2.urlopen(req, timeout=40).read()
			print http_response
			return re.findall(pattern, http_response)
		except Exception as e:
			logger.error(e)
			return []

	def get_result(self, image_cnt, query, pattern):
		"""
		@param image_cnt:需要的图片数量
		@param query:关键词
		@param pattern:抽取url的正则表达式
		"""
		raise NotImplementedError()


class bingSpider(spider):
	bing_thumb_xpath = "//a[@class='thumb']/@href"
	count_per_page = 28

	def __init__(self, timeout=configure.timeout):
		kwargs = configure.bing_header
		super(bingSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern="(?<=imgurl:&quot;)http:[^;]+?\.?(?:jpg|png)"):
		result = []
		i = 0
		while len(result) < image_cnt:
			url = "http://cn.bing.com/images/search?q=%s&first=%d&count=%d&FORM=IBASEP" % (query, i*self.count_per_page+1, self.count_per_page)
			result.extend(self.get_image_url_list(pattern, url))
			i += 1
		return result

	def get_image_url_list(self, pattern, url):
		logger.debug("get_image_url_list [bingSpider]")
		logger.info("get url [bingSpider] : %s" % url)
		time.sleep(configure.time_wait)

		try:
			cj = CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			http_response = opener.open(url).read()
			html = lxml.html.fromstring(http_response)
			return html.xpath(self.bing_thumb_xpath)

		except Exception as e:
			logger.error(e)
			return []

class yahooSpider(spider):
	def __init__(self, timeout=configure.timeout):
		kwargs = configure.yahoo_header
		super(yahooSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern="imgurl=(.*?)&rurl="):
		result = []
		for i in xrange(image_cnt/60+1):
			rand = str(time.time()).split(".")[0] + str(random.randint(100,999))
			b = i*60 + 1
			spos = i * 12
			url = "http://sg.images.search.yahoo.com/search/images?n=60&ei=UTF-8&fr=sfp&fr2=sa-gp-sg.images.search.yahoo.com&o=js&p=%s&tab=organic&tmpl=&nost=1&b=%s&iid=Y.%s&ig=6a0a89ab1b384c948100000000f3e811&spos=%s&&rand=%s"%(query, str(b), str(i), str(spos), rand)
			result.extend(self.get_image_url_list(pattern, url))
		return ["http://"+urllib.unquote(url) for url in result]


class baiduSpider(spider):
	baidu_dataobj_xpath = "//div[@class='imgpage']/ul/li[@class='imgitem']"
	count_per_page = 30

	def __init__(self, timeout=configure.timeout):
		kwargs = configure.baidu_header
		super(baiduSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern="objURL\":\"(http://.*?)\","):
		result = []

		for i in xrange(image_cnt/self.count_per_page+1):
			url = "http://image.baidu.com/search/index?tn=baiduimage&face={face}&istype=2&ie=utf-8&word={q}&pn={start}&rn={cnt}".format(q=query, face=configure.face, cnt=self.count_per_page, start=self.count_per_page*i)
			result.extend(self.get_image_url_list(pattern, url))

		return result


class googleSpider(spider):
	base_url = 'https://www.google.com/search?'
	count_per_page = 100
	google_image_limit = 1000

	def __init__(self, timeout=configure.timeout):
		kwargs = configure.google_header
		super(googleSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern="\"ou\":\"(.*?)\""):
		result = []

		if image_cnt > self.google_image_limit:
			logger.debug('Due to Google\'s limitation, you can only get the first '
			'1000 result. "image_cnt" has been automatically set to the max value. '
			'If you really want to get more than 1000 results, you '
			'can specify different date ranges.')
			image_cnt = self.google_image_limit

		for i in range(0, image_cnt, self.count_per_page):
			cd_min = date_min.strftime('%d/%m/%Y') if configure.date_min else ''
			cd_max = date_max.strftime('%d/%m/%Y') if configure.date_max else ''

			tbs = 'cdr:1,cd_min:{},cd_max:{}'.format(cd_min, cd_max)
			# tbs = 'isz:ex,iszw:{},iszh:{}'.format(width, height)
			params = dict(
				q=query, ijn=int(i / self.count_per_page), start=i, tbs=tbs, tbm='isch')
			url = self.base_url + urllib.urlencode(params)
			result.extend(self.get_image_url_list(pattern, url))

		return result

	def get_image_url_list(self,pattern,url):
		logger.debug("get_image_url_list [googleSpider]")
		logger.info("get url [googleSpider] : %s" % url)
		time.sleep(configure.time_wait)
		req = urllib2.Request(url, None, self.http_header)

		try:
			http_response = urllib2.urlopen(req,timeout=self.timeout).read()
			html = lxml.html.fromstring(http_response)
			image_divs = html.xpath("//div[@class='rg_meta']")

			url_result = []
			for item in image_divs:
				meta = json.loads(item.text)
				if 'ou' in meta:
					url_result.append(meta['ou'])
			return url_result

		except Exception as e:
			logger.error(e)
			return []

class flickrSpider(spider):
	def __init__(self, timeout=configure.timeout):
		kwargs = configure.flickr_header
		super(flickrSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern='url_.*?:"(.*?.jpg)'):
		result = []
		i = 1

		# while len(result) < 4000 and  len(result) < image_cnt:
		while len(result) < image_cnt:
			#print('*'*50)
			url = "https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=11&extras=can_comment,count_comments,count_faves,isfavorite,license,media,needs_interstitial,owner_name,path_alias,realname,rotation,url_c,url_l,url_m,url_n,url_q,url_s,url_sq,url_t,url_z&per_page=100&page=%d&lang=zh-Hant-HK&text=%s&method=flickr.photos.search&api_key=2291ba82f1bdd163733aae69399f709f&format=json&hermes=1&hermesClient=1&nojsoncallback=1" % (i,query)
			urlList = self.get_image_url_list(pattern,url)
			result.extend(urlList)
			#print('~'*50,len(result))
			i += 1
		return result

	def get_image_url_list(self,pattern,url):
		logger.debug("get_image_url_list [flickrSpider]")
		logger.info("get url [flickrSpider] : %s" % url)
		time.sleep(configure.time_wait)
		flickr_date = urllib.urlencode(configure.flickr_date)
		req = urllib2.Request(url,flickr_date,self.http_header)
		try:
			http_response = urllib2.urlopen(req,timeout=self.timeout).read()
			info = json.loads(http_response)['photos']['photo']
			#  print info
			url_result = []
			for item in info:
				if item.has_key('url_z'):
					new_url = item['url_z']
				elif item.has_key('url_m'):
					new_url = item['url_m']
				url_result.append(new_url)
			return url_result
		except Exception as e:
			logger.error(e)
			return 1,[]

class twitterSpider(spider):
	def __init__(self, timeout=configure.timeout):
		kwargs = configure.twitter_header
		super(twitterSpider, self).__init__(timeout, kwargs)

	def get_result(self, image_cnt, query, pattern=r"https:\/\/pbs.twimg.com\/media\/.+\.?(?:jpg|png)"):
		i = 1
		result = []
		count = 0

		# first url
		url = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1'%query
		logger.info("get url [twitterSpider] : %s" % url)

		# get image list from url response json
		response = urllib2.urlopen(url)
		data = json.load(response)
		html = data['items_html']
		imgs = set(re.findall(pattern, html))

		count += len(imgs)
		result.extend(imgs)

		# find second url in first url response json
		begin = html.rfind('data-tweet-id') + 15
		last = begin + 18
		nexturl = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1&max_position=TWEET-%s'%(query, html[begin:last])

		while count < image_cnt:
			time.sleep(configure.time_wait)
			response = urllib2.urlopen(nexturl)
			data = json.load(response)
			# find next url in current url response json
			nexturl = 'https://twitter.com/i/search/timeline?q=%s&src=typd&vertical=default&f=images&include_available_features=1&include_entities=1&max_position='%query + data['min_position']

			logger.info("get nexturl [twitterSpider] : %s" % nexturl)
			# get image list from url response json
			html = data['items_html']
			imgs = set(re.findall(pattern, html))
			if len(imgs)==0:
				break
			count += len(imgs)
			result.extend(imgs)
		return result

def test():
	baidu = googleSpider()
	urls = baidu.get_result(200, urllib.quote_plus("Bonjour store"))
	print urls,len(urls)

if __name__ == "__main__":
	test()
