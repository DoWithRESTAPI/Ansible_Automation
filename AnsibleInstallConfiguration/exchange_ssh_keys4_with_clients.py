#!/bin/python
import boto3
import paramiko
from creation_of_required_AnsController_AnsClient_Servers_1 import *

def clear():
        os.system('clear')
        return None
def welcome():
        print"===================================================================="
        print"This will create a key exchange shell script on AnsController Server"
        print"===================================================================="
        return None
def get_all_prt_ips(ec2_conn):
        dict_of_ids={}
        fo=open("list_of_all_AnsController_and_AnsClient_ids.txt")
        for each in fo.readlines():
                key,value=each.strip('\n').split()
                dict_of_ids[key]=value
        fo.close()
        dict_of_ids_with_ansid=dict_of_ids
        del dict_of_ids['AnsControll_id']
        fo=open('exch_key.bh','w')
        fo.write("#!/bin/bash\n")
        fprivte_ids=open('client_private_ids','w')
        for key,ans_id in dict_of_ids.items():
                for each in ec2_conn.instances.filter(Filters=[{'Name':'instance-id',"Values":[ans_id]}]):
                        line="ssh-copy-id ansadmin@"+each.private_ip_address+'\n'
                        fo.write(line)
                        privateids=each.private_ip_address+'\n'
                        fprivte_ids.write(privateids)
        fprivte_ids.close()
        fo.close()

        return None

def main():
        clear()
        welcome()
        ec2_conn=get_connection()
        list_of_pr_ips=get_all_prt_ips(ec2_conn)

if __name__ == '__main__':
        main()


