from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException 
import subprocess
import pyperclip  # <--- nuova libreria da installare con pip install pyperclip



RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RESET  = "\033[0m"

# Per scaricare immagine da server e poi inserirla
import os
import tempfile
import requests
from urllib.parse import urlparse

CLICK_TIMEOUT = 10
LOAD_TIMEOUT  = 10

driver = None
debug_mode = False
def invia_immagine_come_foto_old(driver, file_path):
    """
    1) Clicca il pulsante 'Allega' (icona plus, aria-label='Allega').
    2) Clicca 'Foto e video' anziché 'Documento'.
    3) Trova l'input file con accept='image/*,video/*' e fa send_keys(file_path).
    4) Clicca il bottone 'Invia' se appare la preview.
    """
   
    # 1) Clic pulsante Allega
    xp_allega_btn = "//button[@aria-label='Allega' or @title='Allega']"
    try:
        allega_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_allega_btn))
        )
        allega_btn.click()
        if debug_mode == True:
            print("[DEBUG] Cliccato pulsante Allega (icona plus).")
        time.sleep(1)
    except Exception as e:
        print("[ERRORE] Non trovo o non riesco a cliccare il pulsante Allega:", e)
        return

    # 2) Clicca su 'Foto e video'
    xp_foto_option = "//div[@aria-label='Foto e video']"  
    # oppure: "//div[contains(@aria-label,'Foto')]" se la lingua cambia
    # In inglese potrebbe essere: "//div[@aria-label='Photos & Videos']"
    try:
        foto_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xp_foto_option))
        )
        foto_option.click()
        if debug_mode == True:
            print("[DEBUG] Cliccato voce 'Foto e video' nel menù.")
        time.sleep(1)
    except Exception as ex:
        print("[WARN] Non trovo l’opzione 'Foto e video' (controlla lingua/HTML). Procedo ugualmente...")

    # 3) Ora cerchiamo l'input file con accept='image'
    xp_input_file = "//input[@type='file' and contains(@accept,'image')]"
    try:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xp_input_file))
        )
        # 4) Inviamo il file
        file_input.send_keys(file_path)
        if debug_mode == True:
            print("[OK] Ho caricato l’immagine come foto:", file_path)
    except Exception as exc:
        print("[ERRORE] Non trovo o non riesco a usare l'input file per foto/video:", exc)
        return

    # 5) Se appare l’anteprima con un pulsante 'Invia' (aria-label='Invia'), clicchiamolo
    xp_invia = "//div[@role='button' and @aria-label='Invia']"
    try:
        invia_foto_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xp_invia))
        )
        invia_foto_btn.click()
        if debug_mode == True:
            print("[DEBUG] Cliccato 'Invia' nella preview foto.")
    except:
        print("[INFO] Non ho trovato un pop-up di anteprima o invio (forse WhatsApp invia subito).")
    if debug_mode == True:
        print("[FINE] Immagine inviata come foto/video (con anteprima).")


def kill_all_chrome():
    """
    Termina forzatamente tutti i processi chrome.exe e chromedriver.exe su Windows.
    """
    for proc in ("chrome.exe", "chromedriver.exe"):
        subprocess.call(
            ["taskkill", "/F", "/IM", proc, "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    pass

def debug_print(msg):
    """Stampa un messaggio solo se DEBUG_MODE è True."""
    if debug_mode:
        print(msg)

def invia_immagine_come_foto(driver, file_path):
    """
    Invia un file immagine (o video) come "Foto e video" su WhatsApp Web.
    Passi:
      1) Clic pulsante Allega (icona plus).
      2) Clic su 'Foto e video' (se disponibile).
      3) Trova input file con accept='image' e invia il file.
      4) Clicca il pulsante 'Invia' se compare la preview.
    """
    # 1) Clic sul pulsante Allega
    xp_allega_btn = "//button[@aria-label='Allega' or @title='Allega']"
    try:
        allega_btn = WebDriverWait(driver, CLICK_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, xp_allega_btn))
        )
        allega_btn.click()
        debug_print("[DEBUG] Cliccato pulsante Allega (icona plus).")
        time.sleep(1)
    except TimeoutException as e:
        print(f"[ERRORE] Non trovo/clicco il pulsante Allega (xpath: {xp_allega_btn}): {e}")
        return
    except Exception as e:
        print("[ERRORE] Errore generico cliccando pulsante Allega:", e)
        return

    # 2) Clic su 'Foto e video' (in base alla lingua, potremmo cercare altre label)
    #    Se non lo troviamo, proseguiamo comunque, perché a volte appare in automatico l'input.
    xp_foto_options = [
        "//div[@aria-label='Foto e video']",
        "//div[@aria-label='Photos & Videos']",
        "//div[contains(@aria-label, 'Foto')]"   # fallback
    ]
    clicked_foto_option = False
    for xp_foto_option in xp_foto_options:
        try:
            foto_option = WebDriverWait(driver, LOAD_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xp_foto_option))
            )
            foto_option.click()
            debug_print(f"[DEBUG] Cliccato voce 'Foto e video' con xpath: {xp_foto_option}")
            time.sleep(1)
            clicked_foto_option = True
            break
        except TimeoutException:
            pass  # Proveremo il prossimo selettore
        except Exception as ex:
            print(f"[WARN] Errore cliccando 'Foto e video' con xpath {xp_foto_option}: {ex}")

    if not clicked_foto_option:
        debug_print("[WARN] Nessun pulsante 'Foto e video' trovato. Procedo con l'input file se presente...")

    # 3) Cerca l'input file con accept='image' (eventualmente anche 'video')
    xp_input_file = (
        "//input[@type='file' "
        "and (contains(@accept,'image') or contains(@accept,'video'))]"
    )
    try:
        file_input = WebDriverWait(driver, CLICK_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, xp_input_file))
        )
        file_input.send_keys(file_path)
        debug_print(f"[OK] Ho caricato il file (foto/video): {file_path}")
    except TimeoutException:
        print(f"[ERRORE] Non trovo l'input file (xpath: {xp_input_file}).")
        return
    except Exception as exc:
        print("[ERRORE] Problema nell'usare l'input file per foto/video:", exc)
        return

    # 4) Proviamo a cliccare il pulsante 'Invia' nella preview (se appare)
    xp_invia = "//div[@role='button' and @aria-label='Invia']"
    try:
        invia_foto_btn = WebDriverWait(driver, LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, xp_invia))
        )
        invia_foto_btn.click()
        debug_print("[DEBUG] Cliccato 'Invia' nella preview foto/video.")
    except TimeoutException:
        # A volte l'immagine si invia subito senza preview. Non è un errore.
        debug_print("[INFO] Nessun pop-up di anteprima (invio automatico).")
    except Exception as e:
        print("[ERRORE] Errore cliccando sul pulsante 'Invia' preview:", e)
    
    debug_print("[FINE] Immagine inviata come foto/video (con eventuale anteprima).")


def setup_driver(user_data_dir, profile_directory):
    global driver
    kill_all_chrome()
    time.sleep(2)

    chrome_options = Options()
    # Metti la TUA cartella personalizzata

    #chrome_options.add_argument("--start-minimized")
    
    #driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    # E questa:
    #driver.minimize_window()
    return driver

def apri_whatsapp():
    global driver
    driver.get("https://web.whatsapp.com/")
    time.sleep(45)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='Cerca o avvia nuova chat']"))
        )
        if debug_mode == True:
            print("[DEBUG] WhatsApp Web caricato.")
    except:
        print("[WARN] Non trovo la barra di ricerca. Forse serve un altro selettore o più tempo.")











def prepare_image_path(img_addr):
    # se è un URL, lo scarico e lo salvo su una cartella temporanea locale (stessa cosa da fare per gli altri programmi, sennò sono costretto ad avere tutto in locale. Meglio fare così.
        if img_addr.startswith("http://") or img_addr.startswith("https://"):
            resp = requests.get(img_addr)
            resp.raise_for_status()
            # estraggo estensione dal path dell'URL
            ext = os.path.splitext(urlparse(img_addr).path)[1] or ".png"
            tmp_file = os.path.join(tempfile.gettempdir(), f"temp_image{ext}")
            with open(tmp_file, "wb") as f:
                f.write(resp.content)
            return tmp_file
        # altrimenti lo considero già un percorso locale
        return img_addr




def open_whatsapp_and_click_chat(chat_title, messaggio, immagine_path):
    global driver

    # 1) Clic sul pulsante "Cerca o avvia nuova chat"
    xp_search_button = "//button[@aria-label='Cerca o avvia una nuova chat']"
    try:
        search_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xp_search_button))
        )
        search_btn.click()
        if debug_mode:
            print("[DEBUG] Cliccato il bottone di ricerca.")
        time.sleep(1)
    except:
        print("[WARN] Non trovo/Non clicco il pulsante di ricerca. Forse è già aperta la barra.")

    # 2) Trova il vero campo (div contenteditable) per digitare
    xp_real_input = "//div[@role='textbox' and @contenteditable='true' and @data-lexical-editor='true']"
    real_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xp_real_input))
    )
    real_input.click()
    real_input.send_keys(Keys.CONTROL, "a")
    real_input.send_keys(Keys.DELETE)
    real_input.send_keys(chat_title)
    time.sleep(2)

    # 3) Clicca sulla chat
    xp_chat = f"//span[contains(@title, '{chat_title}')]"
    try:
        chat_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xp_chat))
        )
        chat_element.click()
        if debug_mode:
            print(f"[OK] Cliccato sulla chat: {chat_title}")
    except:
        print(f"[ERRORE] Non trovo la chat '{chat_title}'.")
        return

    time.sleep(2)

    # 4) Casella messaggio
    xp_input_msg = ("//div[@contenteditable='true' and @role='textbox' "
                    "and contains(@aria-placeholder,'Scrivi un messaggio')]")

    try:
        msg_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xp_input_msg))
        )
        if debug_mode:
            print("[DEBUG] Trovata casella messaggio, invio testo.")
    except TimeoutException:
        print("[WARN] Non posso scrivere in questa chat (solo admin). Skippo la chat.")
        return

    if debug_mode:
        print("[DEBUG] Trovata casella messaggio, invio testo.")

    # 5) Scrivi il messaggio
    #msg_box.send_keys(messaggio)
    pyperclip.copy(messaggio)  # copia il messaggio nella clipboard
    msg_box.click()  # clic per essere certi che la casella sia attiva
    time.sleep(0.5)
    msg_box.send_keys(Keys.CONTROL, 'v')  # incolla il messaggio
    time.sleep(1)
    

    # 6) Invia immagine passata come parametro
    invia_immagine_come_foto(driver, immagine_path)

    # 7) Invio definitivo del messaggio
    xp_send_button = "//button[@aria-label='Invia']"
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_button))
        )
        send_button.click()
    except:
        msg_box.send_keys(Keys.ENTER)

    print("[OK] Messaggio inviato.")








# if __name__ == "__main__":
#     kill_all_chrome()
#     start_time = time.time()  # Avvio cronometro (tic)
#     # 1) Setup driver una sola volta
    
#     if pc_grande:
#         user_data_dir = r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile"
#         profile_directory = "Default"
#         stampa_colore(f"✅ Sono nel PC grande", "verde")
#     else:
#         user_data_dir = r"C:\Users\lspan\Desktop\Chrome_Selenium_Profile"
#         profile_directory = "Default"
#         stampa_colore(f"✅ Sono nel PC piccolo", "verde")

    
    
#     # 2) Apri WhatsApp
#     apri_whatsapp()

    

        

    
    
    
    
#     i = 0
#     #immagine_indirizzo = r"C:\Users\UTENTE\Downloads\Copertina_libro.PNG"
#     immagine_indirizzo = r"C:\Users\lspan\Desktop\ImmaginiSitoTesi\cliccabile.pdf"
#     listadausare = lista
#     for el in listadausare:
#         i = i + 1
#         print("\n\nStampo sulla pagina" + str(el))
#         print("elemento "+ str(i) + "/" +str(len(listadausare)))
        
#         open_whatsapp_and_click_chat(el, Mex_Giovanna, immagine_indirizzo)
        
        
#         time.sleep(3)  # Attendi qualche secondo tra un invio e l'altro

#     # Stampa report
#     print("\nGruppi in cui l'invio è riuscito:")
#     for grp in succeeded:
#         print(" -", grp)

#     print("\nGruppi in cui l'invio è FALLITO:")
#     for grp in failed:
#         print(" -", grp)






def post_a_whatsapp(pc_grande: bool = True, debug: bool = False):
    """
    Esegue un broadcast su WhatsApp Web usando il profilo 'PC grande' o 'PC piccolo'.
    Lista chat, messaggio e percorso immagine sono definite internamente.
    """
    # 1) Lista delle chat
    chats = [
        "Giovanna Di somma Vicina Casa Anna",
        "Famiglia bella",
        # aggiungi qui le altre chat…
    ]

    # 2) Messaggio da inviare
    message = (
        "Preparati al meglio per il tuo esame orale del concorso docente con Help Thesis!\n\n"
        "Offriamo supporto personalizzato per UDA e lezioni simulate per tutte le classi di concorso.\n\n"
        "Prenota subito il tuo posto: contattaci al 3780608777 o scrivi a aiuto.tesi.official@gmail.com."
    )

    # 3) Percorso del file da allegare
    image_path = r"C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\cliccabile.pdf"

    # 4) Avvia Chrome con il profilo giusto
    kill_all_chrome()
    if pc_grande:
        user_data_dir = r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
    else:
        user_data_dir = r"C:\Users\lspan\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
    setup_driver(user_data_dir, profile_directory)

    # 5) Apri WhatsApp Web e invia a ciascuna chat
    apri_whatsapp()
    for chat in chats:
        open_whatsapp_and_click_chat(chat, message, image_path)
        time.sleep(3)