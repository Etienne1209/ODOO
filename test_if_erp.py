erp_ipaddr = "192.168.0.17"
erp_port = "8069"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
import xmlrpc.client

print ("Connexion ODOO")
print(f"@URL={erp_url}")

