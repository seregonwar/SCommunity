import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webview
from bs4 import BeautifulSoup
import requests

# Funzione per ottenere il nuovo indirizzo dal sito web
def get_updated_link():
    url = "https://infotelematico.com/streaming-community/"
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        link_elements = soup.select("ul li mark")
        links = [element.text for element in link_elements]
        return links
    except Exception as e:
        print("Errore durante il recupero dei link:", str(e))
        return []

# Funzione per controllare la validità dei link
def check_link_validity(link):
    try:
        response = requests.head(link)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# Funzione per controllare l'aggiornamento del link all'avvio dell'app
def check_for_update():
    links = get_updated_link()
    if links:
        print("Link trovati:", links)
        new_link = links[-1]  # Prende l'ultimo link nella lista
        print("Nuovo indirizzo trovato:", new_link)
        if check_link_validity(new_link):
            print("Il link e' valido.")
            login_url = new_link + "/login"
            show_login_page(login_url)
        else:
            print("Il link non e' valido.")
    else:
        print("Nessun link trovato.")

# Funzione per visualizzare la pagina di login nell'applicazione
def show_login_page(url):
    window.withdraw()  # Nasconde la finestra principale
    login_window = tk.Toplevel(window)  # Crea una nuova finestra per la pagina di login
    login_window.title("Login")
    login_window.geometry("800x600")

    # Funzione per chiudere la finestra di login e tornare alla finestra principale
    def close_login_window():
        login_window.destroy()
        window.deiconify()  # Mostra nuovamente la finestra principale

    # Widget WebView per visualizzare la pagina di login
    login_webview = webview.WebView(login_window)
    login_webview.pack(fill=tk.BOTH, expand=True)
    login_webview.load_url(url)

    # Gestione dell'evento di chiusura della finestra di login
    login_window.protocol("WM_DELETE_WINDOW", close_login_window)

# Creazione dell'interfaccia grafica dell'app
window = tk.Tk()
window.title("App Streaming Community")
window.geometry("800x600")

# Pulsante per il login
login_button = ttk.Button(window, text="Login", command=check_for_update)
login_button.pack()

# Esecuzione dell'app
window.mainloop()
