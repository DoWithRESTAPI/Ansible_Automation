#!/bin/python
import boto3
import paramiko
import botocore
import os
import sys
import platform
from creation_of_required_AnsController_AnsClient_Servers_1 import *
from  exchange_ssh_keys4_with_clients import *
from generate_ssh_key_on_ans_controller_3 import *
def clear():
        os.system('clear')
        return None

def welcome():
        print"=========================================================================================================="
        print"This will install ansible on  AnsController server and also creates a key exchange script on AnsController "
        print"=========================================================================================================="
        return None
def run_commands(ans_dns):
        key = paramiko.RSAKey.from_private_key_file("DevOps.pem")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                client.connect(hostname=ans_dns, username="ec2-user", pkey=key)
                #sudo yum update -y
                cmds=['sudo yum install http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm  -y','sudo yum install ansible -y' ]
                for each in cmds:
                        print "command is: ",each
                        stdin, stdout, stderr = client.exec_command(each)
                        print each," out is: ",stdout.read()
                client.close()
        except Exception as e:
                print e
                sys.exit(2)
        return None
def main():
    clear()
    welcome()
    ec2_conn=get_connection()
    ans_id,ans_private_ip,ans_dns=get_ip_dns(ec2_conn)
    run_commands(ans_dns)
if __name__ == '__main__':
        main()

