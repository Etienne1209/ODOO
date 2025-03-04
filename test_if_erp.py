import xmlrpc.client

#----------------------------------
# Etablir la connexion avec Odoo
#----------------------------------
erp_ipaddr = "172.31.10.137"
erp_port = "8026"
erp_url = f'http://{erp_ipaddr}:{erp_port}'

print("Connexion ODOO")
print(f"@URL={erp_url}")

try:
    common = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/common')
    version = common.version()
    print(f"Odoo version={version['server_serie']}")
except ConnectionRefusedError:
    print("Odoo Server not found or connection rejected")

#---------------------------------
# Authentification avec Odoo
#---------------------------------
erp_db = "YOURT"
erp_user = "etienne.jugeur1209@gmail.com"
erp_pwd = "vxrq-rwjs-ejpz"
user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})

print(f"Odoo authentification: {user_id}")
if user_id != False:
    models = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/object')
    access = models.execute_kw(erp_db, user_id, erp_pwd,
                               'mrp.production', 'check_access_rights',
                               ['write'], {'raise_exception': False})
else:
    print(f'Odoo Server authentification rejected: DB={erp_db} User={erp_user}')
    
print(f"Manufacturing Order write access rights: {access}")

#---------------------------------
# Exploitation de la base de données
#---------------------------------
def getManufOrderToDo():
    fields = ['name', 'date_planned_start', 'product_id', 'product_qty', 'qty_producing', 'state']
    limit = 10
    mo_list = models.execute_kw(erp_db, user_id, erp_pwd,
                                'mrp.production', 'search_read',
                                [[('state', '=', 'confirmed'), ('qty_produced', '!=', 'product_qty')]],
                                {'fields': fields, 'limit': limit})
    for mo_dico in mo_list:
        print(f'-------------------')
        for k, v in mo_dico.items():
            print(f'- {k}: {v}')
            
            # Accéder aux informations du produit
            if k == 'product_id':
                product_id = v[0]  # Extraire l'ID du produit de la liste [ID, Name]
                product_info = models.execute_kw(erp_db, user_id, erp_pwd,
                                                 'product.product', 'read',
                                                 [product_id], {'fields': ['name', 'list_price', 'default_code']})
                if product_info:
                    print(f"Produit: {product_info[0]['name']}")
                    print(f"Prix: {product_info[0]['list_price']}")
                    print(f"Code produit: {product_info[0]['default_code']}")

# Appeler la fonction pour récupérer les ordres de fabrication
getManufOrderToDo()
