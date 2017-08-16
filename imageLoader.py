#coding=utf8
'''
Created on 2015.04.09
@author: Administrator
'''

import urllib2
import os
from threading import Lock
from mylog import logger

import configure

_global_lock = Lock()

class imageLoader(object):
    def __init__(self):
        pass

    def down_load_image(self, filepath, filename, url, try_cnt):
        logger.debug("down_load_image [imageLoader]")
        logger.info("get url [imageLoader] : %s" % url)
        if try_cnt <= 0:
            with _global_lock:
                with open(configure.error_image_home, "a+") as f:
                    f.write(url+"\t"+filename+"\n")
            return
        #try:
            #filepath = filepath.decode("utf8").encode("gb2312")
            #filename = filename.decode("utf8").encode("gb2312")
        #except:
            #return
        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except:
                return
        req = urllib2.Request(url)
        req.add_header('User-agent', configure.user_agent_list[1])
        try:
            response = urllib2.urlopen(req, timeout=configure.timeout)
            res = response.read()
            if len(res) == 0:
                self.down_load_image(filepath, filename, url, try_cnt-1)
                return
            with open(filename, "wb") as jpg:
                jpg.write(res)
            logger.info("download\t"+filepath)
        except Exception as e:
            self.down_load_image(filepath, filename, url, try_cnt-1)
            logger.info("can't get image\t"+filepath)
            logger.error(e)
            return
