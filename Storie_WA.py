# Inserire una volta immagine, una volta video, altrimenti che ho a fare le immagini?
# Vedi se puoiparalizzarlo ma non so se ne valga la pena
# inserisci tutte le storie e screen da posts.php
# Magari vedere anche le risposte dei clienti e parti di esercizi già svolti

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

from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
from urllib.parse import urlparse

Numero_post_Inserire = 10

Numero_post_Inserire = 10
# Variabile globale per riutilizzare lo stesso driver
driver = None
debug_mode = False

PC_Grande = True















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




import subprocess

# Funzione per stampare messaggi colorati
def stampa_colore(testo, colore="default"):
    colori = {
        "verde": "\033[92m",
        "rosso": "\033[91m",
        "giallo": "\033[93m",
        "default": "\033[0m"
    }
    print(colori.get(colore, colori["default"]) + testo + colori["default"])

def kill_all_chrome():
    stampa_colore("📌 Sto provando a chiudere Chrome e ChromeDriver...", "giallo")
    chiuso = True
    for proc in ("chrome.exe", "chromedriver.exe"):
        risultato = subprocess.call(
            ["taskkill", "/F", "/IM", proc, "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if risultato == 0:
            stampa_colore(f"✅ {proc} terminato correttamente.", "verde")
        else:
            stampa_colore(f"⚠️ {proc} non trovato o non terminato.", "rosso")
            chiuso = False

    if chiuso:
        stampa_colore("Tutti i processi Chrome sono stati terminati correttamente.", "verde")
    else:
        stampa_colore("Alcuni processi non erano in esecuzione o non sono stati chiusi.", "giallo")
   
        
def setup_driver(user_data_dir, profile_directory):
   
    chrome_options = Options()

    # Adesso usiamo correttamente gli argomenti passati
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument("--start-minimized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
#driver.minimize_window()

    return driver













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
  

# if __name__ == "__main__":
#     kill_all_chrome()
#     time.sleep(2)
#     if PC_Grande:   
#         stampa_colore(f"✅ Sono nel PC grande", "verde")

#         driver = setup_driver(
#             user_data_dir=r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile",
#             profile_directory="Profile 5"
#         )
#         stampa_colore(f"✅ Setup_driver: {driver}", "verde")
#     else:     
#         driver = setup_driver(
#             user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data",
#             profile_directory="Profile 2"
#         )
  
  
#     # Assicurati di avere definito la funzione setup_driver() altrove
#     base_url = "https://aiutotesi.altervista.org/blog/"

#     #php_file = r"https://aiutotesi.altervista.org/blog/posts.php"  # File PHP esterno che contiene l'array dei post
#     #php_file = r"C:\Users\lspan\Desktop\HelpThesis\HelpThesis_correct/posts.php"
#     # scarico il sorgente PHP in locale
#     php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
#     local_php = fetch_to_local(php_url_raw)
#     posts = extract_posts_from_php(local_php, base_url)

#     # print("posts", posts)
    

#     urls = []
#     for idx, p in enumerate(posts[:Numero_post_Inserire]):
#         rel = p["video"] if idx % 2==0 and p["video"] else p["image"]
#         if rel: urls.append(base_url + rel)

#     # 1) lancio i download
#     # 1) lancio i download
#     stampa_colore("📌 Inizio download dei file multimediali...", "giallo")
#     with ThreadPoolExecutor(max_workers=5) as exe:
#         future_to_url = {exe.submit(fetch_to_local, u): u for u in urls}
#         local_paths = {}
#         for fut in as_completed(future_to_url):
#             url = future_to_url[fut]
#             local = fut.result()
#             if local:
#                 stampa_colore(f"✅ Scaricato correttamente: {url}", "verde")
#                 local_paths[url] = local
#             else:
#                 stampa_colore(f"❌ Errore nel download: {url}", "rosso")

#     if missing_media:
#         stampa_colore("\n⚠️ I seguenti media non sono stati trovati o scaricati:", "rosso")
#         for url in missing_media:
#             stampa_colore(f" - {url}", "rosso")
#     else:
#         stampa_colore("\n✅ Tutti i media scaricati correttamente!", "verde")


#     # 2) apri WhatsApp
    
#     driver.get("https://web.whatsapp.com/")
#     time.sleep(45)

#     # 3) invia
#     for idx, p in enumerate(posts[:Numero_post_Inserire]):
#         rel = p["video"] if idx % 2 == 0 and p["video"] else p["image"]
#         if not rel:
#             stampa_colore(f"[⚠️] Nessun media disponibile per il post {idx}", "giallo")
#             continue

#         url_completo = base_url + rel
#         local_path = fetch_to_local(url_completo)

#         if local_path and os.path.exists(local_path):
#             stampa_colore(f"✅ Invio il file locale: {local_path}", "verde")
#             testo = f"{p['summary']} {base_url}{p['slug']}"
#             invia_storia(driver, local_path, testo)
#         else:
#             stampa_colore(f"[❌ ERRORE] File locale non trovato o non scaricato: {url_completo}", "rosso")
        
#         time.sleep(8)
#     driver.quit()
        
#     if missing_media:
#         print("\nI seguenti media non sono stati trovati o scaricati:")
#         for url in missing_media:
#             print(" -", url)


def invia_storie_whatsapp(pc_grande=True, numero_post=10):
    kill_all_chrome()
    time.sleep(2)

    # Configura driver in base al PC
    if pc_grande:
        user_data_dir = r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
        stampa_colore(f"✅ Sono nel PC grande", "verde")
    else:
        user_data_dir = r"C:\Users\lspan\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
        stampa_colore(f"✅ Sono nel PC piccolo", "verde")

    driver = setup_driver(user_data_dir, profile_directory)
    stampa_colore(f"✅ Setup_driver: {driver}", "verde")

    base_url = "https://aiutotesi.altervista.org/blog/"
    php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
    local_php = fetch_to_local(php_url_raw)
    posts = extract_posts_from_php(local_php, base_url)

    urls = []
    for idx, p in enumerate(posts[:numero_post]):
        rel = p["video"] if idx % 2 == 0 and p["video"] else p["image"]
        if rel:
            urls.append(base_url + rel)

    stampa_colore("📌 Inizio download dei file multimediali...", "giallo")
    with ThreadPoolExecutor(max_workers=5) as exe:
        future_to_url = {exe.submit(fetch_to_local, u): u for u in urls}
        local_paths = {}
        for fut in as_completed(future_to_url):
            url = future_to_url[fut]
            local = fut.result()
            if local:
                stampa_colore(f"✅ Scaricato correttamente: {url}", "verde")
                local_paths[url] = local
            else:
                stampa_colore(f"❌ Errore nel download: {url}", "rosso")

    if missing_media:
        stampa_colore("\n⚠️ I seguenti media non sono stati trovati o scaricati:", "rosso")
        for url in missing_media:
            stampa_colore(f" - {url}", "rosso")
    else:
        stampa_colore("\n✅ Tutti i media scaricati correttamente!", "verde")

    driver.get("https://web.whatsapp.com/")
    stampa_colore("📌 Attesa iniziale (WhatsApp Web)...", "giallo")
    time.sleep(45)

    for idx, p in enumerate(posts[:numero_post]):
        rel = p["video"] if idx % 2 == 0 and p["video"] else p["image"]
        url = base_url + rel
        local = local_paths.get(url)
        if not local:
            stampa_colore(f"[⚠️ WARN] salto {url}", "giallo")
            continue
        testo = f"{p['summary']} {base_url}{p['slug']}"
        invia_storia(driver, local, testo)
        time.sleep(18)

    driver.quit()