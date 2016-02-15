#!/usr/bin/env python
# coding=utf-8
from push_data_to_mtfalcon import MtFalcon
import urllib

def isUrlAvaliable(url):
    response = urllib.urlopen(url)
    return response.getcode()


mtFalcon = MtFalcon("http://10.4.243.27:6060/api/push")
mtFalcon.setTags("tag=zhang,test=zhang").setCounterType("GAUGE").setMetric('zhang-test-metric').setEndpoint('zhang-test-point').setStep(30).setSleepTime(10).start()
