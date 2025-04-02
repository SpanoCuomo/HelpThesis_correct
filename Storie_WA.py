


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

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
def invia_storia_(driver, file_path, testo=""):
    """
    Automatizza la creazione di uno status su WhatsApp Web:
    1. Clicca sul tab "Stato".
    2. Clicca sul pulsante per aggiungere un nuovo status.
    3. Carica l'immagine (o video) tramite l'input file.
    4. (Facoltativo) Inserisce un testo se fornito.
    5. Pubblica lo status.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

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

    # 2. Clicca sul pulsante per aggiungere un nuovo status
    try:
        aggiungi_stato = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus']"))
    )
        aggiungi_stato.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante Aggiungi status:", e)
        return

    # 3. Carica il file (immagine o video)
    try:
        foto_video_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Foto e video')]"))
        )
        foto_video_button.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare sul pulsante 'Foto e video':", e)
        return



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
        xp_input_file = "//input[@type='file' and contains(@accept,'image')]"
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
    # Assicurati di avere definito la funzione setup_driver() altrove
    php_file = "posts.php"  # File PHP esterno che contiene l'array dei post
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
    time.sleep(15)
    
    # Esempio: pubblica status per i post dal numero 2 al 7 (indice 1 fino a 6)
    for post in posts[0:]:
        # Recupera il percorso dell'immagine e il testo (description) dal post
        image_path = post["image"]
        # Aggiungiamo lo slug al testo in modo che l'URL sia visibile nello status
        text = post["summary"]  + post["slug"]
        
        # Invia lo status con l'immagine e il testo
        invia_storia(driver, image_path, text)
        
        # Aspetta qualche secondo fra uno status e l'altro (modifica in base alle tue necessità)
        time.sleep(10)
    
    # Dopo aver completato tutte le operazioni:
    driver.quit()