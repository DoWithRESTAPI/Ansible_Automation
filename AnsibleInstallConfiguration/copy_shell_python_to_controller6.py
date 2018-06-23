from creation_of_required_AnsController_AnsClient_Servers_1 import *
from exchange_ssh_keys4_with_clients import *

from generate_ssh_key_on_ans_controller_3 import *
def clear():
        os.system('clear')
        return None
def move_files(ans_dns):
    for each in ['exch_key.bh','create_clients.py','update_inventory.sh','final_script.sh']:
        cmd='scp -i DevOps.pem   '+each + '    ansadmin@'+ans_dns+":/home/ansadmin/"
        print "cmd is: ",cmd
        os.system(cmd)
    return None
def thank_you(ans_dns):
    print"========================================================="
    print"\t\tAlmost your work is done"
    print"Goto AnsController Server with the following url"
    print"ssh -i DevOps.pem ansadmin@{}".format(ans_dns)
    print"\nNow run the scripts verification script"
    print"/bin/bash final_script.sh"
    print"\n\nBye............"
    print"=========================================================="
def main():
   clear()
   welcome()
   ec2_conn=get_connection()
   ans_id,ans_private_ip,ans_dns=get_ip_dns(ec2_conn)
   move_files(ans_dns)
   thank_you(ans_dns)
if __name__ == '__main__':
        main()

