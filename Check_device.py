import paramiko
import time
import getpass
import socket


def ssh2(comm_list:list,hostname='192.168.0.1',User='admin',Passwd='admin_default',Port='22'):
    SSH = paramiko.SSHClient()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH.connect(hostname,username=User,password=Passwd,port=Port)
    remote = SSH.invoke_shell()
    logfile = open('log_{}.txt'.format(hostname),mode='w+',encoding='utf-8')
    remote.send('terminal line 0 \n')
    for comm in comm_list:
        remote.send(comm)
        while True:
            time.sleep(1)
            result = remote.recv(65535)
            logfile.writelines(result.decode('utf-8'))
            if result.decode('utf-8').endswith('>'):
                break
        time.sleep(1)
        print('\033[1;3m command {} executed successfully \033[0m'.format(comm))
    else:
        SSH.close()
        logfile.close()

if __name__ == '__main__':
    comm_list = [
        'show version \n',
        'show ip route \n',
        'show ip interface br \n',
        'show run \n'
    ]
    
    with open('TMP\IP.txt') as IP_list:
        for ip in IP_list:
            try:
                conn_parser = ip.split()
                ssh2(comm_list,hostname=conn_parser[0],User=conn_parser[1],Passwd=conn_parser[2])
            except TimeoutError as err:
                print('connect {} falied'.format(conn_parser[0]))
                continue