import paramiko
import time
import threading
import getpass
import socket
import check

def ssh2(hostname,CMD_List,Port=22,Username='admin',Password='admin_default'):
    SSH = paramiko.SSHClient()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        SSH.connect(hostname,username=Username,password=Password,port=Port)
    except socket.timeout as err:
        print(err,'Please check your configurationinfomation')
    print ('\033[1;31m Successfully connect to {} ! \033[0m'.format(hostname))
    remote_connection = SSH.invoke_shell()
    Logfile = open('log_{}.txt'.format(hostname),mode='w+',encoding='utf-8')
    remote_connection.send('terminal line 0 \n')
    for COMMAND in CMD_List:
        print ('\033[1;31m------{}--------\033[0m'.format(COMMAND))
        print(' ')
        remote_connection.send(COMMAND)
        time.sleep(1)
        while True:
            time.sleep(1)
            result = remote_connection.recv(65535)
            Logfile.writelines(result.decode())
            print(result)
            if result.decode().endswith('<DPX8000>'):
                break
        time.sleep(1)
    else:
        remote_connection.send('end \n')
        remote_connection.send('no terminal line \n')
        SSH.close()
        Logfile.close()

if __name__ == "__main__":
    Username = input('Please enter your username  >> ')
    Password = getpass.getpass('Your Password  >> ')
    IP_Address = ['59.48.111.185']
    Command_List = ['show version \n','show device \n','show slot information \n','show ip route \n','show interface status \n','show vlan \n','show ip interface brief \n','show run \n']
    for IP in IP_Address:
        check.is_IP(IP)
        ssh2(IP,CMD_List=Command_List,Port=2211,Password=Password)