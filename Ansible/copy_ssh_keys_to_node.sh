#!/bin/bash
#mkdir .ssh
cd .ssh
pwd
for each in $(cat ${HOME}/nodes_ips.txt)
do

sudo echo "${each}" |  sudo tee -a /etc/ansible/hosts
  sshpass -p "ansible@123" ssh-copy-id -o StrictHostKeyChecking=No ${each}
done
