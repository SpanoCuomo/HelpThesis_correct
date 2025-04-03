


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
# Variabile globale per riutilizzare lo stesso driver
driver = None
debug_mode = False
def setup_driver(user_data_dir, profile_directory):
    global driver
    if driver is not None:
        # Significa che abbiamo già un driver aperto
        return driver  # lo riusiamo

    # Altrimenti creiamo il driver la prima volta
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver



def invia_storia(driver, file_path, testo=""):
    """
    Automatizza la creazione di uno status su WhatsApp Web.
    """
    try:
        stato_tab = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Stato']"))
        )
        stato_tab.click()
        time.sleep(5)  # aumenta se necessario
        print("[DEBUG] Tab Stato cliccato.")
    except Exception as e:
        print("[ERRORE] Non riesco ad accedere alla sezione Stato:", e)
        return

    try:
        aggiungi_stato = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus']"))
        )
        aggiungi_stato.click()
        time.sleep(5)
        print("[DEBUG] Pulsante Aggiungi status cliccato.")
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante Aggiungi status:", e)
        return

    try:
        foto_video_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Foto e video')]"))
        )
        foto_video_button.click()
        time.sleep(5)
        print("[DEBUG] Pulsante 'Foto e video' cliccato.")
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante 'Foto e video':", e)
        return

    try:
        xp_input_file = "//input[@type='file' and contains(@accept,'image')]"
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xp_input_file))
        )
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        time.sleep(5)
        print("[DEBUG] File caricato.")
    except Exception as e:
        print("[ERRORE] Impossibile caricare il file per lo status:", e)
        return

    if testo:
        try:
            xp_text_field = "//div[@contenteditable='true' and @role='textbox']"
            text_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, xp_text_field))
            )
            driver.execute_script("arguments[0].click();", text_field)
            text_field.send_keys(testo)
            time.sleep(2)
            print("[DEBUG] Testo inserito.")
        except Exception as e:
            print("[WARN] Non sono riuscito ad inserire il testo:", e)

    try:
        xp_send_status = "//div[@role='button' and @aria-label='Invia']"
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_status))
        )
        send_button.click()
        print("[OK] Status pubblicato correttamente.")
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione dello status:", e)



    # 4. (Facoltativo) Inserisci un testo se fornito
    if testo:
        try:
            xp_text_field = "//div[@contenteditable='true' and @role='textbox']"
            text_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xp_text_field))
            )
            text_field.click()
            text_field.send_keys(testo)
            time.sleep(1)
        except Exception as e:
            print("[WARN] Non sono riuscito ad inserire il testo:", e)

    # 5. Clicca sul pulsante per pubblicare lo status
    try:
        xp_send_status = "//button[@aria-label='Invia']"
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_status))
        )
        send_button.click()
        print("[OK] Status pubblicato correttamente.")
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione dello status:", e)








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


    

    # Assicurati di avere definito la funzione setup_driver() altrove
    base_url = "https://aiutotesi.altervista.org/blog/"

   # php_file = "https://aiutotesi.altervista.org/blog/posts.php"  # File PHP esterno che contiene l'array dei post
    php_file = r"C:\Users\lspan\Desktop\HelpThesis\HelpThesis_correct/posts.php"
    posts = extract_posts_from_php(php_file, base_url)
   
    
    # Se PC grande
    #setup_driver(
    #    user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data",
    #    profile_directory="Profile 5"
    #)
    
    #Se pc Piccolo
    driver = setup_driver(
        user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data",
        profile_directory="Profile 2"
    )
    
    # Apri WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    # Attendi per il caricamento della pagina e la scansione del QR se necessario
    time.sleep(45)
    
    # Definisci il percorso della cartella dove sono memorizzate le immagini
    base_dir = r"C:\Users\lspan\Desktop\ImmaginiSitoTesi"

    random_posts = random.sample(posts, 5)

    for post in random_posts:
  
    
        print("sto stampando " + post["slug"])
        # Recupera il percorso dell'immagine e il testo (description) dal post
        image_path = post["video"]
        #image_path = post["image"]  # se vuoi immagine 
        # Aggiungiamo lo slug al testo in modo che l'URL sia visibile nello status
        
        #text = post["summary"]  
        text = f"{post['summary']} {base_url}{post['slug']}"
        full_image_path = os.path.join(base_dir, image_path)
        # Invia lo status con l'immagine e il testo
        invia_storia(driver, full_image_path, text)
        
        # Aspetta qualche secondo fra uno status e l'altro (modifica in base alle tue necessità)
        time.sleep(10)
    
    # Dopo aver completato tutte le operazioni:
    driver.quit()