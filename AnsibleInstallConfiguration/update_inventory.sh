#!/bin/bash
echo "[myservers]" | sudo tee -a /etc/ansible/hosts  >> /dev/null
for line in `cat clients_pv.txt`
do
echo "${line}"
echo "${line}" | sudo tee -a /etc/ansible/hosts >> /dev/null

done
