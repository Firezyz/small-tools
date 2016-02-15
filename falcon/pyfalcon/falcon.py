#!/usr/bin/env python
# coding=utf-8
from push_data_to_mtfalcon import MtFalcon
mtFalcon = MtFalcon("http://10.4.243.27:6060/api/push")
mtFalcon.setTags("tag=zyz,test=zyz").setCounterType("GAUGE").setValue(5).setMetric('zyz-test-metric03').setEndpoint('zyz-test-point03').setStep(60).setSleepTime(60).start()
