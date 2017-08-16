#coding=utf8
import os
import logging
import configure

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

logpath = configure.logpath
logfile = configure.logpath + configure.logfile

if not os.path.exists(logpath):
    try:
        os.makedirs(logpath)
    except Exception as e:
        print e

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
