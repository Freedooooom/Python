import re
from datetime import datetime

logline = '''183.60.212.153 - - [19/Feb/2013:10:23:29 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 16691 "-" "Mozilia/5.0 (compatible; EasouSpider; +http://www.easou.com/search/spider.html)"'''

pattern = '''(?P<remoteIP>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]+" "(?P<UserAgent>[^"]+)"'''
regex = re.compile(pattern)

def extract(line):
    matcher = regex.match(line)
#    return matcher.groupdict()
    if matcher:
        return {k:ops.get(k,lambda x: x)(v) for k,v in matcher.groupdict(logline).items()}

ops = {
    'datetime':lambda timestr: datetime.strptime(timestr,"%d/%b/%Y:%H:%M:%S %z"),
    'status':int,
    'size':int,
    'request':lambda request: dict(zip(('method','url','protocol'),request.split()))
}

# wordict = {k:ops.get(k,lambda x: x)(v) for k,v in extract(logline).items()}
# 这里这个lambda x: x是因为get方式去获取一个key的时候不存在给的默认值无论如何都是一个str对象是没有()调用的,所以给了一个lambda,当给函数的时候返回一个函数去调用v,当给一个字符的时候就返回一个字符串

with open("/var/log/local_access_log") as f:
    for line in f.readline():
        wordict = extract(line)
        if wordict:
            print(wordict[UserAgent],wordict[remoteIP])
        else:
            print("Not pattern")
