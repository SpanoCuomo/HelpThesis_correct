
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
from selenium.webdriver import ActionChains
Numero_post_Inserire = 10





def stampa_colore(testo, colore="default"):
    colori = {
        "verde": "\033[92m",
        "rosso": "\033[91m",
        "giallo": "\033[93m",
        "default": "\033[0m"
    }
    print(colori.get(colore, colori["default"]) + testo + colori["default"])





RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RESET  = "\033[0m"
# Variabile globale per riutilizzare lo stesso driver
driver = None
debug_mode = False
# PC_ID: 1 = grande, 2 = piccolo
# PAGE_ID: 1 = Arancione, 2 = Blu (puoi aggiungere 3,4,...)
PC_ID = 1
PAGE_ID = 1
########################
# Mappa centralizzata (estendibile) per profili e URL base
CONFIG = {
    # PAGE_ID 1 = Arancione
    1: {
        "name": "Arancione",
        "base_url": "https://aiutotesi.altervista.org/blog/",
        "profiles": {
            # PC_ID 1 = grande
            1: {"user_data_dir": r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile", "profile_directory": "Default"},
            # PC_ID 2 = piccolo
            2: {"user_data_dir": r"C:\ChromeProfili", "profile_directory": "Profile 2"},
        },
    },
    # PAGE_ID 2 = Blu
    2: {
        "name": "Blu",
        "base_url": "https://aiutotesi.altervista.org/ImmaginiSitoTesi/Video_Blu/",
        "profiles": {
            1: {"user_data_dir": r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile_Blu", "profile_directory": "Default"},
            2: {"user_data_dir": r"C:\ChromeProfili", "profile_directory": "Profile 4"},
        },
    },
    3: {
        "name": "Mininterno",
        "base_url": "https://aiutotesi.altervista.org/ImmaginiSitoTesi/Video_Blu/",
        "profiles": {
            1: {"user_data_dir": r"C:\Users\UTENTE\Desktop\MinInterno", "profile_directory": "Default"},
            2: {"user_data_dir": r"C:\ChromeProfili", "profile_directory": "Profile 4"},
        },
    },
}


DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "fb_status_temp")
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
        
def setup_driver(user_data_dir, profile_directory):
    kill_all_chrome()
    time.sleep(2)

    chrome_options = Options()
    
    # Usa i parametri passati dalla main:
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")

    #chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument("--start-minimized")
    driver = webdriver.Chrome(options=chrome_options)
    #driver.minimize_window()
    driver.maximize_window()

    return driver

        
def pubblica_unico_reel(video_path: str,
                         didascalia: str = "",
                         pc_id: int = PC_ID,
                         page_id: int = PAGE_ID):
     """
     Pubblica UN SOLO video come Reel su Facebook, senza leggere posts.php.
     - video_path: percorso locale o URL http/https
     - didascalia: testo del reel
     - pc_id/page_id: usano i profili già definiti in CONFIG
     """
     kill_all_chrome()
     time.sleep(2)

     if page_id not in CONFIG:
         raise ValueError(f"PAGE_ID sconosciuto: {page_id}")
     page_cfg = CONFIG[page_id]
     if pc_id not in page_cfg["profiles"]:
         raise ValueError(f"PC_ID sconosciuto per PAGE_ID {page_id}: {pc_id}")
     prof = page_cfg["profiles"][pc_id]

     drv = setup_driver(prof["user_data_dir"], prof["profile_directory"])
     stampa_colore(f"✅ Profilo attivo: {page_cfg['name']} | PC_ID={pc_id}", "verde")

     local_media = fetch_to_local(video_path)
     if not local_media or not os.path.exists(local_media):
         stampa_colore("❌ Video non trovato/scaricato", "rosso")
         try: drv.quit()
         except Exception: pass
         return

     drv.get("https://www.facebook.com/")
     time.sleep(8)
     crea_reel_facebook(drv, local_media, didascalia=didascalia)
     try: drv.quit()
     except Exception: pass
     stampa_colore("✔ Reel unico pubblicato.", "verde")
      
        
        

def extract_posts_from_php(source, base_url):
    """
    Estrae i post da uno pseudo-array PHP contenuto in un file (o URL) "posts.php".
    Ritorna una lista di dizionari con chiavi: slug, image, summary, video, full_url.
    """
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
    for slug, img, summ, vid in zip(slugs, images, summaries, videos):
        posts_data.append({
            "slug": slug,
            "image": img,
            "summary": summ,
            "video": vid,
            "full_url": base_url + slug,  # Se vuoi costruire l'URL completo
        })
    return posts_data



# ----------------------------------------------------------------
# FUNZIONE PER INVIARE UNA STORIA SU FACEBOOK
# ----------------------------------------------------------------

def invia_storia_facebook(driver, file_path, testo=""):
    """
    Automatizza la creazione di una storia su Facebook con pulsante link (FACOLTATIVO).
    1) Clicca sul link /stories/create/
    2) Clicca su "Crea una storia con foto"
    3) Carica il file (immagine o video) - verifichiamo se funziona anche per video
    4) Aggiunge (opzionalmente) un pulsante Link
    5) (Opzionale) Inserisce testo
    6) Clicca su "Condividi nella storia"
    """
    # 1. Apri la sezione /stories/create/
    try:
        create_story_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/stories/create/')]"))
        )
        create_story_link.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco ad aprire la sezione Storie (link /stories/create/):", e)
        return

    # 2. Clicca su "Crea una storia con foto" (Attenzione se vuoi caricare un video)
    #    In alcune interfacce potrebbe esserci "Crea una storia con foto/video"
    try:
        photo_option = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Crea una storia con foto')]"))
        )
        photo_option.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a selezionare 'Crea una storia con foto':", e)
        return

    # 3. Carica il file (immagine o video)
    try:
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        time.sleep(5)  # Attendi il caricamento dell'anteprima
    except Exception as e:
        print("[ERRORE] Non riesco a caricare il file:", e)
        return

    # 4. (FACOLTATIVO) Aggiungi il pulsante link
    #    Se non vuoi aggiungere alcun link, commenta questa parte.
    try:
        add_button_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Aggiungi pulsante')]"))
        )
        add_button_btn.click()
        time.sleep(1)
        # Seleziona "Pulsanti Link web"
        link_web_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pulsanti Link web')]"))
        )
        link_web_btn.click()
        time.sleep(1)
        # Inserisci il link (verifica il placeholder o aria-label)
        link_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[@placeholder='Inserisci link']"))
        )
        link_input.send_keys("https://www.aiutotesi.altervista.org")
        time.sleep(1)
        # Clicca su "Fatto"
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Fatto')]"))
        )
        confirm_btn.click()
        time.sleep(1)
    except Exception as e:
        print("[WARN] Non sono riuscito ad aggiungere il pulsante link:", e)

    # 5. (Opzionale) Inserisci testo
    if testo:
        try:
            text_area = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
            )
            text_area.click()
            text_area.send_keys(testo)
            time.sleep(1)
        except Exception as e:
            print("[WARN] Non sono riuscito ad inserire il testo:", e)

    # 6. Condividi la storia
    try:
        share_in_story_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Condividi nella storia')]"))
        )
        share_in_story_btn.click()
        print("[OK] Storia pubblicata correttamente su Facebook.")
        time.sleep(5)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare 'Condividi nella storia':", e)


# ----------------------------------------------------------------
# FUNZIONE PER CREARE UN REEL SU FACEBOOK
# ----------------------------------------------------------------

def click_button(xpath):
        btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        ActionChains(driver).move_to_element(btn).click().perform()
        time.sleep(1.5)



def crea_reel_facebook(driver, video_path, didascalia=""):
   
    print("→ creo Reel si, nuova function")

    # ── 1. pagina reels ───────────────────────────────────────────────
    try:
        driver.get("https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS")
        time.sleep(4)
    except Exception as e:
        print("[ERRORE] apertura pagina Reels:", e)
        return


    # ── 1.1 se compare il pulsante “Crea reel” (profilo Blu), cliccalo
    from selenium.common.exceptions import TimeoutException
    crea_reel_xpaths = [
        "//div[@role='button' and contains(., 'Crea reel')]",
        "//span[normalize-space(text())='Crea un reel']/ancestor::div[@role='button']",
        "//button[normalize-space(text())='Crea reel']",
    ]
    for xp in crea_reel_xpaths:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xp))
            )
            btn.click()
            print(f"[DEBUG] cliccato ‘Crea reel’ con locator: {xp}")
            time.sleep(3)
            break
        except TimeoutException:
            continue

    # ── 2. carica video ───────────────────────────────────────────────
    try:
        up = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        driver.execute_script("arguments[0].style.display='block';", up)
        up.send_keys(video_path)
        time.sleep(5)          # anteprima
    except Exception as e:
        print("[ERRORE] upload video:", e)
        return

 # ── 3. clic su “Avanti” finché non compare il pulsante di condivisione ───────
    # feature‐detection: nuova UI vs vecchia UI
    if driver.find_elements(By.XPATH, "//div[@role='button' and @aria-label='Avanti']"):
        avanti_xpath = "//div[@role='button' and @aria-label='Avanti' and not(@aria-disabled)]"
        share_text   = "Condividi reel"
    else:
        avanti_xpath = "//button[normalize-space(text())='Next']"
        share_text   = "Share Reel"
    print(f"[DEBUG] userà locator Avanti: {avanti_xpath!r}, pulsante finale: {share_text!r}")

    # click “Avanti” fino a due volte
    for i in range(2):
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, avanti_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            btn.click()
            print(f"[OK] Click Avanti #{i+1}")
            time.sleep(2)
        except Exception:
            print(f"[WARN] Avanti #{i+1} non trovato con locator {avanti_xpath}")
            break

    # ── 4. didascalia (opzionale) ─────────────────────────────────────
    def _safe_click_any(xpaths, wait_sec=6):
        for xp in xpaths:
            try:
                el = WebDriverWait(driver, wait_sec).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                el.click()
                print(f"[DEBUG] Click su: {xp}")
                time.sleep(0.8)
                return True
            except Exception:
                continue
        return False

    def _insert_caption_via_js(el, text):
        # Metodo affidabile per editor React/Lexical/Draft
        driver.execute_script("""
            const el = arguments[0];
            const text = arguments[1];
            el.focus();
            try {
              document.execCommand('selectAll', false, null);
              document.execCommand('insertText', false, text);
            } catch (e) {
              el.textContent = text;
            }
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new KeyboardEvent('keydown', {bubbles:true, key:' ', code:'Space'}));
            el.dispatchEvent(new KeyboardEvent('keyup', {bubbles:true, key:' ', code:'Space'}));
        """, el, text)

    inserted = False
    if didascalia:
        # 4.0 Alcune UI richiedono di aprire tab "Dettagli/Details" o il campo "Aggiungi didascalia"
        _safe_click_any([
            "//div[@role='tab' and .//span[normalize-space()='Dettagli']]",
            "//div[@role='tab' and .//span[normalize-space()='Details']]",
            "//span[normalize-space()='Dettagli']/ancestor::div[@role='tab']",
            "//span[normalize-space()='Details']/ancestor::div[@role='tab']",
            "//*[normalize-space()='Aggiungi didascalia' or normalize-space()='Write a caption']",
        ], wait_sec=4)

        # 4.1 Prova con una rosa di locator molto ampia (IT/EN e vari framework FB)
        locator_candidates = [
            # IT / EN placeholder / aria
            "//*[@placeholder='Scrivi una didascalia']",
            "//*[@placeholder='Aggiungi una didascalia']",
            "//*[@aria-label='Aggiungi didascalia']",
            "//*[@aria-label='Scrivi una didascalia']",
            "//*[@placeholder='Write a caption']",
            "//*[@aria-label='Write a caption']",
            # contenteditable / role textbox (Lexical/Draft)
            "//div[@role='textbox' and @contenteditable='true']",
            "//div[@contenteditable='true' and @data-lexical-editor='true']",
            "//div[@contenteditable='true' and contains(@aria-placeholder,'reel')]",
            "//div[@contenteditable='true']",
            # alcuni casi: textarea "classico"
            "//textarea[@name='caption' or @aria-label='Caption' or @placeholder='Caption']",
        ]

        for xp in locator_candidates:
            try:
                el = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xp)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                driver.execute_script("arguments[0].focus();", el)
                time.sleep(0.2)

                tag = el.tag_name.lower()
                if tag == "input" or tag == "textarea":
                    try:
                        el.clear()
                    except Exception:
                        pass
                    el.send_keys(didascalia)
                else:
                    # contenteditable: usa metodo JS robusto
                    _insert_caption_via_js(el, didascalia)

                # assicurati che la UI recepisca la modifica
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", el)
                try:
                    el.send_keys(Keys.TAB)
                except Exception:
                    pass

                print(f"[OK] didascalia inserita con locator: {xp}")
                inserted = True
                break
            except Exception:
                continue

    if not inserted and didascalia:
        print("[WARN] didascalia NON inserita: nessun locator ha funzionato su questa UI")

    if inserted:
        print("[OK] didascalia inserita correttamente")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    time.sleep(5)
    print("Arrivato al Pubblica")
    # ── 5. pubblica ───────────────────────────────────────────────────
    
        # ── 5. pubblica ────────────────────────────────────────────────
    pub_btn = None
    for _ in range(4):                    # max 3 tentativi / 3 s
        try:
            pub_btn = WebDriverWait(driver, 1).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    'div[role="button"][aria-label="Pubblica"]'
                )
            )
            if pub_btn.get_attribute("aria-disabled") == "false":
                time.sleep(1)
                continue
            break
        except Exception:
            time.sleep(1)
    if pub_btn and pub_btn.get_attribute("aria-disabled") != "true":
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pub_btn)
        # click via JS per bypassare overlay
        driver.execute_script("arguments[0].click();", pub_btn)
        print("✔ Reel pubblicato correttamente (via aria-label='Pubblica')")
    else:
        # 2) Fallback: cerco qualsiasi button role=button che contenga il testo giusto
        found = False
        all_btns = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        for b in all_btns:
            text = b.text.strip().lower()
            if "pubblica" in text or "condividi reel" in text or "share reel" in text:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", b)
                driver.execute_script("arguments[0].click();", b)
                print(f"✔ Reel pubblicato correttamente (fallback su '{b.text.strip()}')")
                found = True
                break
        if not found:
            print("[ERRORE] impossibile trovare il pulsante di pubblicazione")
    # lascio un attimo di margine per la post-pubblicazione
    time.sleep(5)


    # ── 6. Chiudi l'overlay di conferma per tornare alla schermata principale ─────────
    try:
        # Proviamo a chiudere con il tasto 'ESC'
        from selenium.webdriver.common.keys import Keys
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
    except Exception:
        pass

    try:
        # Oppure cerchiamo un pulsante "Chiudi" o "Done"
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//div[@role='button' and (normalize-space(@aria-label)='Chiudi' or normalize-space(text())='Chiudi' or normalize-space(text())='Done')]"
            ))
        )
        close_btn.click()
        time.sleep(1)
    except Exception:
        pass




# ----------------------------------------------------------------
# ESEMPIO DI CODICE CHE CHIAMA LE FUNZIONI
# ----------------------------------------------------------------

# if __name__ == "__main__":
#     # Esempio di quanti post caricare
#     NUMERO_POST_INSERIRE = 10

#     kill_all_chrome()
#     # 2) Lascia un paio di secondi di “respiro” per essere sicuro
#     time.sleep(5)
    
#     print(GREEN + "[OK] Dopo il kill" + RESET)
    
    
    
    
    
    
#     if PC_Grande == True and Arancione == True:   
#    # Se PC grande
#        driver =setup_driver(
#             user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data",
#             profile_directory="Profile 5"
#         )
#     elif PC_Grande == False and Arancione == True:     
#         #Se pc Piccolo
#         driver = setup_driver(
#             user_data_dir=r"C:\ChromeProfili",
#             profile_directory="Profile 2"
#         )
#     if PC_Grande == True and Arancione == False:   
#    # Se PC grande
#        driver =setup_driver(
#             user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data",
#             profile_directory="Devi crearlo"
#         )
#     elif PC_Grande == False and Arancione == False:     
#         #Se pc Piccolo
#         driver = setup_driver(
#             user_data_dir=r"C:\ChromeProfili",
#             profile_directory="Profile 4"
#         )
    
    

    
#     print(GREEN + "[OK] Setup Finito" + RESET)
    
#     # Modalità di pubblicazione: "storia", "reel" o "auto" (default alterna)
#     publish_mode = "reel"  # cambia in "storia" o "reel" se vuoi forzare




#     # 2) Legge i post dal tuo file PHP (remoto o locale)
#     if Arancione == True:
#         base_url = "https://aiutotesi.altervista.org/blog/"
#         php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
#     else: 
#         base_url = "https://aiutotesi.altervista.org/ImmaginiSitoTesi/Video_Blu/"
#         php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
    
#     local_php = fetch_to_local(php_url_raw)  # Scarica in locale il contenuto "raw" di posts.php
#     #print(local_php)
#     posts = extract_posts_from_php(local_php, base_url)
#     #print(posts)
#     # 3) Scarica in locale i file immagine/video (con thread pool, per velocizzare)
#     #    Prima raccogliamo le URL in una lista
#     urls_da_scaricare = []
#     for idx, p in enumerate(posts[:NUMERO_POST_INSERIRE]):
#         if idx % 2 == 0 and p["video"]:
#             media_rel_path = p["video"]
#         else:
#             media_rel_path = p["image"]
#         if not media_rel_path:
#             continue
#         # URL originale
#         orig_url = base_url + media_rel_path
#         urls_da_scaricare.append(orig_url)
#         # se siamo nella cartella Video_Blu e si tratta di un video,
#         # aggiungiamo anche la versione "_blu"
#         if Arancione== False and media_rel_path.lower().endswith((".mp4", ".mov", ".avi")):
#             name, ext = os.path.splitext(media_rel_path)
#             blu_rel = f"{name}_blu{ext}"
#             blu_url = base_url + blu_rel
#             urls_da_scaricare.append(blu_url)
#     print(GREEN + "[OK] Materiale Scaricato" + RESET)
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         future_to_url = {executor.submit(fetch_to_local, u): u for u in urls_da_scaricare}
#         local_paths = {}
#         for fut in as_completed(future_to_url):
#             url = future_to_url[fut]
#             local_file = fut.result()  # None se fallito
#             if local_file:
#                 local_paths[url] = local_file
    
#     # 4) Vai su Facebook home, per sicurezza
#     driver.get("https://www.facebook.com/")
#     time.sleep(10)  # tempo di caricamento pagina
    
#     print(GREEN + "[OK] Aperto Facebook" + RESET)
#     # 5) Pubblica ciclicamente su Facebook (storia o reel) in base alla logica

#     for idx, p in enumerate(posts[:NUMERO_POST_INSERIRE]):
#         print(f"\n\n step {idx+1}")
#         # determina modalità attuale
#         if publish_mode == "reel":
#             mode = "reel"
#         elif publish_mode == "storia":
#             mode = "storia"
#         else:  # auto
#             mode = "reel" if (idx % 2 == 0 and p["video"]) else "storia"

#         # forziamo cambio se non disponibile
#         if mode == "reel" and not p["video"]:
#             print("[WARN] nessun video, passo a storia")
#             mode = "storia"
#         if mode == "storia" and not p["image"]:
#             print("[WARN] nessuna immagine, passo a reel")
#             mode = "reel"
        
#         print(GREEN + '[mode]: '+  mode + RESET)
#         # se siamo nel folder Video_Blu e Arancione=False, i file video finiscono in "_blu.ext"
#  # costruiamo l’URL del media: col suffisso _blu per i reel in Video_Blu, con fallback all’originale
#         # Se è un reel e siamo in Video_Blu, tenta prima il suffisso "_blu"
#         if mode == "reel" and not Arancione:
#             orig_rel = p["video"]
#             name, ext = os.path.splitext(orig_rel)
#             blu_rel = f"{name}_blu{ext}"
#             blu_url = base_url + blu_rel
#             if blu_url in local_paths:
#                 full_url_media = blu_url
#                 local_media = local_paths[blu_url]
#             else:
#                 orig_url = base_url + orig_rel
#                 full_url_media = orig_url
#                 local_media = local_paths.get(orig_url)
#         else:
#             # Storia o reel “normale”
#             full_url_media = base_url + (p["video"] if mode == "reel" else p["image"])
#             local_media = local_paths.get(full_url_media)

#         # lookup case-insensitive finale, se ancora non trovato
#         # lookup case‐insensitive finale, se ancora non trovato
#         if not local_media:
#             for url, path in local_paths.items():
#                 if url.lower() == full_url_media.lower():
#                     local_media = path
#                     break
#         if not local_media:
#             print(f"[WARN] non posso scaricare il file: {full_url_media} (lookup case-insensitive fallito)")
#             continue
#         if not local_media:

#             print(f"[WARN] non posso scaricare il file: {full_url_media} (case-insensitive lookup fallito)")
#             continue

#         if mode == "reel":
#             didascalia = f"{p['summary']} {full_url_media}"
#             crea_reel_facebook(driver, local_media, didascalia=didascalia)
#         else:
#             testo_storia = f"{p['summary']} {full_url_media}"
#             invia_storia_facebook(driver, local_media, testo_storia)

#         time.sleep(10)



def invia_storie_facebook(pc_id: int = PC_ID, page_id: int = PAGE_ID, numero_post: int = 1, publish_mode: str = "auto"):
    global missing_media

    kill_all_chrome()
    time.sleep(2)

    # Configura profilo Chrome in base ai parametri


# --- NUOVO: lookup da CONFIG con validazioni chiare ---
    if page_id not in CONFIG:
        raise ValueError(f"PAGE_ID sconosciuto: {page_id}. Definisci la pagina in CONFIG.")
    page_cfg = CONFIG[page_id]
    if pc_id not in page_cfg["profiles"]:
        raise ValueError(f"PC_ID sconosciuto per PAGE_ID {page_id}: {pc_id}. Aggiungi il profilo in CONFIG.")

    user_data_dir = page_cfg["profiles"][pc_id]["user_data_dir"]
    profile_directory = page_cfg["profiles"][pc_id]["profile_directory"]
    stampa_colore(f"✅ Profilo: PC_ID={pc_id} | PAGE_ID={page_id} ({page_cfg['name']})", "verde")
 

    driver = setup_driver(user_data_dir, profile_directory)
    stampa_colore(f"✅ Setup_driver: {driver}", "verde")

    # Scegli URL in base ad "arancione"
    base_url = page_cfg["base_url"]
    php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"
    local_php = fetch_to_local(php_url_raw)
    posts = extract_posts_from_php(local_php, base_url)
    random.shuffle(posts)
    urls_da_scaricare = []
    for idx, p in enumerate(posts[:numero_post]):
        rel = p["video"] if idx % 2 == 0 and p["video"] else p["image"]
        if rel:
            orig_url = base_url + rel
            urls_da_scaricare.append(orig_url)
            if page_id != 1 and rel.lower().endswith((".mp4", ".mov", ".avi")):
                name, ext = os.path.splitext(rel)
                blu_rel = f"{name}_blu{ext}"
                urls_da_scaricare.append(base_url + blu_rel)

    stampa_colore("📌 Inizio download dei file multimediali...", "giallo")
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_to_local, u): u for u in urls_da_scaricare}
        local_paths = {}
        for fut in as_completed(future_to_url):
            url = future_to_url[fut]
            local = fut.result()
            if local:
                stampa_colore(f"✅ Scaricato correttamente: {url}", "verde")
                local_paths[url] = local
            else:
                stampa_colore(f"❌ Errore nel download: {url}", "rosso")

    driver.get("https://www.facebook.com/")
    stampa_colore("📌 Attesa iniziale (Facebook)...", "giallo")
    time.sleep(20)

    for idx, p in enumerate(posts[:numero_post]):
        if publish_mode == "reel":
            mode = "reel"
        elif publish_mode == "storia":
            mode = "storia"
        else:
            mode = "reel" if (idx % 2 == 0 and p["video"]) else "storia"

        rel = p["video"] if mode == "reel" else p["image"]
        if not rel:
            stampa_colore(f"[⚠️ WARN] Nessun media disponibile per il post {idx+1}", "giallo")
            continue

        full_url_media = base_url + rel
        local_media = local_paths.get(full_url_media)

        if mode == "reel" and page_id != 1:
            name, ext = os.path.splitext(rel)
            blu_url = f"{base_url}{name}_blu{ext}"
            local_media = local_paths.get(blu_url, local_media)

        if not local_media:
            stampa_colore(f"[⚠️ WARN] File locale non trovato: {full_url_media}", "giallo")
            continue

        testo = f"{p['summary']} {base_url}{p['slug']}"

        if mode == "reel":
            crea_reel_facebook(driver, local_media, didascalia=testo)
        else:
            invia_storia_facebook(driver, local_media, testo)

        time.sleep(18)

    driver.quit()
    stampa_colore("✅ Tutti i contenuti pubblicati correttamente!", "verde")
