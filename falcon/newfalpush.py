#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import logging
import time
import ConfigParser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import httplib
 
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

def postDataToUrl(data,url,port):
    logging.info("POSTDATATOURL")
    if data is None or len(data) == 0:
        logging.info("data is None or empty")
        return False
    httpClient = None
    try:
        params = urllib.urlencode(data)
        print params
        headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
        url = 'http://10.4.243.27'
        port = 6060
        httpClient = httplib.HTTPConnection(url, port, timeout=5)
        print httpClient
        httpClient.request("POST", "/api/push", params, headers)
     
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
        print response.getheaders() #获取头信息
        if response.status == 200:
            return True
        return False
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def getOnePostData(metric,endpoint,value,timestamp,step,counterType,tags,posturl,port):
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
    return dict(status=True,metric=metric,endpoint=endpoint,timestamp=timestamp,step=step,value=value,counterType=counterType,tags=tags,posturl=posturl,port=port);

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
        dataFromINI = getOnePostData(config.get(section,'metric'),config.get(section,'endpoint'),isUrlAvaliable(config.get(section,'url')),int(time.time()),config.getint(section,'step'),config.get(section,'counterType'),config.get(section,'tags'),config.get(section,'posturl'),config.get(section,'port'))
        if dataFromINI['status'] == True:
            postDatas.append(dataFromINI)
    return postDatas

def urlfalconJob(posturl,port):
    print postDataToUrl(urlPostData,posturl,port)
    if not postDataToUrl(urlPostData,posturl,port):
        logging.error('PUSH DATA FAIL')
        postDataToUrl(urlPostData,posturl,port)

urlPostTo = ""
blockingScheduler = getBlockingScheduler()
urlPostDataList = getResourceFromINI('./urlbalcon.ini')
for urlPostData in urlPostDataList:
    blockingScheduler.add_job(urlfalconJob,'interval',seconds=urlPostData['step'],args=[urlPostData['posturl'],urlPostData['port']])
blockingScheduler.start()
