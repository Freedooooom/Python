import re
import datetime
from queue import Queue
import threading
from pathlib import Path
from user_agents import parse

pattern = '''(?P<remoteIP>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]+" "(?P<UserAgent>[^"]+)"'''
regedate = re.compile(pattern)

ops = {
    'datetime':lambda timestr: datetime.datetime.strptime(timestr,"%d/%b/%Y:%H:%M:%S %z"),
    'status':int,
    'size':int,
    'request':lambda request: dict(zip(('method','url','protocol'),request.split())),
    'UserAgent': lambda useragent: parse(useragent)
}

def edatetract(line):
    '抽取关键信息生成字典'
    matcher = regedate.match(line)
#    return matcher.groupdict()
    info = None
    if matcher:
        info = {k:ops.get(k,lambda date: date)(v) for k,v in matcher.groupdict(line).items()}
    return info



# wordict = {k:ops.get(k,lambda date: date)(v) for k,v in edatetract(logline).items()}
# 这里这个lambda date: date是因为get方式去获取一个key的时候不存在给的默认值无论如何都是一个str对象是没有()调用的,所以给了一个lambda,当给函数的时候返回一个函数去调用v,当给一个字符的时候就返回一个字符串


def load(path:str):
    '加载文件内容,返回一个生成器'
    with open(path) as f:
        for line in f:
            wordict = edatetract(line)
            if wordict:
                yield wordict
            else:
                print("Not pattern")
                continue

def loadall(path:str):
    if Path(path).is_file():
        with open(path) as f:
            for line in f:
                wordict = edatetract(line)
                if wordict:
                    yield wordict
                else:
                    print("Not pattern")
                    continue
    if Path(path).is_dir():
        for file in Path(path).iterdir():
            if file.is_file():
                with open(str(file)) as f:
                    for line in f:
                        wordict = edatetract(line)
                        if wordict:
                            yield wordict
                        else:
                            print("Not pattern")
                            continue



def window(src:Queue,handler,width:int,interval:int):
    ''' 
    分析数据时间属性，按照需求返回数据
    src:数据源
    handler:处理函数
    width:时间窗口
    interval:滑动窗口 -每次滑动的时间
    '''
    start = datetime.datetime.strptime('1970/01/01 01:01:01 +0800','%Y/%m/%d %H:%M:%S %z')  # 滑动开始的时间
    current = datetime.datetime.strptime('1970/01/01 01:01:02 +0800','%Y/%m/%d %H:%M:%S %z')    # 滑动结束的时间
    delta = datetime.timedelta(seconds = width - interval)  # 将int转化为一个时间对象   #\delta时间(图中重复的时间https://freedom-1257717218.cos.ap-nanjing.myqcloud.com/MarkDown时间窗口.JPG)

    buffer = [] # 时间开始滑动的时候将数据放入一个容器内

    while True:
        date = src.get()

        if date:
            buffer.append(date)
            current = date['datetime']
        
        if (current - start).total_seconds() >= interval:
            handler(buffer)
            start = current

            buffer = [i for i in buffer if i['datetime'] > current - delta] # 当处理完成后重新生成这个容器数据

def dispatcher(src):
    # 队列列表
    queues = []
    threads = []

    def reg(handler,width,interval):
        q = Queue()
        queues.append(q)        # 每一个消费者注册的时候都会给这个消费者一个队列

        t = threading.Thread(target=window,args=(q,handler,width,interval))
        threads.append(t)

    def run():
        for t in threads:
            t.start()

            for date in src:
                for q in queues:
                    q.put(date)    #生成者将数据put入队列,然后由window函数Queues.get进行时间滑动,最后由handler函数进行处理
    
    return reg,run

# 什么都不做的测试handler
def donothing_handler(iterable):
    print(iterable)

# 统计状态码的handler
def status_handler(iterable):
    d = {}
    for i in iterable:
        key = i['status']
        if key in d.keys():
            d[key] += 1
        else:
            d[key] = 1
    print(d)

# 统计状态码的另一种实现
def status_handler1(iterable):
    d = {}
    for i in iterable:
        if d.get(i['status']):
            d[i['status']] += 1
        else:
            d[i['status']] = 1
    print(d)
def status_handler2(iterable):
    d = {}
    for i in iterable:
        if d.get(i['status']):
            d[i['status']] += 1
        else:
            d[i['status']] = 1

    valuesum = sum(d.values())
    for i in d.keys():
#        print({k:v/valuesum*100 for k,v in d.items()})
        print('{}的比重为{:.2f}'.format(i,d[i] // valuesum))

# User_Agent分析

#ua_dict = {}        # 将字典放在函数外部，每次在window函数中调用handler函数都会在字典中增加元素，这样就会让时间窗口失效。分析所有数据
def user_agent_handler(iterable:list):
    ua_dict = {}        # 将字典放在函数内部，每次在window函数中调用handler函数都会重新生成一个字典
    for i in iterable:
        ua = i['UserAgent']
        key = ''.join(ua.browser.family+ua.browser.version_string)
        if ua_dict.get(key,None):
            ua_dict[key] += 1
        else:
            ua_dict[key] = 1
    print(ua_dict)

reg,run = dispatcher(load(r'C:\Free\Script\TMP\log'))

reg(user_agent_handler,10,5)
run()

