#!/usr/bin/python
#coding=utf8
'''
Created on 2015.04.09
@author: Administrator
'''
import os
import re
import time
import urllib
from collections import OrderedDict
from multiprocessing import freeze_support, Process, Queue, Lock

import configure
import baseSpider
import imageLoader
import set_demon
from mylog import logger

_global_lock = Lock()
_global_start_flag = False
_last_flag = False

class processDispatch(object):
    def __init__(self):
        self.imageLoader = imageLoader.imageLoader()
        self.query_max = set([query.strip() for query in open(configure.query_home, "r")])
        self.query_min = set([query.strip() for query in open(configure.finished_home, "r")])
        self.query_set = self.query_max - self.query_min
        self.url_queue = Queue()

    # singleton
    @staticmethod
    def instance():
        with _global_lock:
            if not hasattr(processDispatch, "_instance"):
                processDispatch._instance = processDispatch()
                return processDispatch._instance
            return processDispatch._instance

    def _queryProcessFunc(self):
        num = 0
        end_flag = False
        logger.info('queryProcess')
        for query in self.query_set:
            query = query.decode("utf-8-sig").encode("gbk")
            logger.info("query now is : %s" % query)
            if end_flag:
                break
            num += 1
            logger.info("query num is : %s" % num)
            urls = []
            if "baiduSpider" in configure.spider_source:
                urls.extend(baseSpider.baiduSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            if "googleSpider" in configure.spider_source:
               urls.extend(baseSpider.googleSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            if "yahooSpider" in configure.spider_source:
                urls.extend(baseSpider.yahooSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            if "bingSpider" in configure.spider_source:
                urls.extend(baseSpider.bingSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            if "flickrSpider" in configure.spider_source:
                urls.extend(baseSpider.flickrSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            if "twitterSpider" in configure.spider_source:
                urls.extend(baseSpider.twitterSpider(timeout=10).get_result(configure.image_cnt, urllib.quote_plus(query)))
            else:
                print ("falied")
            cnt = 0

            try:
                logger.info("cnt of url is:"+str(len(urls)))
                dic = OrderedDict()
                try:
                    for url in urls:
                        #url = "".join([re.split("jpg|png|gif", url)[0], "jpg"])
                        dic[url] = 0
                except Exception as e:
                    logger.error(e)
                url_set = dic.keys()
                logger.info("cnt of url is:"+str(len(url_set)))
                for url in url_set:
                    cnt += 1
                    if not url.endswith(configure.image_type):
                        continue
                    if cnt == len(url_set):
                        if num == len(self.query_set):
                            self.url_queue.put((query, url, cnt, -1))   #全体任务结束
                            end_flag = True
                            break
                        self.url_queue.put((query, url, cnt, 0))        #单个任务结束
                    else:
                        self.url_queue.put((query, url, cnt, 1))        #普通任务
            except Exception as e:
                logger.error(e)

    def _imageProcessFunc(self):
        global _last_flag
        while True:
            # print self.url_queue.qsize()
            url_info = self.url_queue.get()
            query = url_info[0]
            url = url_info[1]
            no = url_info[2]
            flag = url_info[3]
            try:
                image_type = "." + url.split(".")[-1][:3]
                filepath = os.path.join(configure.image_path, query)
                filename = os.path.join(filepath, query+str(no)+image_type)
                self.imageLoader.down_load_image(filepath, filename, url, configure.try_cnt)
                with _global_lock:
                    with open(configure.url_list, "a+") as f:
                        f.write(filename+"\t"+url+"\n")
                if flag == 1:
                    pass
                elif flag == 0:
                    with _global_lock:
                        with open(configure.finished_home, "a+") as f:
                            f.write(query+"\n")
                else:
                    self.url_queue.put(url_info)
                    with _global_lock:
                        if not _last_flag:
                            _last_flag = True
                            with open(configure.finished_home, "a+") as f:
                                f.write(query+"\n")
                    break
            except Exception as e:
                logger.error(e)

    def start(self):
        '''
        @brief:该方法只能调用一次,启动spider
        '''
        global _global_start_flag
        with _global_lock:
            if _global_start_flag:
                raise AttributeError("start() already started 该方法只能调用一次")
            _global_start_flag = True
        freeze_support()
        query_proc = Process(target=self._queryProcessFunc, args=())
        query_proc.start()
        # self._queryProcessFunc()
        process_list = []
        for i in xrange(configure.imageLoader_process_cnt):
            freeze_support()
            child_proc = Process(target=self._imageProcessFunc, args=())
            process_list.append(child_proc)
            child_proc.start()
        for proc in process_list:
            proc.join()
        query_proc.join()
        print("end with success")


if __name__ == "__main__":
    #set_demon.daemonize(stdout='../log/stdout.log', stderr='../log/stderr.log')
    logger.info("I am Here!!!")
    a = time.time()
    processDispatch.instance().start()
    print time.time()-a
