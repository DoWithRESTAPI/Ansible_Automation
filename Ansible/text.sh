cnt=1;
for each in $(cat servers_ips.txt )
do
   if [[ cnt -eq 1 ]]
   then
      cnt=$((cnt+1))
      continue
   fi
   echo $each | awk -F = '{print $2}'
   cnt=$((cnt+1))
done
