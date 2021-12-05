from os import rename
import dns.resolver
from dns.rdatatype import UnknownRdatatype
from dns.resolver import NoNameservers, query


class Query_Domin_Name():
    '''
    查询DNS记录,返回查询数据,以及查询时间
    Name: 查询的FQDN
    Query_Type: 查询的记录
    NameServer: 使用的DNS服务器,如果未指定则使用本机自身的DNS
        Unix     -->    /etc/resolv.conf
        windows  -->    请在注册表中查找 
    '''

    def __init__(self,FQDN,query_type='A') -> None:

        ''' 初始化函数并且做异常处理'''

        self.query_type = query_type
        self.FQDN = FQDN
        try:
            query_result = dns.resolver.resolve(FQDN,query_type,raise_on_no_answer=False)
            self.query_result = query_result
            if query_result.rrset is None:
                print ('{} 没有对应的{}记录，请核实'.format(FQDN,query_type))
        except UnknownRdatatype as e:
            print ('请输入正确的类型')
        except Exception:
            print('请检查你的输入是否正确')
        except NoNameservers as e:
            print('请检查网络或者DNS配置')

    def getresult(self):

        ''' 根据类型获取结果 '''

        for query in self.query_result.response.answer:
            for item in query:
                if self.query_type == 'A':
                    return ('{}的{}记录是{}'.format(self.FQDN,self.query_type,item.address))
                elif self.query_type == 'SOA':
                    return ('{}的授权服务器是{},E-mail是{}'.format(self.FQDN,item.mname,item.rname))
                elif self.query_type == 'MX':
                    print('邮件MX记录的优先级越高,它的数值越小')
                    return ('{}的邮件服务器是{},它的优先级是{}.'.format(self.FQDN,item.exchange,item.preference))
                elif self.query_type == 'NS':
                    return ('{}域名的别名记录是{}'.format(self.FQDN,item.to_text()))















        


        


test = Query_Domin_Name('www.baidu.com','A')
print (test.getresult())
