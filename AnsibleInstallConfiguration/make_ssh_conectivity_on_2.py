#!/bin/python
import os
import sys
import platform
import time
from creation_of_required_AnsController_AnsClient_Servers_1 import *
try:
  import boto3
  import paramiko
  import botocore
except Exception as e:
  print e
  sys.exit(1)


def clear():
   if platform.system()=="Windows":
        os.system('cls')
   else:
        os.system('clear')
   return None

def welcome():
   print"===================================================================================================="
   print"This scrit will enable SSH Connection between ur AnsibleController servers and AnsibleClient servers"
   print"===================================================================================================="
   print"\n\n"
   return None
def get_list_of_all_ids_of_Ansible_Servers():
   print"Getting all ids of Ansible Servers from a file:  list_of_all_AnsController_and_AnsClient_ids.txt"
   time.sleep(2)
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
   return dict_of_ids

def get_public_dns_names(ec2_conn,dict_of_ans_ec2):
    in_ids=dict_of_ans_ec2.values()
    list_of_public_dns=[]
    for each in ec2_conn.instances.filter(Filters=[{'Name':'instance-id',"Values":in_ids}]):
        list_of_public_dns.append(each.public_dns_name)
    print "The all availabe public dns names are: ",list_of_public_dns
    print"\n\n"
    return list_of_public_dns
def wait_upto_all_running(ec2_conn,ids_dict):
    list_of_ids=ids_dict.values()
    for each_id in list_of_ids:
        while True:
            state=False
            for each in ec2_conn.instances.filter(Filters=[{'Name':'instance-id',"Values":[each_id]}]):
                print each.state
                if each.state['Name']=="running":
                    state=True
            if state==True:
                break
    print "all are running"
    return None
def create_ansadmin_user_on_all_ec2(list_of_public_dns):
    key = paramiko.RSAKey.from_private_key_file("DevOps.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for instance_ip in list_of_public_dns:
        print "Creating ansadmin user on ",instance_ip
        try:
            client.connect(hostname=instance_ip, username="ec2-user", pkey=key)
            cmds=['sudo useradd ansadmin', 'echo "ansadmin:Ans#123"|sudo chpasswd', 'echo "ansadmin        ALL=(ALL)       NOPASSWD: ALL" | sudo tee -a /etc/sudoers', "sudo sed -i -e 's/PasswordAuthentication no/#PasswordAuthentication no/g' /etc/ssh/sshd_config", "sudo sed -i -e 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config", 'sudo systemctl restart sshd']
            for cmd in cmds:
                print "command is: ",cmd
                stdin, stdout, stderr = client.exec_command(cmd)
                print cmd," out is: ",stdout.read()
            client.close()
        except Exception as e:
            print e
            sys.exit(2)
    print "Successfully created users on all hosts"
    return None
def thank_you():
   time.sleep(2)
   print"\n"
   print"====================================================================="
   print"Success fully enabled SSH connection between all your Ansbile Servers"
   print"Thank you\nBye!!"
   print"====================================================================="
   return None
def main():
   clear()
   welcome()
   ec2_conn=get_connection()
   dict_of_ids=get_list_of_all_ids_of_Ansible_Servers()
   #print "all ids are: ",dict_of_ids
   wait_upto_all_running(ec2_conn,dict_of_ids)
   public_dns=get_public_dns_names(ec2_conn,dict_of_ids)
   create_ansadmin_user_on_all_ec2(public_dns)
   thank_you()

if __name__=="__main__":
   main()
