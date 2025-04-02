import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setup_driver(user_data_dir, profile_directory):
    """
    Crea e restituisce un driver Chrome utilizzando il profilo specificato.
    """
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def invia_storia(driver, file_path, testo=""):
    """
    Automatizza la creazione di uno status su WhatsApp Web:
    1. Naviga nella sezione "Stato"
    2. Clicca sul pulsante per aggiungere un nuovo status (icona plus)
    3. Clicca sul pulsante "Foto e video"
    4. Carica il file (immagine o video)
    5. (Facoltativo) Inserisce un testo se fornito
    6. Pubblica lo status
    """
    try:
        stato_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Stato']"))
        )
        stato_tab.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco ad accedere alla sezione Stato:", e)
        return

    try:
        aggiungi_stato = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus']"))
        )
        aggiungi_stato.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante Aggiungi status:", e)
        return

    try:
        foto_video_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Foto e video')]"))
        )
        foto_video_button.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante 'Foto e video':", e)
        return

    try:
        xp_input_file = "//input[@type='file' and contains(@accept,'image')]"
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xp_input_file))
        )
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Impossibile caricare il file per lo status:", e)
        return

    if testo:
        try:
            xp_text_field = "//div[@contenteditable='true' and @role='textbox']"
            text_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xp_text_field))
            )
            driver.execute_script("arguments[0].click();", text_field)
            text_field.send_keys(testo)
            time.sleep(1)
        except Exception as e:
            print("[WARN] Non sono riuscito ad inserire il testo:", e)

    try:
        xp_send_status = "//div[@role='button' and @aria-label='Invia']"
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_status))
        )
        send_button.click()
        print("[OK] Status pubblicato correttamente.")
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione dello status:", e)

def extract_posts_from_php(file_path, base_url):
    """
    Legge il file PHP (che contiene l'array $posts) ed estrae i valori associati alle chiavi
    "slug", "summary" e "image". Prepone la base_url allo slug per ottenere l'URL completo.
    Restituisce una lista di dizionari, uno per post.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Rimuovi newline per semplificare le regex
    content = " ".join(content.split())
    # Trova tutti i blocchi che corrispondono a un post (tra { e })
    posts_blocks = re.findall(r'\{(.*?)\}', content)
    posts = []
    for block in posts_blocks:
        slug_match = re.search(r'"slug"\s*=>\s*"([^"]+)"', block)
        summary_match = re.search(r'"summary"\s*=>\s*"([^"]+)"', block)
        image_match = re.search(r'"image"\s*=>\s*"([^"]+)"', block)
        if slug_match:
            post = {}
            post["slug"] = base_url + slug_match.group(1)
            if summary_match:
                post["summary"] = summary_match.group(1)
            if image_match:
                post["image"] = image_match.group(1)
            posts.append(post)
    return posts

if __name__ == "__main__":
    # Configura il driver (modifica i percorsi come necessario)
    
    
    
    
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
    driver.get("https://web.whatsapp.com/")
    time.sleep(15)  # Attendi il caricamento e la scansione del QR

    base_url = "https://aiutotesi.altervista.org/blog/"
    php_file = "posts.php"  # File PHP esterno che contiene l'array dei post
    posts = extract_posts_from_php(php_file, base_url)
    print("Post estratti:", posts)

    # Itera sui post ed invia lo status per ciascuno
    for post in posts:
        image_path = post.get("image", "")
        # Costruisci il testo dello status: usa summary e aggiungi lo slug
        testo = post.get("summary", "") + " " + post.get("slug", "")
        print("Invio status per:", testo)
        invia_storia(driver, image_path, testo)
        time.sleep(10)  # Attendi 10 secondi tra uno status e l'altro

    driver.quit()
