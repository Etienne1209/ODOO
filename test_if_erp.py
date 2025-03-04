erp_ipaddr = "172.31.10.137"
erp_port = "8026"
erp_url = f'http://{erp_ipaddr}:{erp_port}'
erp_db = "YOURT"
erp_user = "etienne.jugeur1209@gmail.com"
erp_pwd = "vxrq-rwjs-ejpz"
import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
version = common.version()
user_id = common.authenticate(erp_db,erp_user,erp_pwd,{})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
access = models.execute_kw(erp_db,user_id, erp_pwd,
    'mrp.production','check_access_rights',
    ['write'],{'raise_exception': False})

print ("Connexion ODOO")
print(f"@URL={erp_url}")
print(f"Odoo version={version['server_serie']}")
print(f"Odoo authentification:{user_id}")
print(f"Manufactoring Order write access rights : {access}")