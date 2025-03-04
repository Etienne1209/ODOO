import xmlrpc.client
#----------------------------------
#Etablir la connexion avec Odoo
#----------------------------------
erp_ipaddr = "172.31.10.137"
erp_port = "8026"
erp_url = f'http://{erp_ipaddr}:{erp_port}'

print ("Connexion ODOO")
print(f"@URL={erp_url}")

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    version = common.version()
    print(f"Odoo version={version['server_serie']}")
except ConnectionRefusedError:
    print("Odoo Server not found or connection rejected")
#---------------------------------
#Athentification avec Odoo
#---------------------------------
erp_db = "YOURT"
erp_user = "etienne.jugeur1209@gmail.com"
erp_pwd = "mauvais"
user_id = common.authenticate(erp_db,erp_user,erp_pwd,{})

print(f"Odoo authentification:{user_id}")
if(user_id!=False):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
    access = models.execute_kw(erp_db,user_id, erp_pwd,
     'mrp.production','check_access_rights',
     ['write'],{'raise_exception': False})
else:
    print(f'Odoo Server authentification rejected : DB={erp_db} User={erp_user}')
print(f"Manufactoring Order write access rights : {access}")



import xmlrpc.client
#----------------------------------
#Etablir la connexion avec Odoo
#----------------------------------
erp_ipaddr = "172.31.10.137"
erp_port = "8026"
erp_url = f'http://{erp_ipaddr}:{erp_port}'

print ("Connexion ODOO")
print(f"@URL={erp_url}")

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    version = common.version()
    print(f"Odoo version={version['server_serie']}")
except ConnectionRefusedError:
    print("Odoo Server not found or connection rejected")
#---------------------------------
#Athentification avec Odoo
#---------------------------------
erp_db = "YOURT"
erp_user = "etienne.jugeur1209@gmail.com"
erp_pwd = "vxrq-rwjs-ejpz"
user_id = common.authenticate(erp_db,erp_user,erp_pwd,{})
gModels=None

print(f"Odoo authentification:{user_id}")
if(user_id!=False):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
    access = models.execute_kw(erp_db,user_id, erp_pwd,
     'mrp.production','check_access_rights',
     ['write'],{'raise_exception': False})
else:
    print(f'Odoo Server authentification rejected : DB={erp_db} User={erp_user}')
print(f"Manufactoring Order write access rights : {access}")
#---------------------------------
#Exploitation de la base de donées
#---------------------------------
def getManufOrderToDo():
    fields =['name','date_planned_start','product_id','product_dty','qty_producing','state']
    limit=10
    mo_list = gModels.execute_kw(erp_db,user_id,erp_user,
        'mrp.production','search_read',
        [[('state','=','confirmed'),('qty_produced','!=','product_qty')]],
        {'fields':fields,'limit':limit})
    for mo_dico in mo_list:
        print(f'-------------------')
        for k in mo_dico.keys():
            print(f'-{k}:{mo_dico[k]}')
