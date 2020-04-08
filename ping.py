#!/usr/local/python38/bin/python3.8
import os
import time
import logging
import paramiko
import getpass

passwd = getpass('Enter your password >> ')

switch = 0
result = open('result.txt','w+',encoding='UTF-8')
logging.basicConfig(
    filename='ping.txt',
    level=logging.WARNING,
    format='[%(asctime)-10s] %(message)s'
)

def ssh2():
    command_list = [ 
    'neigh_show arp \n',
    'dev_cfg l3 sw8_0 route show;dmesg -c \n',
    'dev_cfg l3 sw8_0 route show 15750 16000;dmesg -c \n',
    'dev_cfg l3 sw8_0 route show 16000 16500;dmesg -c \n',
    'dev_cfg l3 sw8_0 host show;dmesg -c \n',
    'dev_cfg l3 sw8_0 arp show;dmesg -c \n',]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname='172.16.200.1',port=22000,username='conplat',password=passwd)
    except:
        print('Connect error Please check your configurationinfomation')
    remote_shell = client.invoke_shell()
    remote_shell.send('su \n')
    time.sleep(0.1)
    remote_shell.send(passwd)
    for comm in command_list:
        result.writelines('\033[1;31m------{}--------\033[0m'.format(comm))
        remote_shell.send(comm)
        time.sleep(0.2)
        while True:
            show_result = remote_shell.recv(65535)
            result.write(show_result.decode())
            if show_result.decode().endswith('root@THY_Access-SW ~$ '):
                break
while True:
    for i in range(1,21):
        IP = '10.200.{}.1'.format(i)
        ping_result = os.system('ping -c 2 {} >> /dev/null'.format(IP))
        if ping_result:
            print('{} is not ok '.format(IP))
            logging.warning('{} is not ok'.format(IP))
            switch += 1
        else:
            logging.warning('{} is ok'.format(IP))
    time.sleep(10)
    if switch == 4:
        ssh2()
#        switch = False



