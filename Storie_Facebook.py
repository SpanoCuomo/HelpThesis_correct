from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# ----------------------------------------------------------------
# FUNZIONE PER CREARE IL DRIVER
# ----------------------------------------------------------------
def setup_driver(user_data_dir, profile_directory):
    """
    Crea (o riusa) un'istanza di Chrome, utilizzando un profilo già loggato.
    """
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# ----------------------------------------------------------------
# FUNZIONE PER INVIARE UNA STORIA SU FACEBOOK
# ----------------------------------------------------------------
def invia_storia_facebook(driver, file_path, testo=""):
    """
    Automatizza la creazione di una storia su Facebook con pulsante link:
      1) Clicca sul link /stories/create/
      2) Clicca su "Crea una storia con foto"
      3) Carica il file (immagine o video)
      4) Clicca su "Aggiungi pulsante" e poi su "Pulsanti Link web"
      5) Inserisce il link (es. www.aiutotesi.altervista.org) e conferma
      6) (Opzionale) Inserisce del testo nel campo contenteditable
      7) Clicca su "Condividi nella storia"
    NOTA: Gli XPATH e i testi vanno adattati se Facebook cambia l'interfaccia o la lingua.
    """
    # 1. Clicca sul link /stories/create/
    try:
        create_story_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/stories/create/')]"))
        )
        create_story_link.click()
        time.sleep(2)
    except Exception as e:
        print("[ERRORE] Non riesco ad aprire la sezione Storie (link /stories/create/):", e)
        return
    
    # 2. Clicca su "Crea una storia con foto"
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

    # 4. Aggiungi il pulsante link
    try:
        # Clicca sul bottone "Aggiungi pulsante"
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
        link_input.send_keys("www.aiutotesi.altervista.org")
        time.sleep(1)
        # Clicca sul pulsante di conferma, ad esempio "Fatto"
        confirm_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Fatto')]"))
        )
        confirm_btn.click()
        time.sleep(1)
    except Exception as e:
        print("[WARN] Non sono riuscito ad aggiungere il pulsante link:", e)

    # 5. (Opzionale) Inserisci testo nel campo contenteditable
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
        print("[OK] Storia pubblicata correttamente su Facebook con pulsante link.")
        time.sleep(5)
    except Exception as e:
        print("[ERRORE] Non riesco a cliccare 'Condividi nella storia':", e)

# ----------------------------------------------------------------
# FUNZIONE PER CREARE UN REEL SU FACEBOOK
# ----------------------------------------------------------------
def crea_reel_facebook(driver, video_path, didascalia=""):
    """
    Automatizza la creazione di un Reel su Facebook:
      1) Naviga alla pagina di creazione Reel
      2) Carica il video (o slideshow convertito in video)
      3) (Opzionale) Inserisce la didascalia
      4) Clicca su "Condividi reel"
    NOTA: Gli XPATH vanno adattati in base all'interfaccia e alla lingua.
    """
    try:
        driver.get("https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS")
        time.sleep(5)
    except Exception as e:
        print("[ERRORE] Non riesco a navigare su Reels:", e)
        return

    # Carica il video
    try:
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(video_path)
        time.sleep(5)
    except Exception as e:
        print("[ERRORE] Non riesco a caricare il video:", e)
        return

    # Inserisci didascalia, se prevista (modifica il placeholder se necessario)
    if didascalia:
        try:
            caption_area = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[@placeholder='Scrivi una didascalia']"))
            )
            caption_area.click()
            caption_area.send_keys(didascalia)
            time.sleep(1)
        except Exception as e:
            print("[WARN] Non riesco a inserire la didascalia:", e)

    # Clicca su "Condividi reel"
    try:
        share_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Condividi reel')]"))
        )
        share_button.click()
        print("[OK] Reel pubblicato correttamente.")
        time.sleep(5)
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione del reel:", e)

# ----------------------------------------------------------------
# ESEMPIO DI CODICE CHE CHIAMA LE FUNZIONI
# ----------------------------------------------------------------
if __name__ == "__main__":
    # 1. Imposta il driver con un profilo di Chrome già loggato a Facebook
    driver = setup_driver(
        user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data",
        profile_directory="Profile 2"
    )
    
    # 2. Vai su Facebook
    driver.get("https://www.facebook.com/")
    time.sleep(10)  # Attendi il caricamento della home

    # 3. Esempio: crea una Storia con pulsante link
    posts = [
        {
            "slug": "https://aiutotesi.altervista.org/blog/blog_1_metodologie_didattiche.php",
            "summary": "Scopri le metodologie didattiche innovative.",
            "image": r"C:\Users\lspan\Desktop\ImmaginiSitoTesi\blog_1_metodologie_didattiche.PNG"
        }
        # Puoi aggiungere altri post qui...
    ]
    
    for post in posts:
        image_path = post["image"]
        text = post["summary"] + " " + post["slug"]
        invia_storia_facebook(driver, image_path, text)
        time.sleep(10)
    
    # 4. Esempio: crea un Reel (assicurati che il video sia verticale o adatto al formato)
    video_path = r"C:\Users\lspan\Desktop\VideoReel\reel_video.mp4"
    crea_reel_facebook(driver, video_path, didascalia="Il mio nuovo Reel!")
    
    # 5. Chiudi il browser
    driver.quit()
