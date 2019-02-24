function Checking_status_check
{
  Logs_Info=${PWD}/logs
  echo "Checking Master status check"
  Master_Id=`cat  ${Logs_Info}/Ansible_Master.txt |awk 'NR==2 {print $7}'`
  i=0
  while [ $i -le 5 ]
  do
    sleep 5
  #echo "aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate"
  echo "Checing status check for Master node"
  STATUS_CNT=`aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|wc -l`
  if [ ${STATUS_CNT} -ge  6 ]
  then
      STATUS=`aws ec2 describe-instance-status --instance-ids ${Master_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|awk 'NR==5 {print $2 }'`
      if [ "${STATUS}" == "ok" ]
      then
         echo "Master node is ready to accept requests"
          break

      fi
  fi
  done
  for each in `seq 1 $1`
  do
  Client_Id=`cat ${Logs_Info}/Ansible_Client${each}.txt |awk 'NR==2 {print $7}'`
  echo "aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate"
    i=0
    while [ $i -le 5 ]
    do
    echo "Checking Node$each status"
    STATUS_CNT=`aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|wc -l`
      if [ ${STATUS_CNT} -ge 6 ]
      then
      STATUS=`aws ec2 describe-instance-status --instance-ids ${Client_Id}  --filters 'Name=instance-status.status,Values=ok' --no-paginate|awk 'NR==5 {print $2 }'`
      if [ "${STATUS}" == "ok" ]
      then
         echo "Node$each is ready to accept requests"
          break

      fi
      fi
      echo "We will check again after 5 second"
      sleep 5
    done
  done
}


Checking_status_check
