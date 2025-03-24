import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Importa WebDriverWait e expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura le opzioni di Chrome per usare un profilo già loggato
options = Options()
user_data_dir = r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data"
profile_directory = "Profile 5"
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Esempio di URL di un membro (modifica l'URL in base alle tue esigenze)
member_url = "https://www.facebook.com/groups/137462603725184/user/100006385361221"



def inserimento_testo(member_url):
    try:
        # Naviga alla pagina del membro
        driver.get(member_url)
        time.sleep(5)  # Attendi il caricamento della pagina

        print("Visito:", driver.current_url)

        # Aspetta fino a 10 secondi che il pulsante "Messaggio" sia cliccabile
        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Messaggio' and @role='button']"))
        )
        
        # Scrolla l'elemento in vista (opzionale se non è visibile)
        driver.execute_script("arguments[0].scrollIntoView(true);", message_button)
        time.sleep(1)
        
        # Clicca sul pulsante "Messaggio" per aprire il popup
        message_button.click()
        time.sleep(3)  # Attendi che il popup del messaggio venga caricato

        # Ora individua il campo di testo dove inserire il messaggio.
        # L'elemento ha role="textbox" ed è contenteditable="true"
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
        )
        
        # Clicca sul campo di testo per attivarlo, se necessario
        message_input.click()
        time.sleep(1)
        
        # Invia il testo del messaggio
        message_input.send_keys("Ciao, tanti auguri di buon compleanno!")
        try:
        # Attendi fino a 10 secondi che il pulsante di invio sia cliccabile
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Premi Invio per inviare' and @role='button']")
                )
            )
            
            # Scrolla il pulsante in vista (opzionale)
            driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
            time.sleep(1)
            
            # Clicca il pulsante per inviare il messaggio
            send_button.click()
            print("Messaggio inviato!")
            
        except Exception as e:
            print("Errore durante il click sul pulsante di invio:", e)
            
        print("Messaggio scritto correttamente nel campo di input.")

        # Se vuoi anche inviare il messaggio (ad esempio premendo INVIO)
        # message_input.send_keys(Keys.ENTER)  # Ricorda di importare Keys se necessario:
        # from selenium.webdriver.common.keys import Keys

    except Exception as e:
        print("Errore durante il click sul pulsante 'Messaggio' o l'invio del testo:", e)

    finally:
        # Attendi un po' per osservare il risultato e poi chiudi il driver
        time.sleep(10)
        driver.quit()






inserimento_testo(member_url)