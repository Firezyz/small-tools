#!/bin/bash
e="sys-sre-test02-zyz"
m="test.metric1"
t="t0=tag0,t1=zyz,t2=tag2"
ts=`date +%s`
curl -s -X POST -d "[{\"metric\":\"$m\", \"endpoint\":\"$e\", \"timestamp\":$ts,\"step\":10, \"value\":9, \"counterType\":\"GAUGE\",\"tags\":\"$t\"
}]" "http://10.4.243.27:6060/api/push" | python -m json.tool
