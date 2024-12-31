import platform
import subprocess
import sys
import distro
import tkinter as tk
import requests

def check_python():
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], universal_newlines=True).strip()
        return python_version
    except FileNotFoundError:
        return "Python n'est pas installé sur ce système."

def install_tkinter():
    system_name = platform.system()

    if system_name == "Windows":
        print("Tkinter est normalement inclus avec Python sur Windows.")

    elif system_name == "Darwin":
        print("Tkinter est inclus avec Python sur macOS.")

    elif system_name == "Linux":
        distro_name = distro.id().lower()
        if distro_name in ["debian", "ubuntu"]:
            print("Installation de Tkinter pour Debian/Ubuntu.")
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "-y", "python3-tk"])
        elif distro_name == "fedora":
            print("Installation de Tkinter pour Fedora.")
            subprocess.check_call(["sudo", "dnf", "install", "-y", "python3-tkinter"])
        elif distro_name == "arch":
            print("Installation de Tkinter pour Arch Linux.")
            subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm", "tk"])

def check_tkinter():
    try:
        import tkinter
        print("Tkinter est déjà installé.")
    except ImportError:
        print("Tkinter n'est pas installé. Tentative d'installation...")
        install_tkinter()

def fetch_minecraft_versions():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        data = response.json()
        # Filtrer pour ne garder que les versions stables
        versions = [version['id'] for version in data['versions'] if version['type'] == 'release']
        return versions
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des versions : {e}")
        return []

def on_play_button_click():
    entered_version = version_entry.get().strip()
    print(f"Version saisie : {entered_version}")

    # Récupère les versions disponibles
    available_versions = fetch_minecraft_versions()

    # Vérifie si la version saisie est dans les versions disponibles
    if 1 == 2 :
        error_message = f"Erreur : La version '{entered_version}' n'est pas valide ou n'est pas disponible."
        print(error_message)
        error_label.config(text=error_message, fg="red")
    else:
        error_label.config(text="")
        print(f"Jouer avec la version : {entered_version}")

        # Commande pour démarrer portablemc avec la version saisie
        try:
            subprocess.check_call([sys.executable, "-m", "portablemc", "start", entered_version])
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'exécution de portablemc : {e}")

def connect():


def main():
    python_version = check_python()
    check_tkinter()

    # Importation tardive de tkinter après installation
    import tkinter as tk

    # Crée une instance de la fenêtre principale
    root = tk.Tk()

    # Définit le titre de la fenêtre
    root.title("FRMC Launcher")

    # Dimensions de la fenêtre (largeur x hauteur)
    root.geometry("400x300")

    # Ajoute un label pour la version
    label_version = tk.Label(root, text="Saisissez la version :")
    label_version.pack(pady=10)

    # Champ de saisie pour entrer la version
    global version_entry
    version_entry = tk.Entry(root)
    version_entry.pack(pady=10)

    # Ajoute un bouton "Jouer"
    play_button = tk.Button(root, text="Jouer", command=on_play_button_click)
    play_button.pack(pady=20)
    login_button = tk.Button(root, text="Se Connecter", command=connect)
    login_button.pack(pady=20)
    # Label pour afficher les messages d'erreur
    global error_label
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack(pady=5)

    # Affiche les informations sur le système et Python
    info_text = f"Système : {platform.system()} {platform.release()}\nPython : {python_version}"
    label_info = tk.Label(root, text=info_text)
    label_info.pack(pady=10)

    # Affiche la fenêtre
    root.mainloop()

if __name__ == "__main__":
    main()
