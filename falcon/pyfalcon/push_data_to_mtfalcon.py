#!/usr/bin/env python
# coding=utf-8
import requests
import time
import json
import traceback
import urllib

class MtFalcon(object):
    url=''
    data={}
    postData=[]
    step=None
    endpoint=''
    metric=''
    value=None
    counterType=''
    tags=''
    sleepTime=None
    
    def __init__(self,url):
        self.url=url

    def initData(self,url,data):
        self.url=url
        self.postData=data
        return self

    def setStep(self,step):
        self.step=step
        return self
    
    def setSleepTime(self,sleepTime):
        self.sleepTime=sleepTime
        return self

    def setEndpoint(self,endpoint):
        self.endpoint=endpoint
        return self

    def setMetric(self,metric):
        self.metric=metric
        return self

    def setValue(self,value):
        self.value=value
        return self

    def setCounterType(self,counterType):
        self.counterType=counterType
        return self

    def setTags(self,tags):
        self.tags=tags
        return self

    def confirmParams(self):
        if self.step is None or len(self.endpoint)==0 or len(self.metric)==0 or self.value is None or len(self.counterType)==0:
            return False
        return True

    def confirmPostInfo(self):
        if len(self.url)==0 or len(self.postData)==0 or self.sleepTime is None:
            return False
        return True

    def constructPostData(self):
        if not self.confirmParams():
            raise Exception("参数不满足")
        self.data['endpoint']= self.endpoint
        self.data['step']=self.step
        self.data['metric']=self.metric
        self.data['value']=self.value
        self.data['counterType']=self.counterType
        self.data['tags']=self.tags
        self.data['timestamp']=int(time.time())
        self.postData.append(self.data)
        self.postData=json.dumps(self.postData)
        
    def flush(self):
        if len(self.url)!=0:
            self.url=''
        if len(self.postData)!=0:
            self.postData=[]
        if self.sleepTime:
            self.sleepTime=None
        if len(self.data) !=0:
            self.data=''
        if self.step:
            self.step=None 
        if len(self.endpoint)!=0: 
            self.endpoint=''
        if len(self.metric)!=0: 
            self.metric=''
        if self.value:
            self.value=None
        if len(self.counterType)!=0:
            self.counterType!=''
        if len(self.tags)!=0:
            self.tags=''

    def isUrlAvaliable(self,url):
        response = urllib.urlopen(url)
        return response.getcode()
            

    def start(self):
        self.value=self.isUrlAvaliable('http://jipiao.31jipiao.com/')
        print self.value
        try:
            if len(self.postData)==0:
                self.constructPostData()
            if not self.confirmPostInfo():
                raise Exception("url或者data或sleepTime为空")
            while(True):
                print self.url,self.postData
                response = requests.post(self.url,self.postData)
                print response.text
                response = json.loads(response.text); 
                if not ('msg' in response and response['msg'] == 'success'):
                    raise Exception("push失败")
                time.sleep(self.sleepTime)
        except Exception,e:
            print traceback.format_exc()
        finally:
            self.flush()
