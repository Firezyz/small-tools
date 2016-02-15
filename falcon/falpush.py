#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import logging
import time
import ConfigParser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

def getBlockingScheduler():
    executors = {
	'default': ThreadPoolExecutor(10),
	'processpool': ProcessPoolExecutor(5)
    }

    job_defaults = {
	'coalesce': False,
	'max_instances': 5
    }
    scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults)
    return scheduler

def postDataToUrl(data,url):
    logging.info("POSTDATATOURL")
    if data is None or len(data) == 0:
        logging.info("data is None or empty")
        return False
    postData = urllib.urlencode(data)
    req = urllib2.Request(url, postData)
    response = urllib2.urlopen(req)
    responseData = response.read()
    logging.info(responseData)
    if response.getcode() == 200:
        return True
    return False

def getOnePostData(metric,endpoint,value,timestamp,step,counterType,tags,posturl):
    if metric is None or len(metric) ==0:
        logging.error("GETONEPOSTDATA | metric is None or empty")
        return dict(status=False)
    if endpoint is None or len(endpoint) == 0:
        logging.error("GETONEPOSTDATA | endpoint is None or empty")
        return dict(status=False)
    if not isinstance(value,bool):
        if value is None or len(value) == 0:
            logging.error("GETONEPOSTDATA | value is None or empty")
            return dict(status=False)
    if counterType is None or len(counterType) == 0:
        logging.error("GETONEPOSTDATA | counterType is None or empty")
        return dict(status=False)
    if tags is None or len(tags) == 0:
        logging.error("GETONEPOSTDATA | tags is None or empty")
        return dict(status=False)
    return dict(status=True,metric=metric,endpoint=endpoint,timestamp=timestamp,step=step,value=value,counterType=counterType,tags=tags,posturl=posturl);

def isUrlAvaliable(url):
    try:
        response = urllib.urlopen(url)
        if response.getcode() == 200:
            return True
        return False
    except Exception,e:
        return False

def getResourceFromINI(resoursePath):
    config = ConfigParser.ConfigParser()
    config.read(resoursePath)
    postDatas = []
    for section in config.sections():
        dataFromINI = getOnePostData(config.get(section,'metric'),config.get(section,'endpoint'),isUrlAvaliable(config.get(section,'url')),time.time()*1000,config.getint(section,'step'),config.get(section,'counterType'),config.get(section,'tags'),config.get(section,'posturl'))
        if dataFromINI['status'] == True:
            postDatas.append(dataFromINI)
    return postDatas

def urlfalconJob(posturl):
    print postDataToUrl(urlPostData,posturl)
    if not postDataToUrl(urlPostData,posturl):
        logging.error('PUSH DATA FAIL')
        postDataToUrl(urlPostData,posturl)

urlPostTo = ""
blockingScheduler = getBlockingScheduler()
urlPostDataList = getResourceFromINI('./urlbalcon.ini')
for urlPostData in urlPostDataList:
    blockingScheduler.add_job(urlfalconJob,'interval',seconds=urlPostData['step'],args=[urlPostData['posturl']])
blockingScheduler.start()
