/bin/bash exch_key.bh
/bin/python create_clients.py
/bin/bash update_inventory.sh

sleep 4
echo "Sucessfully verified all your configurations"
echo "Now you can test my the command as follows"
echo"==================================="
echo"    ansible myservers -m ping"
echo"==================================="
