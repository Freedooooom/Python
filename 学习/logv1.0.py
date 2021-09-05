import datetime

# 日志文件:
logline = '''183.60.212.153 - - [19/Feb/2013:10:23:29 +0800]\
    "GET /o2o/media.html?menu=3 HTTP/1.1" 200 16691 "-" \
    "Mozilia/5.0 (compatible; EasouSpider; +http://www.easou.com/search/spider.html)"'''

wordlist = []
tmp = ''
flag = False            # 设置一个开关,如果是以",]开头的进入一种循环处理,如果不是进入另一个循环处理
for word in logline.split():
    if not flag and (word.startswith('"') or word.startswith('[')) and (not word.endswith('"')):
        tmp = word[1:]
        flag = True     #判断是以",]开头打开这个开关
        continue
    if flag:
        if word.endswith('"') or word.endswith(']'):
            tmp += ' ' + word[:-1]      # 为了阅读方便添加了一个空格
            wordlist.append(tmp)
            tmp = ""
            flag = False        # 处理完毕,关闭这个开关
            continue
        else:
            tmp += " " + word
            continue
    word = word if not word.endswith('"') else word[:-1]    # 处理 "-" 这种字符串
    tmp = word if not word.startswith('"') else word[1:]
    wordlist.append(tmp)
''' ['183.60.212.153', '-', '-', '19/Feb/2013:10:23:29 +0800', 'GET /o2o/media.html?menu=3 HTTP/1.1', '200', '16691', '-', 
'Mozilia/5.0 (compatible; EasouSpider; +http://www.easou.com/search/spider.html)']'''


def Convert_time(timestr):
    # 19/Feb/2013:10:23:29 +0800
    fmtstr = "%d/%b/%Y:%H:%M:%S %z"
    return datetime.datetime.strptime(timestr,fmtstr)

def Convert_request(request:str):
    return dict(zip(('method','url','protocol'),request.split()))


names = ['remoteIP ','','','datetime','request','status','size','','UserAgent']
ops = [None,None,None,Convert_time,Convert_request,int,int,None,None]      # 可以使用这个方法将多个数据按照不同方式压缩成一个字典

wordict= {}
for Num,word in enumerate(wordlist):
    key = names[Num]
    if ops[Num]:
        wordict[key] = ops[Num](word)
    else:
        wordict[key] = word
    
print(wordict)