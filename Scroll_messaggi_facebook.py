import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Import necessari per i wait ed eccezioni
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurazione delle opzioni di Chrome per usare un profilo già loggato
options = Options()
user_data_dir = r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data"
profile_directory = "Profile 5"
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

import time
import random

# Genera un numero casuale float tra 5 e 10 (es. 7.43 secondi)
def num_casual():
    attesa = random.uniform(5, 10)
    print(f"Attendo {attesa:.2f} secondi...")
    return  time.sleep(attesa)





def inserimento_testo(member_url):
    try:
        # Naviga alla pagina del membro
        driver.get(member_url)
        num_casual()  # Attendi il caricamento della pagina
        print("\n\nVisito:", driver.current_url)
        
        # Prova a individuare il pulsante "Messaggio"
        try:
            message_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Messaggio' and @role='button']"))
            )
        except TimeoutException:
            print("\n\nIl pulsante 'Messaggio' non è disponibile per questo utente. Saltando...")
            return  # Esce dalla funzione se l'utente non è contattabile
        
        # Scrolla il pulsante in vista e cliccaci sopra per aprire il popup del messaggio
        driver.execute_script("arguments[0].scrollIntoView(true);", message_button)
        num_casual()
        message_button.click()
        num_casual()  # Attendi il caricamento del popup

        # Individua il campo di input (contenteditable) per il messaggio
        try:
            message_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
            )
        except TimeoutException:
            print("\n\nIl campo di testo per il messaggio non è stato trovato. Saltando...")
            return
        
        # Clicca sul campo e invia il messaggio
        message_input.click()
        num_casual()
        message_input.send_keys("Buonasera")
        print("Messaggio scritto correttamente nel campo di input.")

        # Individua il pulsante di invio e cliccaci sopra
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Premi Invio per inviare' and @role='button']")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
            num_casual()
            send_button.click()
            print("Messaggio inviato!")
        except Exception as e:
            print("Errore durante il click sul pulsante di invio:", e)

    except Exception as e:
        print("Errore durante il contatto dell'utente:", e)












try:
    # Vai alla pagina dei membri del gruppo
    group_members_url = "https://www.facebook.com/groups/137462603725184/members"
    #group_members_url = "https://www.facebook.com/groups/531999858522473/members"
    
    driver.get(group_members_url)
    num_casual()  # Attendi il caricamento iniziale

    # Individua il contenitore in cui vengono caricati i membri
    # (qui si utilizza il selettore che hai menzionato)
    container = driver.find_element(By.CSS_SELECTOR, "div.x78zum5.xdt5ytf.x1iyjqo2")

    # Scrolla la pagina per caricare un numero sufficiente di membri
    desired_count = 20  # Numero minimo di membri da caricare
    max_scrolls = 20
    scroll_count = 0

    while scroll_count < max_scrolls:
        member_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/137462603725184/user/')]")
        current_count = len(member_elements)
        print(f"Scroll {scroll_count}: trovati {current_count} membri")
        if current_count >= desired_count:
            break
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", container)
        num_casual()
        scroll_count += 1

    member_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/137462603725184/user/')]")
    print(f"\nTotale membri estratti: {len(member_elements)}\n")

    # Estrai gli URL dei membri (evitando duplicati)
    member_urls = []
    for elem in member_elements:
        href = elem.get_attribute("href")
        if href not in member_urls:
            member_urls.append(href)
    
    print("\nNavigazione alle pagine dei membri:")
    for url in member_urls:
        num_casual()  # Attendi che la pagina del membro si carichi
        inserimento_testo(url)
        num_casual()
        # Torna alla pagina dei membri prima di passare al successivo
        driver.get(group_members_url)
        

    print("Operazione completata.")

finally:
    driver.quit()
