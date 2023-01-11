from bs4 import BeautifulSoup
import os
import requests

def download_resources(response, dirpath, base_url):
    soup = BeautifulSoup(response.text, 'html.parser')

    css_urls = [link['href'] for link in soup.find_all('link', href=True) if link.get('rel')[0] == 'stylesheet']
    js_urls = [script['src'] for script in soup.find_all('script', src=True)]
    img_urls = [img['src'] for img in soup.find_all('img', src=True)]

    css_folder = os.path.join(dirpath, 'CSS')
    js_folder = os.path.join(dirpath, 'JS')
    img_folder = os.path.join(dirpath, 'IMG')
    if not os.path.exists(css_folder):
        os.mkdir(css_folder)
    if not os.path.exists(js_folder):
        os.mkdir(js_folder)
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)

    for url in css_urls:
        if not url.startswith("http"):
            url = base_url + url
        res = requests.get(url)
        filename, file_extension = os.path.splitext(os.path.basename(url))
        filename = filename.replace("?", "_")
        if file_extension in {'.css'}:
            with open(os.path.join(css_folder, filename + file_extension), 'wb') as f:
                f.write(res.content)
        else:
            continue
    for url in js_urls:
        if not url.startswith("http"):
            url = base_url + url
        res = requests.get(url)
        filename, file_extension = os.path.splitext(os.path.basename(url))
        filename = filename.replace("?", "_")
        if file_extension in {'.js'}:
            with open(os.path.join(js_folder, filename + file_extension), 'wb') as f:
                f.write(res.content)
        else:
            continue
    for url in img_urls:
        if not url.startswith("http"):
            url = base_url + url
        res = requests.get(url)
        filename, file_extension = os.path.splitext(os.path.basename(url))
        filename = filename.replace("?", "_")
        if file_extension in {'.jpg', '.jpeg', '.png', '.gif', '.svg'}:
            with open(os.path.join(img_folder, filename + file_extension), 'wb') as f:
                f.write(res.content)
        else:
            continue

url = input("Entrez l'URL de la page web à télécharger : ")
try:
    response = requests.get(url, verify='cacert.pem')
    if response.status_code == 200:
        domain = url.split('/')[2]
        dirpath = domain
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        #Ecrire le fichier html
        with open(os.path.join(dirpath, "example.html"), 'w', encoding='utf-8') as f:
            f.write(response.text)
        # Télécharger les ressources liées
        base_url = 'https://' + url.split('/')[2] + '/'
        download_resources(response, dirpath, base_url)
        
        print("La page a été téléchargée avec succès !")
    else:
        print("Impossible de télécharger la page, erreur HTTP : " + str(response.status_code))
except requests.exceptions.RequestException as e:
    print("Impossible de se connecter au site: ", e)