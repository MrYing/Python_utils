#coding:utf-8
#!/usr/bin/python
'''
command methods  

@author: Administrator
'''
import paramiko
import pexpect
import logging

paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
paramiko.util.log_to_file('/tmp/ssh.log')

def ssh2(host,cmd):  
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        ssh.connect(host,username='root',port = 22,timeout=60)
        logging.info(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)        
        info = stdout.readlines()
        logging.info(info)
        logging.info(stderr.readlines())
        ssh.close()
        
    except Exception,e:  
        logging.info(e)
    print info    
    return info


def ssh2_trust(host,cmd):  
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())        
        ssh.connect('vq12zdfb01',username='root',password='Root@dnt01',port = 22,timeout=60)
        logging.info(cmd)
        stdin, stdout, stderr = ssh.exec_command('ssh -vv '+ host +' " '+cmd +' "')        
        info = stdout.readlines()
        logging.info(info)
        logging.info(stderr.readlines())
        ssh.close()
        
    except Exception,e:  
        logging.info(e)
        
    return info

def ssh2_deploy(host,username,password,cmd):  
    print "============host,username#=###======================"
    print host
    print username
    print password
    try:
        out_info = ''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(host,username=username, password=password,port = 22,timeout=2000)
        logging.info(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out_info = stdout.readlines()
        logging.info(out_info)        
        
    except Exception,e:  
        logging.info(e)
        
    return out_info

def ssh2_deploy_log(host,username,password,cmd):
    try:
        out_info = []
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host,username=username, password=password,port = 22,timeout=2000)
        logging.info(cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out_info = stdout.read().decode('gbk','ignore').encode('utf-8');

    except Exception,e:
        logging.info(e)
    print out_info
    return out_info

import select
def ssh2_deploy_wait(host,username,password,cmd):  
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(host,username=username, password=password,port = 22,timeout=1200)
        
        channel = ssh.get_transport().open_session()
        logging.info(cmd)
        channel.exec_command(cmd)
        while True:
            if channel.exit_status_ready():
                break
            rl, wl, xl = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                logging.info(channel.recv(1024))
        
        channel.close()
        ssh.close()
        
    except Exception,e:  
        logging.info(e)

def sftp2(hostname,username,password,localfile,remotefile):
    try:
        
        username_deploy = username
        password_deploy = password
        transport = paramiko.Transport((hostname,22)) 
        transport.connect(username = username_deploy, password = password_deploy) 
        sftp = paramiko.SFTPClient.from_transport(transport) 
        sftp.put(localfile,remotefile) 
        logging.info(localfile,remotefile)
        transport.close()  
        
    except Exception,e:  
        print(e)
        
def establishtrust(ip,hostname):
    
    pexpect.TIMEOUT(5)
    #append hosts info to /etc/hosts
    logging.info(hostname)
    logging.info(ip)
    ssh_root = pexpect.spawn('su - root',timeout=5) 
    index1 = ssh_root.expect(['(?i)password:',pexpect.EOF,pexpect.TIMEOUT])
    logging.info(index1)
    if(index1==0):    
        ssh_root.sendline('Root@dnt01')
    ssh_root.expect('vq12zdfb01:~ #')
    ssh_root.sendline('/bin/sh -c "echo %s  %s >> /etc/hosts"' % (ip,hostname))
    ssh_root.expect('vq12zdfb01:~ #')
    ssh_root.delaybeforesend = 0.1   
    ssh_root.sendline('/bin/sh -c "/usr/bin/ssh-copy-id -o StrictHostKeyChecking=no -o ConnectTimeout=5 -i /root/.ssh/id_rsa.pub  root@%s ";' % (ip))
    try:
        index2= ssh_root.expect(['(?i)password:','vq12zdfb01:~ #',pexpect.TIMEOUT])
        logging.info('2'+str(index2))
        if(index2==0):
            ssh_root.sendline('Root@dnt01')
            index4 = ssh_root.expect(['(?i)password:','vq12zdfb01:~ #'])
            logging.info('4'+str(index4))
            if (index4 == 0):
                ssh_root.sendline('Root_dnt01')
                                                   
    except pexpect.EOF,pexpect.TIMEOUT:
        ssh_root.close()

'''
def main():
  host_ip="192.168.91.132"
  username="tapp"
  password_user="tapp!Pass"
  logfile_req="appsrv01-20161008.log"
  line_req="1"
  linenumber=1
  script_name = "start-appsrv01.sh"
  #ssh2("192.168.91.132","uptime")
  #ssh2_deploy("192.168.91.132","root","rootroot","uptime")
  #ssh2_dep = ssh2_deploy(host_ip, username, password_user, r'/home/tapp/'+script_name+' 2>&1 & ;')
  #ssh2_deploy_log(host_ip, username, password_user, r"line=`wc -l "+logfile_req+"|awk '{print $1}'`;echo ${line};sed -n "+line_req+",${line}p "+logfile_req+"")
  ssh2_deploy_log(host_ip, username, password_user, r"a=`wc -l deploy.log | awk '{print $1}'`;echo ${a};sed -n "+str(linenumber)+",${a}p deploy.log")

if __name__ == '__main__':
    main()
'''
