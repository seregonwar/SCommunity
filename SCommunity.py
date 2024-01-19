from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from bs4 import BeautifulSoup
import requests
import sys

class App(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.main_window = QMainWindow()

    def show_login_page(self, url):
        view = QWebEngineView()
        view.load(QUrl(url))
        self.main_window.setCentralWidget(view)
        self.main_window.show()

def get_updated_link():
    url = "https://www.informarea.it/streamingcommunity-nuovo-indirizzo/"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.567 Safari/537.36',
            'X-XSRF-TOKEN': 'eyJpdiI6ImRESzc0NlhxekVqREQ4WFIzdWtTYmc9PSIsInZhbHVlIjoiNm9iRmJNdHdFRlZoSzRqNEFBT2pJc0srUzVhYS9kNitDTXpMdGtiSHA1aVoxbHBkYnhZbVphaTVqT3RKNXNING9BYjF3aGsyK1lSa2RWTm5ZSmVoRGFMdlBWZnNHbmF3WmxtQXh5OVhpaVdMdDR5V1YwOEUvWmF0N3kwOUVXNUQiLCJtYWMiOiI2OTRkMTU4NmQ5OWQxMDExZDg2Y2QxYjgzMmQ2N2JmN2M5NTZhMzY0NjFjOTUxMDc2OWNmNzU1ZTdmODljYjk1IiwidGFnIjoiIn0%3D',
            'Cookie': 'eyJpdiI6InVPemVTNmNLSmowZkxYdU10V2xja2c9PSIsInZhbHVlIjoiSWxmU25NZitOZGIvSzE2MWZaMEUzZWRjQlV4KzViM2pSd0tvZjJKdTliemVJVFdjaS9zQkkvdWwxdEdCQWllclAzQUVFckRUVW9PaGd4OWgwbUJQeGhxc1lTT3lKZGZQaDBGRmFHR01rakZBc2dWbkhuVGxNd2FPeWJRWDUvZHoiLCJtYWMiOiI3ZjI0MjVmMTZmMjhlN2E2ZjdkZWFkZjNlMGYxM2Y4NjI2NThkZDU0MGJlOWI4NTE4Y2MyY2Y2MDE3YjBiMDgyIiwidGFnIjoiIn0%3D'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        link_elements = soup.select("ul li strong span[style='color: #ff0000;']")
        links = [element.text.strip() for element in link_elements]
        return links
    except requests.RequestException as e:
        print("Errore durante il recupero dei link:", str(e))
        return []


def check_link_validity(link):
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_for_update():
    links = get_updated_link()
    if links:
        print("Link trovati:", links)
        new_link = links[-1]
        print("Nuovo indirizzo trovato:", new_link)
        if check_link_validity(new_link):
            print("Il link è valido.")
            login_url = new_link + "/login"
            app.show_login_page(login_url)
        else:
            print("Il link non è valido.")
    else:
        print("Nessun link trovato.")

if __name__ == "__main__":
    app = App(sys.argv)
    check_for_update()
    sys.exit(app.exec_())

