import re
from datetime import datetime

logline = '''172.17.0.1 - - [24/May/2020:03:09:02 +0000] "GET /assets/fonts/material-icons.css HTTP/1.1" 200 873 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37" "-"'''

pattern = '''(?P<remoteIP>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]+" "(?P<UserAgent>[^"]+)"'''
regex = re.compile(pattern)

def extract(line):
    matcher = regex.match(line)
#    return matcher.groupdict()
    info = None
    if matcher:
        info = {k:ops.get(k,lambda x: x)(v) for k,v in matcher.groupdict(logline).items()}
    return info

ops = {
    'datetime':lambda timestr: datetime.strptime(timestr,"%d/%b/%Y:%H:%M:%S %z"),
    'status':int,
    'size':int,
    'request':lambda request: dict(zip(('method','url','protocol'),request.split()))
}

# wordict = {k:ops.get(k,lambda x: x)(v) for k,v in extract(logline).items()}
# 这里这个lambda x: x是因为get方式去获取一个key的时候不存在给的默认值无论如何都是一个str对象是没有()调用的,所以给了一个lambda,当给函数的时候返回一个函数去调用v,当给一个字符的时候就返回一个字符串

with open(r"C:\Free\Script\TMP\log") as f:
    for line in f:
        wordict = extract(line)
        if wordict:
            print(wordict['remoteIP'])
        else:
            print("Not pattern")
            continue