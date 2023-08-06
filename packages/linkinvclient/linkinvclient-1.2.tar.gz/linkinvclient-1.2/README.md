# linkinvclient
python and CLI client for linkinventory micoservie 




Installation
================================

    git clone https://github.com/microservice-tsp-billing/linkinvclient.git
    cd linkinvclient
    virtualenv -p python3 venv
	source venv/bin/activate
	pip install -r requirement.txt


pip install 
----------------------------

	mkdir linkinvclient
	cd linkinvclient
	virtualenv -p python3 venv
	source venv/bin/activate
	pip install linkinvclient

config
===============================================================
Follow readme for configuring the tokenleaderclient first - https://github.com/microservice-tsp-billing/linkinvclient
apart from the tokenleaderclient configuration  the following sections should be present in the /etc/tokenleader/client_configs.yml


	llinkInventory:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
  
  
hence the complete configuraion will look as:  


    user_auth_info_from: file # OSENV or file
	user_auth_info_file_location: /home/bhujay/tlclient/user_settings.ini
	fernet_key_file: /home/bhujay/tlclient/prod_farnetkeys	
	tl_public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYV9y94je6Z9N0iarh0xNrE3IFGrdktV2TLfI5h60hfd9yO7L9BZtd94/r2L6VGFSwT/dhBR//CwkIuue3RW23nbm2OIYsmsijBSHtm1/2tw/0g0UbbneM9vFt9ciCjdq3W4VY8I6iQ7s7v98qrtRxhqLc/rH2MmfERhQaMQPaSnMaB59R46xCtCnsJ+OoZs5XhGOJXJz8YKuCw4gUs4soRMb7+k7F4wADseoYuwtVLoEmSC+ikbmPZNWOY18HxNrSVJOvMH2sCoewY6/GgS/5s1zlWBwV/F0UvmKoCTf0KcNHcdzXbeDU9/PkGU/uItRYVfXIWYJVQZBveu7BYJDR bhujay@DESKTOP-DTA1VEB
	tl_user: user1
	tl_url: http://localhost:5001
	ssl_verify: False	
	llinkInventory:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
 


PYTHON client
===================================

	from tokenleaderclient.configs.config_handler import Configs
	from  tokenleaderclient.client.client import Client
	from linkinvclient.client import LIClient
	auth_config = Configs()
	tlclient = Client(auth_config)
	c = LIClient(tlclient)
	c.list_links()


from tokenleaderclient.configs.config_handler import Configs
from  tokenleaderclient.client.client import Client
from linkinvclient.client import LIClient
auth_config = Configs()
tlclient = Client(auth_config)
c = LIClient(tlclient)
c.list_links()
c.list_link_by_slno(1)

rate_dict = {'tsp': 'TATA', 
                 'linktype': 'MPLS',
                 'activity_type': 'Install',
                 'otc': 5000, 
                 'rate_per_year': 100000 }
              
                 
c.add_rate(rate_dict)
c.list_obj('Rate', 'all', 'all')
c.delete_obj('Rate', '16')

all_ad =  d = {"prem_name": "prem ABCD", 
             "prem_no": 420, 
             "state": "Lost state",  "city": "Newfoundland",
             "pin": 4200,
             "gstn": "GSTN420", 
             "sgst_rate": 9, "cgst_rate": 9}

c.add_altaddress(all_ad)


lnet_d = {"infoopsid": "info XXXX", 
             "altaddress_id": 4, 
             "rate_id": 17,             
             }
c.add_lnetlink(lnet_d)

lnet_d = {"infoopsid": "info ABCD", 
             "altaddress_id": 4, 
             "rate_id": 17, 
             "last_payment_date": "01-04-2019"           
             }
c.add_lnetlink(lnet_d)



payment_dict = {"invoice_id": "invoice1234", 
             	"billing_from": "01-01-2019", 
             	"billing_to": "31-03-2019",
             	"billing_type": "Installation",  
             	"amount": "5000",
             	"payment_date": "27-04-2019", 
             	"mode": "NEFT",
             	"ref_no": "NEFT-hhhh-99989-NS", 
             	"status": "Paid",
             	"netlink_id": 7}
    
c.add_payment(payment_dict)
    

CLI coming soon
=====================
     
     linkinv.sh  list -n all
     linkinv.sh  list -n 1
     
 or when  pip installation from package is not done and you are running from the source 
     
    ./linkinv.sh  list -n all
    ./linkinv.sh  list -n 1
    

- name: role1
  allow:
  - tokenleader.adminops.adminops_restapi.list_users
  - micros1.ms2app.restapi.firstapi.ep3
  - linkInventory.restapi.routes.get_links_rest
  - linkInventory.restapi.routes.get_link_by_slno
  - linkInventory.list_obj
  - linkInventory.add_rate
  - linkInventory.delete_obj
  - linkInventory.add_payment
  - linkInventory.add_altaddress
  - linkInventory.add_lnetlink
  - micros1.create_invoice
  - micros1.upload_excel
  - micros1.list_all
  - micros1.delete_all
  - micros1.update_invoice
  - micros1.recommend_change
  - micros1.accept_recom
  - micros1.approve_invoice
  - micros1.reject_invoice
  - micros2.save_tesprec
  - micros2.list_all
  - micros2.delete_all    
 
 
#duration from current time and a last_date
import datetime
fmt = '%d-%m-%Y'
cdt = datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)
cdt = datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)
ldt = datetime.datetime.strptime('12-12-2018', fmt)
dur = cdt - ldt
dur
#datetime.timedelta(136, 70458, 943446)
dur.days 
  
 >>> c.list_obj("Lnetlink", "id", "7")
/mnt/c/mydev/microservice-tsp-billing/linkinvclient/venv/lib/python3.5/site-packages/urllib3/connectionpool.py:847: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
[{'altaddress': {'prem_no': 420, 'sgst_rate': 9, 'cgst_rate': 9, 'pin': 4200, 'state': 'Lost state', 'id': 4, 'city': 'Newfoundland', 'prem_name': 'prem ABCD', 'gstn': 'GSTN420'}, 'payments': [{'date': '27-04-2019', 'id': 12, 'billing_to': '31-03-2019', 'mode': 'NEFT', 'amount': 5000, 'billing_from': '01-01-2019', 'invoice_id': 'invoice1234', 'netlink_id': 7, 'ref_no': 'NEFT-hhhh-99989-NS', 'billing_type': 'Installation', 'status': 'Paid'}], 'last_payment_date': '27-04-2019', 'id': 7, 'infoopsid': 'info XXXX', 'rate': {'rate_per_month': None, 'rate_per_day': None, 'activity_type': 'Install', 'id': 17, 'linktype': 'MPLS', 'otc': 5000, 'rate_per_year': 100000, 'tsp': 'TATA'}}]

istoffset = datetime.timedelta(hours=5, minutes=30)
if lifecycle_phase is not == surrender:
	invoice bill_to  <= datetime.datetime.utcnow() + istoffset
else:
    invoice bill_to <= infoops_link.surrender_date + 30days
    
if lnet last_payment_date:
    invoice bill_from >= lnet last_payment_date
else:
    invoice bill_from >= infoops life_cycle_start-date
    

duration = (bill_to - bill_from).days

link_charge_rate = lnet[0].get('rate').get('rate_per_year')/365

charge_amount = duration * link_charge_rate

link_location = lnet[0].get('altaddress')

gstn_percent = link_location.get('sgst_rate') + link_location.get('cgst_rate')

tax = charge_amount * (gstn_percent/100)

charge_amount_with_tax  = charge_amount + tax





