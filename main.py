import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import requests  # Pour télécharger l'image
from PIL import Image, ImageTk  # Pour afficher l'image téléchargée dans Tkinter
import xmlrpc.client  # Pour la connexion à Odoo via XML-RPC
import io  # Pour traiter les données d'image en mémoire
import sys
import datetime as dt

#=============================================================================================================================================================================
#=============================================================================================================================================================================

#---------------------------
# Intégration interface Odoo |
# ---------------------------

# Ajout du chemin si nécessaire pour inclure votre module 'IF_Odoo'
sys.path.append("/home/Documents/Informatique_industrielle/PYTHON/07_ProjetPython_Odoo/odoo.py")

class App(tk.Tk):
    """Application GUI en Tkinter"""
    def __init__(self):
        """Constructeur de l'application (héritage de l'objet Tk)"""
        super().__init__()
        try:
            # Initialiser la connexion à Odoo via l'objet IF_Odoo
            self.ifOdoo = IF_Odoo("172.31.10.137", "8026", "etienne.jugeur1209@gmail.com", "vxrq-rwjs-ejpz")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de IF_Odoo : {e}")
            messagebox.showerror("Erreur", f"Impossible d'initialiser la connexion à Odoo. {e}")
            self.quit()
        
        self.initWidgetOdoo()

    def initWidgetOdoo(self):
        """Initialisation du widget Odoo"""
        self.frmOdoo = ttk.Frame(self)
        self.frmOdoo.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.btnConnect = ttk.Button(self.frmOdoo, text="Connect", command=self.onBtnConnect)
        self.btnConnect.pack()

        # Label pour afficher le statut
        self.lblStatusbar = tk.Label(self, text="Status : Disconnected", relief="sunken", anchor="w")
        self.lblStatusbar.pack(side="bottom", fill="x")

    def onBtnConnect(self):
        """Callback pour le bouton de connexion"""
        try:
            self.lblStatusbar.config(text=f'Status : Connexion en cours...')
            self.btnConnect.config(cursor='watch')
            self.update()
            
            self.ifOdoo.connect()  # Connexion à Odoo

            self.btnConnect.config(cursor='arrow')
            self.lblStatusbar.config(text=f'Status : Odoo Version = {self.ifOdoo.mOdooVersion}')
        except Exception as e:
            self.btnConnect.config(cursor='arrow')
            messagebox.showerror("Erreur", f"Échec de la connexion à Odoo : {e}")
            self.lblStatusbar.config(text="Status : Erreur de connexion")

    def update(self):
        """Mettre à jour l'interface utilisateur"""
        try:
            date = dt.datetime.now()
            date_str = f'[{date:%d-%m-%Y :: %H hrs %M min %S sec}]'
            self.lblStatusbar.config(text=f'{date_str} Status : Odoo Version = {self.ifOdoo.mOdooVersion}')
            self.after(5000, self.update)  # Rafraîchit toutes les 5000 ms (5 secondes)
        except Exception as e:
            print(f"Erreur de mise à jour de l'interface : {e}")

#==========================================================================================================================================================================
#==========================================================================================================================================================================

#---------------------------------------------
# Fonction de gestion de la fenêtre principale |
#---------------------------------------------

def ouvrir_fenetre_principale():
    global entry_login, entry_password, fenetre_connexion  # Déclaration des variables globales nécessaires

    login = entry_login.get()  # Récupérer le texte entré dans le champ login
    password = entry_password.get()  # Récupérer le texte entré dans le champ mot de passe

    # Vérification des informations de connexion
    if login == "PROD" and password == "1234":
        # Si les identifiants sont corrects, ouvrir la fenêtre principale
        fenetre_connexion.withdraw()  # Masquer la fenêtre de connexion
        fenetre_principale = tk.Toplevel(fenetre_connexion)  # Créer une nouvelle fenêtre secondaire
        fenetre_principale.title("ERP de Yourt")  # Titre de la fenêtre
        fenetre_principale.geometry("800x600")  # Dimension de la fenêtre
        fenetre_principale.config(bg="white")  # Fond d'écran blanc

        # Affichage du titre
        label_erp = tk.Label(fenetre_principale, text="ERP de Yourt", font=("Arial", 40), fg="black", bg="white")
        label_erp.pack(pady=20)

        # ---------------------------------------------------------------
        # Frame contenant les menus déroulants et le bouton de validation |
        #----------------------------------------------------------------

        frame_gauche = tk.Frame(fenetre_principale, bg="white")
        frame_gauche.pack(side="left", padx=20, pady=20, anchor="n")  # Frame à gauche et centrée verticalement

        # Menu déroulant pour sélectionner le produit
        variable = tk.StringVar(fenetre_principale)
        variable.set("Banane")  # Définir la valeur par défaut à "Banane"
        menu_deroulant = tk.OptionMenu(frame_gauche, variable, "Banane", "Fraise", "Kiwi", command=afficher_image)
        menu_deroulant.config(font=("Arial", 15), width=15)  # Police de taille 15
        menu_deroulant.pack(pady=30)  # Augmenter le padding vertical (espacement plus bas)

        # Menu déroulant pour le conditionnement
        variable_conditionnement = tk.StringVar(fenetre_principale)
        variable_conditionnement.set("4x1")
        menu_conditionnement = tk.OptionMenu(frame_gauche, variable_conditionnement,"4x1", "2x1")
        menu_conditionnement.config(font=("Arial", 15), width=10)  # Police de taille 15
        menu_conditionnement.pack(pady=30)  # Augmenter le padding vertical ici aussi

        # Bouton de validation
        bouton_validation = tk.Button(frame_gauche, text="Validation", command=envoyer_commande, font=("Arial", 18))
        bouton_validation.pack(pady=20)

        # ---------------------------------------
        # Frame pour afficher l'image du produit |
        # ---------------------------------------

        frame_image = tk.Frame(fenetre_principale, bg="white")
        frame_image.pack(side="right", expand=True, padx=10, pady=10)
        global label_image  # Déclaration globale pour accéder à la variable label_image
        label_image = tk.Label(frame_image)
        label_image.pack(pady=20)  # L'image sera affichée ici

        # Tentative de connexion à Odoo
        if se_connecter_a_odoo():  # Si la connexion à Odoo réussit
            print("Connexion à Odoo réussie.")
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à Odoo.")

        # Démarrer la boucle principale de la fenêtre secondaire
        fenetre_principale.mainloop()

    else:
        # Si les identifiants sont incorrects, afficher un message d'erreur
        messagebox.showerror("Erreur", "L'identifiant ou le mot de passe n'est pas correct.")

#===============================================================================================================================================================================
#===============================================================================================================================================================================

#------------------------------------------------------------------
# Fonction pour afficher l'image en fonction du produit sélectionné |
#------------------------------------------------------------------

def afficher_image(selection):
    """Cette fonction affiche une image en fonction du produit sélectionné."""
    try:
        if selection == "Banane":
            image_path = "/chemin/vers/banane.png"  # Mettez ici le chemin de l'image
        elif selection == "Fraise":
            image_path = "/chemin/vers/fraise.png"  # Mettez ici le chemin de l'image
        elif selection == "Kiwi":
            image_path = "/chemin/vers/kiwi.png"  # Mettez ici le chemin de l'image
        else:
            image_path = ""

        # Charger l'image
        image = Image.open(image_path)
        image = image.resize((200, 200))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)

        # Afficher l'image
        label_image.config(image=photo)
        label_image.image = photo  # Garder une référence de l'image
    except Exception as e:
        print(f"Erreur lors de l'affichage de l'image : {e}")
        messagebox.showerror("Erreur", f"Erreur lors de l'affichage de l'image : {e}")

#===============================================================================================================================================================================
#===============================================================================================================================================================================

# -------------------------------
# Fonction d'envoi de la commande |
#--------------------------------

def envoyer_commande():
    # Cette fonction peut être étendue pour envoyer les commandes à Odoo ou faire d'autres actions
    print("Commande envoyée !")
    
#===============================================================================================================================================================================
#===============================================================================================================================================================================

#------------------------------------
# Création de la fenêtre de connexion |
#------------------------------------

fenetre_connexion = tk.Tk()
fenetre_connexion.title("Fenêtre de Connexion")

# Récupérer la taille de l'écran pour ajuster la fenêtre de connexion
screen_width = fenetre_connexion.winfo_screenwidth()
screen_height = fenetre_connexion.winfo_screenheight()

# Ajuster la taille de la fenêtre pour qu'elle occupe tout l'écran
fenetre_connexion.geometry(f"{screen_width}x{screen_height}")
fenetre_connexion.config(bg="white")

# Affichage du titre de l'application
label_erp = tk.Label(fenetre_connexion, text="ERP de Yourt", font=("Arial", 35), fg="black", bg="white")
label_erp.pack(pady=20)

# Création d'un frame pour centrer les éléments de connexion
frame_connexion = tk.Frame(fenetre_connexion, bg="white", bd=5, relief="solid", width=600, height=300)
frame_connexion.place(relx=0.5, rely=0.5, anchor="center")

# Champs de saisie pour le login et le mot de passe
label_login = tk.Label(frame_connexion, text="Login:", bg="white", font=("Arial", 30))
label_login.pack(pady=5)
entry_login = tk.Entry(frame_connexion, font=("Arial", 30))
entry_login.pack(pady=5)

label_password = tk.Label(frame_connexion, text="Mot de passe:", bg="white", font=("Arial", 30))
label_password.pack(pady=5)
entry_password = tk.Entry(frame_connexion, show="*", font=("Arial", 30))
entry_password.pack(pady=5)

# Bouton pour se connecter et ouvrir la fenêtre principale
button_connexion = tk.Button(frame_connexion, text="Connexion", command=ouvrir_fenetre_principale, font=("Arial", 30))
button_connexion.pack(pady=20)

# Démarrer la boucle principale pour afficher la fenêtre de connexion
fenetre_connexion.mainloop()
