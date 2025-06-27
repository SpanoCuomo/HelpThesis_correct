# Inserire una volta immagine, una volta video, altrimenti che ho a fare le immagini?
# Vedi se puoiparalizzarlo ma non so se ne valga la pena
# inserisci tutte le storie e screen da posts.php
# Magari vedere anche le risposte dei clienti e parti di esercizi già svolti
<<<<<<< HEAD

=======
# Manca  PC_Grande utilizzo- è tutto fisso
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import requests
import re
import os
import random
import subprocess
import sys
<<<<<<< HEAD

from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
from urllib.parse import urlparse

Numero_post_Inserire = 10
=======
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
from urllib.parse import urlparse
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)

Numero_post_Inserire = 10
# Variabile globale per riutilizzare lo stesso driver
driver = None
debug_mode = False
<<<<<<< HEAD

PC_Grande = False

=======
PC_Grande = False
########################
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)














DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "whatsapp_status_imgs")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


missing_media = []


def fetch_to_local(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        filename = os.path.basename(urlparse(path_or_url).path)
        local_path = os.path.join(DOWNLOAD_DIR, filename)
        if not os.path.exists(local_path):
            try:
                resp = requests.get(path_or_url, stream=True)
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
            except requests.exceptions.HTTPError:
                print(f"[WARN] Media non trovato: {path_or_url}")
                missing_media.append(path_or_url)
                return None
            except Exception as e:
                print(f"[WARN] Errore scaricando {path_or_url}: {e}")
                missing_media.append(path_or_url)
                return None
        return local_path
    else:
        return path_or_url




def kill_all_chrome():
    """
    Termina forzatamente tutti i processi chrome.exe e chromedriver.exe
    su Windows, così liberi il profilo prima di aprire una nuova sessione.
    """
    for proc in ("chrome.exe", "chromedriver.exe"):
        subprocess.call(
            ["taskkill", "/F", "/IM", proc, "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        
        
<<<<<<< HEAD
=======


>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)
def setup_driver(user_data_dir, profile_directory):
    kill_all_chrome()
    time.sleep(2)

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=D:\\ChromeProfili\\ProfiloDidattica")
    chrome_options.add_argument("--profile-directory=Profile 2")
    chrome_options.add_argument("--remote-debugging-port=9222")
<<<<<<< HEAD

    driver = webdriver.Chrome(options=chrome_options)
    return driver



=======
    
    # Aggiungi queste due righe:
    chrome_options.add_argument("--start-minimized")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # E questa:
    driver.minimize_window()

    return driver
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)







def invia_storia(driver, file_path, testo=""):
    """
    Automatizza la creazione di uno status su WhatsApp Web:
    1. Clicca sul tab "Stato".
    2. Clicca sul pulsante per aggiungere un nuovo status (icona plus).
    3. Clicca sul pulsante "Foto e video".
    4. Carica il file (immagine o video) tramite l'input file.
    5. (Facoltativo) Inserisce un testo se fornito.
    6. Pubblica lo status.
    """
    # 1. Vai alla sezione "Stato"
    try:
        stato_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Stato']"))
        )
        stato_tab.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco ad accedere alla sezione Stato:", e)
        return

    # 2. Clicca sul pulsante per aggiungere un nuovo status (icona plus)
    try:
        aggiungi_stato = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus']"))
        )
        aggiungi_stato.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante Aggiungi status:", e)
        return

    # 3. Clicca sul pulsante "Foto e video"
    try:
        foto_video_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Foto e video')]"))
        )
        foto_video_button.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante 'Foto e video':", e)
        return

    # 4. Carica il file (immagine o video)
    try:
        # Modifica qui il selettore in modo da accettare anche i video
        xp_input_file = "//input[@type='file' and (contains(@accept,'image') or contains(@accept,'video'))]"
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xp_input_file))
        )
        # Se l'input è nascosto, forziamo la visualizzazione
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Impossibile caricare il file per lo status:", e)
        return

    # 5. (Facoltativo) Inserisci un testo se fornito
    if testo:
        try:
            xp_text_field = "//div[@contenteditable='true' and @role='textbox']"
            text_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xp_text_field))
            )
            # Forza il click via JavaScript se l'elemento non è cliccabile direttamente
            driver.execute_script("arguments[0].click();", text_field)
            text_field.send_keys(testo)
            time.sleep(1)
        except Exception as e:
            print("[WARN] Non sono riuscito ad inserire il testo:", e)

    # 6. Clicca sul pulsante per pubblicare lo status
    try:
        xp_send_status = "//div[@role='button' and @aria-label='Invia']"
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_status))
        )
        send_button.click()
        print("[OK] Status pubblicato correttamente.")
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione dello status:", e)




def extract_posts_from_php(source, base_url):
    if source.startswith("http"):
        response = requests.get(source)
        content = response.text
    else:
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

    # Rimuove i ritorni a capo per semplificare il parsing
    content = " ".join(content.split())
    pattern_slug = re.compile(r"""['"]slug['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_image = re.compile(r"""['"]image['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_summary = re.compile(r"""['"]summary['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_video = re.compile(r"""['"]video['"]\s*=>\s*['"]([^'"]+)['"]""")

    slugs = pattern_slug.findall(content)
    images = pattern_image.findall(content)
    summaries = pattern_summary.findall(content)
    videos = pattern_video.findall(content)

    posts_data = []
    # Assumiamo che tutti gli array abbiano la stessa lunghezza
    for slug, img, summ, vid in zip(slugs, images, summaries, videos):
        posts_data.append({
            "slug": slug,
            "image": img,
            "summary": summ,
            "video": vid,
            "full_url": base_url + slug,
        })
    return posts_data
  
if __name__ == "__main__":

    kill_all_chrome()
    # 2) Lascia un paio di secondi di “respiro” per essere sicuro
    time.sleep(2)
<<<<<<< HEAD
    if PC_Grande == True:   
=======
    if PC_
    +ande == True:   
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)
   # Se PC grande
       setup_driver(
            user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data",
            profile_directory="Profile 5"
        )
    else:     
        #Se pc Piccolo
        driver = setup_driver(
            user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data",
            profile_directory="Profile 2"
        )
    print("Setup_driver:", setup_driver)



    

    # Assicurati di avere definito la funzione setup_driver() altrove
    base_url = "https://aiutotesi.altervista.org/blog/"

    #php_file = r"https://aiutotesi.altervista.org/blog/posts.php"  # File PHP esterno che contiene l'array dei post
    #php_file = r"C:\Users\lspan\Desktop\HelpThesis\HelpThesis_correct/posts.php"
    # scarico il sorgente PHP in locale
    php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
    local_php = fetch_to_local(php_url_raw)
    posts = extract_posts_from_php(local_php, base_url)

    # print("posts", posts)
    

    urls = []
    for idx, p in enumerate(posts[:Numero_post_Inserire]):
        rel = p["video"] if idx % 2==0 and p["video"] else p["image"]
        if rel: urls.append(base_url + rel)

    # 1) lancio i download
    with ThreadPoolExecutor(max_workers=5) as exe:
        future_to_url = {exe.submit(fetch_to_local, u): u for u in urls}
        local_paths = {}
        for fut in as_completed(future_to_url):
            url = future_to_url[fut]
            local = fut.result()  # None se fallito
            if local: local_paths[url] = local

    # 2) apri WhatsApp
    
    driver.get("https://web.whatsapp.com/")
    time.sleep(45)

    # 3) invia
    for idx, p in enumerate(posts[:Numero_post_Inserire]):
        rel = p["video"] if idx%2==0 and p["video"] else p["image"]
        url = base_url + rel
        local = local_paths.get(url)
        if not local:
            print(f"[WARN] salto {url}")
            continue
        testo = f"{p['summary']} {base_url}{p['slug']}"
        invia_storia(driver, local, testo)
        time.sleep(8)
    driver.quit()
        
    if missing_media:
        print("\nI seguenti media non sono stati trovati o scaricati:")
        for url in missing_media:
            print(" -", url)
