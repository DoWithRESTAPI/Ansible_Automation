#!/bin/python
import boto3
import paramiko
import botocore
from creation_of_required_AnsController_AnsClient_Servers_1 import *

def clear():
        os.system('clear')
        return None

def welcome():
        print"====================================================================="
        print"It will create ssh key paris on anscontroll server with user ansadmin"
        print"====================================================================="
        return None
def get_ip_dns(ec2_conn):
    dict_of_ids={}
    try:
        fo=open("list_of_all_AnsController_and_AnsClient_ids.txt","r")
        for each_line in fo.readlines():
            key,value=each_line.strip('\n').split()
            dict_of_ids[key]=value
        fo.close()
    except Exception as e:
        print e
        sys.exit(2)
    ans_id=dict_of_ids['AnsControll_id']
    for each in ec2_conn.instances.filter(Filters=[{'Name':'instance-id',"Values":[ans_id]}]):
        ans_pri,ans_dns=each.private_ip_address,each.public_dns_name
        break
    return ans_id,ans_pri,ans_dns
def move_script(ans_pr_ip):
    cmd="scp -i DevOps.pem ssh_key_gen.sh ec2-user@"+ans_pr_ip+":/home/ec2-user"
    os.system(cmd)
    return None
def run_script(ans_dns):
        key = paramiko.RSAKey.from_private_key_file("DevOps.pem")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                client.connect(hostname=ans_dns, username="ec2-user", pkey=key)
                cmds=['chmod +x /home/ec2-user/ssh_key_gen.sh','/home/ec2-user/ssh_key_gen.sh']
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
        print "info",ans_id,ans_private_ip,ans_dns
        move_script(ans_private_ip)
        run_script(ans_dns)
if __name__ == '__main__':
        main()

