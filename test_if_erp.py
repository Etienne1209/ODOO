erp_ipaddr = "172.31.10.137"
erp_port = "8026"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()

print ("Connexion ODOO")
print(f"@URL={erp_url}")
print(f"Odoo version={version}")