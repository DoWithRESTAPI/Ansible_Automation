#!/bin/python
import sys
import os
import time
import platform
try:
    import boto3
    import botocore
    import paramiko
    #print"imported boto3 module successfully"
    time.sleep(2)

except Exception as e:
    print e
    print "terminating the script"
    sys.exit(1)
def is_windows():
    if platform.system()=='Windows':
        return True
    else:
        return False
def clear():
    if is_windows():
        os.system('cls')
    else:
        os.system('clear')
def welcome():
    print"======================================================================"
    print"      Welcome to creations of required servers for Ansible Setup      "
    print"======================================================================"
def get_connection():
    try:
        time.sleep(2)
        print"Getting connection with your AWS Account...."
        ec2_conn=boto3.resource('ec2')
        time.sleep(2)
        print"Successfully Connected with your AWS Account\n\n"
    except Exception as e:
        print e
        print "\\nSo terminating the program. Verify it and re-execute this"
        sys.exit(2)
    return ec2_conn
def get_no_AnsClients():
    count=input('Enter number of AnsClients servers required: ')
    print"We are going to Create 1-AnsController Server and {}-AnsClient Servers".format(count)
    return count
def create_AnsAdmin(ec2_conn):
    time.sleep(1)
    image_id='ami-6871a115'
    ec2_type='t2.micro'
    key_pair_name='DevOps'
    dict_of_ans_ec2={}
    print"Creating  Anscontoller ........"
    response=ec2_conn.create_instances(ImageId=image_id,
                              MinCount=1,MaxCount=1,KeyName=key_pair_name,InstanceType=ec2_type,
                              SecurityGroupIds=['sg-daecc0af'],
                              TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'AnsController'
                },
            ]
        },
    ])
    time.sleep(2)
    print "Sucessfuly Created AnsController Server\n\n"
    ans_contr_id=response[0].id
    dict_of_ans_ec2['AnsControll_id']=ans_contr_id
    return dict_of_ans_ec2
def create_AnsClients(ec2_conn,no_of_clients,dict_of_ans_ec2):
    image_id='ami-6871a115'
    ec2_type='t2.micro'
    key_pair_name='DevOps'
    for each in range(no_of_clients):
        time.sleep(2)
        tag_value="AnsClient"+str(each+1)
        print"Creating AnsClient-{}......".format(each+1)
        response=ec2_conn.create_instances(ImageId=image_id,
                              MinCount=1,MaxCount=1,KeyName=key_pair_name,InstanceType=ec2_type,
                              SecurityGroupIds=['sg-daecc0af'],
                              TagSpecifications=[
                                     {
                                        'ResourceType': 'instance',
                                        'Tags': [
                                                    {
                                                        'Key': 'Name',
                                                        'Value': tag_value
                                                    },
                                                 ]
                                        },
                                                ])
        print"Sucessfully Created AnsClient-{}\n\n".format(each+1)
        tag_value=tag_value+'_id'
        client_id=response[0].id
        dict_of_ans_ec2[tag_value]=client_id
    time.sleep(2)
    return dict_of_ans_ec2
def write_to_file(dict_of_ids):
    fo=open("list_of_all_AnsController_and_AnsClient_ids.txt","w")
    for key,value in dict_of_ids.items():
        fo.write("{} {}\n".format(key,value))
    fo.close()
    print"Sucessfully created a file for ids"
    return None
def thank_you():
    print"\n\n"
    print"==========================================================================================="
    print"Sucessfully created AnsController and AnsClients  Servers     "
    #print"\n\nSaved all info of all server in a file called AnsController_AnsClients_ids_dns_details.txt"
    print"\n\nThank you for using this script   "
    print"*****************************************"
    print"* Now run:   2_make_ssh_connectivity.py *"
    print"*****************************************"
    print"==========================================================================================="
def main():
    clear()
    welcome()
    no_of_Ansclients=get_no_AnsClients()
    ec2_conn=get_connection()
    dict_of_id=create_AnsAdmin(ec2_conn)
    dict_of_ids=create_AnsClients(ec2_conn,no_of_Ansclients,dict_of_id)
    print"The ids are: ",dict_of_ids
    write_to_file(dict_of_ids)
    #wiat_till_running()
    thank_you()

if __name__=="__main__":
    main()

