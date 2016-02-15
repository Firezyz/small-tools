#!/usr/bin/env python
# coding=utf-8
import requests
import time
import json

while(True):
    ts = int(time.time())
    payload = [
        {
            "endpoint": "test-zyz-endpoint",
            "metric": "zyz-test-metric",
            "timestamp": ts,
            "step": 2,
            "value": 5,
            "counterType": "GAUGE",
            "tags": "location=beijing,service=zyz"
    },
    ]
    r = requests.post("http://10.4.243.27:6060/api/push",data=json.dumps(payload))
    print r.text
    time.sleep(2)
