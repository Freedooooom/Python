'''
    name:check.py
    Explian:
'''

def is_Zh(s):
    '检查给定字符串是否包含中文字符'
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False

def is_AllZh(s):
    '检查给定字符串是否是中文'
    for c in  s:
        if '\u4e00' <= c <= '\u9fa5':
            continue
        return False
    return True

def is_IP(ipAddr):
    '检查所给字符串是否为IP地址'
    import re
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:  
        return False


