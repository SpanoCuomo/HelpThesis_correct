import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configura le opzioni di Chrome per usare un profilo già loggato
options = Options()
user_data_dir = r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data"
profile_directory = "Profile 5"
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    # Vai alla pagina dei membri del gruppo
    group_members_url = "https://www.facebook.com/groups/137462603725184/members"
    driver.get(group_members_url)
    
    # Attendi il caricamento iniziale della pagina
    time.sleep(5)
    
    # Imposta il numero minimo di membri desiderati e il numero massimo di scroll
    desired_count = 1000
    max_scrolls = 30
    scroll_count = 0
    
    # Salva l'altezza iniziale della pagina
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while scroll_count < max_scrolls:
        # Esegui lo scroll verso il fondo della pagina
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # attendi il caricamento dei nuovi elementi
        
        # Rileva l'altezza aggiornata della pagina
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Trova tutti i link dei membri (quelli che contengono "/groups/137462603725184/user/")
        member_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/137462603725184/user/')]")
        current_count = len(member_elements)
        print(f"Scroll {scroll_count}: trovati {current_count} membri, altezza pagina: {new_height}")
        
        # Se non cambia l'altezza, probabilmente non ci sono altri membri da caricare
        if new_height == last_height:
            print("Non sono stati caricati nuovi elementi; interrompo lo scroll.")
            break
        
        # Se abbiamo raggiunto il numero desiderato, esci dal ciclo
        if current_count >= desired_count:
            break
        
        last_height = new_height
        scroll_count += 1

    # Dopo lo scroll, rileggi tutti gli elementi dei membri
    member_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/groups/137462603725184/user/')]")
    print(f"\nTotale membri estratti: {len(member_elements)}\n")
    
    print("Membri del gruppo (Nome e ID):")
    for elem in member_elements:
        name = elem.text.strip()
        href = elem.get_attribute("href")
        match = re.search(r"/user/(\d+)/", href)
        if match:
            user_id = match.group(1)
            print(f"Nome: {name}, ID: {user_id}")
        else:
            print(f"Nome: {name}, ID non trovato in: {href}")

finally:
    driver.quit()
