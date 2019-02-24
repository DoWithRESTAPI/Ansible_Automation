#!/bin/bash
get_variables()
{
  clear
  source ./ec2_specifications.cfg
  D="\e[0m"
  R="\e[31m"
  G="\e[32m"
  Y="\e[33m"
  M="\e[35m"
  C="\e[36m"
}

_INFO()
{
 C_D=`date '+%Y-%b-%d %T'`
 echo -e "${G}INFO:${C_D}  $1$D"
}

_WARNING()
{
 C_D=`date '+%Y-%b-%d %T'`
 echo -e "${Y}WARNING:${C_D}  $1$D"
}
_ERROR()
{
 C_D=`date '+%Y-%b-%d %T'`
 echo -e "${R}WARNING:${C_D}  $1$D"
}
_CRITICAL()
{
 C_D=`date '+%Y-%b-%d %T'`
 echo -e "${C}WARNING:${C_D}  $1$D"
}

welcome()
{
  echo -e "\t    ${M}***********************************************************************************************${D}"
  echo -e "\t    ${G}|     Welcome to Automation of Ansible Installation and Configuration with Shell Scripting${D}    |"
  echo -e "\t    ${M}***********************************************************************************************${D}"
}
thankyou()
{
  echo -e "\t    ${M}***********************************************************************************************${D}"
  echo -e "\t    ${G}|     Successfully Installed and Configured Ansilbe. Thank you for using this Shell Script${D}    |"
  echo -e "\t    ${M}***********************************************************************************************${D}"

}

Checking_status_check()
{
  Logs_Info=${PWD}/logs
  _INFO "Checking status check for Master node"
  Master_Id=`cat  ${Logs_Info}/Ansible_Master.txt |awk 'NR==2 {print $7}'`
  i=0
  while [ $i -le 5 ]
  do
    sleep 5
  #echo "aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate"
  _INFO "Checking status check for Master node"
  STATUS_CNT=`aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|wc -l`
  if [ ${STATUS_CNT} -ge  6 ]
  then
      STATUS=`aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|awk 'NR==5 {print $2 }'`
      if [ "${STATUS}" == "ok" ]
      then
         _INFO "Master node is ready to accept requests"
          break

      fi
  fi
  done
  for each in `seq 1 $1`
  do
  Client_Id=`cat ${Logs_Info}/Ansible_Client${each}.txt |awk 'NR==2 {print $7}'`
  #echo "aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate"
    i=0
    while [ $i -le 5 ]
    do
    _INFO "Checking Node$each status"
    STATUS_CNT=`aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|wc -l`
      if [ ${STATUS_CNT} -ge 6 ]
      then
      STATUS=`aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|awk 'NR==5 {print $2 }'`
      if [ "${STATUS}" == "ok" ]
      then
         _INFO "Node$each is ready to accept requests"
          break

      fi
      fi
      #_INFO "We will check again after 5 second"
      sleep 5
    done
  done
}

create_ansible_controller()
{
  Logs_Info=${PWD}/logs
  rm -rf ${Logs_Info}/*
  #_INFO "Finding Private Address for Ansible Controller...."
  aws ec2 run-instances --image-id ${Img_Id}  --count 1 --instance-type ${Ec2_Type}  --key-name ansible_key --security-group-ids ${Security_Group} --user-data file://ud_controller.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Ansible_Controller},{Key=Ansible,Value=Controller}]' > ${Logs_Info}/Ansible_Master.txt
  cat ${Logs_Info}/Ansible_Master.txt | grep PRIVATEIPADDRESSES | awk '{print $NF}'> ${Logs_Info}/Ansible_Master_Private_IP.txt
  SEP=`cat ${Logs_Info}/Ansible_Master_Private_IP.txt`
  sleep 5
  aws ec2 describe-instances |grep $SEP | awk -F "$SEP" 'NR==1{ print $3 }'|awk '{ print $1 }' > ${Logs_Info}/Ansible_Master_Connection
  _INFO "Successfully created Ansible Controller"
}
create_ansible_nodes()
{
  #Logs_Info=${PWD}/logs
  #rm -rf ${Logs_Info}/*
 

  for each in `seq 1 $1`
 do
   _INFO "Creating Node: $each"
   aws ec2 run-instances --image-id ${Img_Id}  --count 1 --instance-type ${Ec2_Type}  --key-name ansible_key --security-group-ids ${Security_Group} --user-data file://ud_node.sh --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Ansible_Node},{Key=Ansible,Value=Node}]' > ${Logs_Info}/Ansible_Client${each}.txt
 sleep 5
 cat ${Logs_Info}/Ansible_Client${each}.txt | grep PRIVATEIPADDRESSES | awk '{print $NF}'> ${Logs_Info}/Ansible_Node${each}_Private_IP.txt
 SEP=`cat ${Logs_Info}/Ansible_Node${each}_Private_IP.txt`
 aws ec2 describe-instances |grep $SEP | awk -F "$SEP" 'NR==1{ print $3 }'|awk '{ print $1 }' > ${Logs_Info}/Ansible_Node${each}_Connection

 done
}

create_ec2_instances()
{
  no_nodes=$((No_of_Ec2s - 1))
 _INFO "Creating ${No_of_Ec2s} Instances, 1 Instance for Ansible Controller and ${no_nodes} Instance/s for Ansible Nodes."
 if [[ ${No_of_Ec2s} -eq 0 ]]
 then
   _WARNING "Sorry we cant create any instances"
 else
  if [[ ${No_of_Ec2s} -eq 1 ]]
  then
    _INFO "Creating only Ansible Controller server (Note: No Nodes)........"
    create_ansible_controller
  else
    _INFO "Creating Ansible Controller........."
    create_ansible_controller
    Nodes=$((No_of_Ec2s-1))
    _INFO "Creating ${Nodes} Node/s for Ansible "
    create_ansible_nodes ${Nodes}
  fi
 fi
 
}
get_nodes_ips()
{
 rm -rf servers_ips.txt
 if [[ $1 -eq 1 ]]
 then
   _INFO "Only Ansible Controller is created so need to work on nodes"
 else
   Master_Ip=$(cat logs/Ansible_Master_Private_IP.txt)
   _INFO "Finding IP address of Ansible Controller"
   sleep 1
   echo "Master_IP=${Master_Ip}" > servers_ips.txt
   cnt=$1
   nd_cnt=1
   nodes=$((cnt-1))
   for each_node in `seq 1 $nodes`
   do
     Node_ip=$(cat logs/Ansible_Node${nd_cnt}_Private_IP.txt)
     _INFO "Finding IP Address of Node${nd_cnt}"
     sleep 1
     echo "Node_${nd_cnt}_IP=${Node_ip}" >> servers_ips.txt
     nd_cnt=$((nd_cnt+1))
   done
 fi

}
getting_nodes_ips()
{
  rm -rf nodes_ips.txt
  cnt=1;
  for each in $(cat servers_ips.txt )
  do
     if [[ cnt -eq 1 ]]
     then
        cnt=$((cnt+1))
        continue
     fi
     echo $each | awk -F = '{print $2}' >>nodes_ips.txt
     cnt=$((cnt+1))
  done

}
generate_ssh_keys_on_Ansible_Controller()
{
 _INFO "Generating SSH KEYS on Ansible Controller "
 sleep 2
 sshpass -p "${Ansible_Admin_Passwd}" scp -q -o StrictHostKeyChecking=No ssh_key_ex.sh ${Ansible_Admin_User}@${Master_Ip}:ssh_key_ex.sh
 sshpass -p "${Ansible_Admin_Passwd}" scp -q -o StrictHostKeyChecking=No nodes_ips.txt ${Ansible_Admin_User}@${Master_Ip}:nodes_ips.txt
sshpass -p "${Ansible_Admin_Passwd}" ssh -t -o StrictHostKeyChecking=No ${Ansible_Admin_User}@${Master_Ip} "sh ssh_key_ex.sh" >/dev/null
 _INFO "Sucessfully generated SSH KEYS on Ansible Controller"
 
  _INFO "Copying SSH KEYS to Nodes"
  sshpass -p "${Ansible_Admin_Passwd}" scp -q -o StrictHostKeyChecking=No copy_ssh_keys_to_node.sh ${Ansible_Admin_User}@${Master_Ip}:copy_ssh_keys_to_node.sh
  sleep 5
  sshpass -p "${Ansible_Admin_Passwd}" ssh -t -o StrictHostKeyChecking=No ${Ansible_Admin_User}@${Master_Ip} "sh copy_ssh_keys_to_node.sh" >/dev/null
  _INFO "Successfully copied SSH Keys to all your servers"
  _INFO "Updating default invetroy file with Ansible Nodes IP's"
   echo -e "${Y}==================Just Connect with Ansible Controller using below link and run ansible all -m ping ==========${D}"
   echo -e "${C}$(cat logs/Ansible_Master_Connection)${D}"

}



main()
{
  get_variables
  welcome
  #create_ec2_instances
  Checking_status_check
  get_nodes_ips $No_of_Ec2s
  getting_nodes_ips
  generate_ssh_keys_on_Ansible_Controller
  thankyou
}



main
