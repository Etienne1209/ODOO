import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import os

def ouvrir_fenetre_principale():
    login = entry_login.get()
    password = entry_password.get()

# Paramètrage de la page de connexion avec le login et mot de passe
    if login == "PROD" and password == "1234":
        fenetre_connexion.withdraw()
        fenetre_principale = tk.Toplevel(fenetre_connexion)
        fenetre_principale.title("ERP Connexion")
        fenetre_principale.geometry("500x500")

# Ouverture et affichage de la 2ème fenêtre si le login et mot de passe est correct
        img_path = Path("yaourt.png")
        img = tk.PhotoImage(file=img_path)
        label_image = tk.Label(fenetre_principale, image=img)
        label_image.image = img
        label_image.pack(pady=20)

# Le logo de l'entreprise s'affiche
        logo_path = Path("/home/leclerc/Downloads/LOGO.ico")
        if logo_path.exists():
            fenetre_principale.iconphoto(True, tk.PhotoImage(file=logo_path))
        fenetre_principale.mainloop()
        
# Affichage du message d'erreur car le login et le mot de passe n'est pas correct        
    else:
        messagebox.showerror("Erreur", "L'identifiant ou le mot de passe n'est pas correct.")

fenetre_connexion = tk.Tk()
fenetre_connexion.title("Fenêtre de Connexion")

fenetre_connexion.geometry("500x500")
fenetre_connexion.config(bg="white")

logo_path = Path("/home/leclerc/Downloads/LOGO.ico")
if logo_path.exists():
    fenetre_connexion.iconphoto(True, tk.PhotoImage(file=logo_path))

frame_connexion = tk.Frame(fenetre_connexion, bg="white", bd=5, relief="solid")
frame_connexion.place(relx=0.5, rely=0.5, anchor="center")

label_login = tk.Label(frame_connexion, text="Login:", bg="white", font=("Arial", 15))
label_login.pack(pady=5)
entry_login = tk.Entry(frame_connexion, font=("Arial", 15))
entry_login.pack(pady=5)

label_password = tk.Label(frame_connexion, text="Mot de passe:", bg="white", font=("Arial", 15))
label_password.pack(pady=5)
entry_password = tk.Entry(frame_connexion, show="*", font=("Arial", 15))
entry_password.pack(pady=5)

button_connexion = tk.Button(frame_connexion, text="Connexion", command=ouvrir_fenetre_principale, font=("Arial", 15))
button_connexion.pack(pady=20)

fenetre_connexion.mainloop()
