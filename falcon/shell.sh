#!/bin/bash
e="sys-sre-test02"
m="test.metric1"
t="t0=tag0,t1=zyz,t2=tag2"
ts=`date +%s`
curl -s -X POST -d "[{\"metric\":\"$m\", \"endpoint\":\"$e\", \"timestamp\":$ts,\"step\":60, \"value\":9, \"counterType\":\"GAUGE\",\"tags\":\"$t\"}]"  "10.4.243.27:8433/api/push" | python -m json.tool
