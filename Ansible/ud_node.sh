#!/bin/bash
useradd ansadmin
echo -e "ansible@123\nansible@123"|passwd ansadmin
echo "ansadmin       ALL=(ALL)        NOPASSWD: ALL" >> /etc/sudoers
sed -i "s/PasswordAuthentication no/#PasswordAuthentication no/g" /etc/ssh/sshd_config
sed -i "s/#PasswordAuthentication yes/PasswordAuthentication yes/g" /etc/ssh/sshd_config
systemctl restart sshd
yum update -y
