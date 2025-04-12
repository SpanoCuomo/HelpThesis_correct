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



def invia_immagine_come_foto(driver, file_path):
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

def apri_whatsapp():
    global driver
    driver.get("https://web.whatsapp.com/")
    time.sleep(5)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='Cerca o avvia nuova chat']"))
        )
        if debug_mode == True:
            print("[DEBUG] WhatsApp Web caricato.")
    except:
        print("[WARN] Non trovo la barra di ricerca. Forse serve un altro selettore o più tempo.")










def open_whatsapp_and_click_chat_old(chat_title, messaggio):
    global driver

    # 1) Clic sul pulsante "Cerca o avvia nuova chat"
    xp_search_button = "//button[@aria-label='Cerca o avvia una nuova chat']"
    try:
        search_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xp_search_button))
        )
        search_btn.click()
        if debug_mode == True:
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
    # Pulisci se c'era altro testo
    real_input.send_keys(Keys.CONTROL, "a")
    real_input.send_keys(Keys.DELETE)
    real_input.send_keys(chat_title)
    time.sleep(2)

    # 3) Ora clicca la chat 
    xp_chat = f"//span[contains(@title, '{chat_title}')]"
    try:
        chat_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xp_chat))
        )
        chat_element.click()
        if debug_mode == True:
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
        if debug_mode == True:
            print("[DEBUG] Trovata casella messaggio, invio testo.")
    except TimeoutException:
        print("[WARN] Non posso scrivere in questa chat (solo admin). Skippo la chat.")
        return

    
    
    if debug_mode == True:
        print("[DEBUG] Trovata casella messaggio, invio testo.")

    # 5) Scrivi e invia
    msg_box.send_keys(messaggio)
    time.sleep(1)
 #   invia_immagine_come_foto(driver, r"C:\Users\UTENTE\Desktop\TFA_inserire 28 Ottobre 2024.mp4")
    invia_immagine_come_foto(driver, r"C:\Users\UTENTE\Downloads\Copertina_libro.PNG")
    
    xp_send_button = "//button[@aria-label='Invia']"
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_button))
        )
        send_button.click()
    except:
        msg_box.send_keys(Keys.ENTER)

    print("[OK] Messaggio inviato.")







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
    msg_box.send_keys(messaggio)
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







if __name__ == "__main__":
    start_time = time.time()  # Avvio cronometro (tic)
    # 1) Setup driver una sola volta
    setup_driver(
        user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data",
        profile_directory="Profile 2"
    )
    
    
    # 2) Apri WhatsApp
    apri_whatsapp()

    # 3) Ciclo su varie chat
    lista = ["Giovanna Di somma Vicina Casa Anna", "Famiglia bella"]
    listaUDA = [
    "CONCORSO DOCENTI PNRR 2 - Scambio di informazioni",
    "Grande Gruppo Iscritti 30 E 60 Cfu",
    "A09 30cfu e-campus",
    "A13 Ecampus art. 13",
    "30cfu Pegaso - A018",
    "Ecampus art. 13 IV ciclo",
    "Conc. A012/A022Lombardia",
    "A19 art13 ECampus III ciclo",
    "IV SOTTOCOMMISSIONE IC MARELLI",
    "FABRIANO 3 Commissione ADSS",
    "CONCORSO ADSS MARCHE - ABRUZZO - UMBRIA",
    "PNRR2-EEE/AAA- Reg. Lazio",
    "Orale A046 Basilicata ⚖️",
    "Adss Sec di sec Grado conc ter Lazio",
    "Concorso EEEE Talamona",
    "III SOTTOCOMMISSIONE EEEE",
    "Primaria Castellammare di Stabia 3° Circolo San Marco Evangelista",
    "EEEE VI SOTTOCOMMISSIONE",
    "Concorso primaria Lombardia",
    "ORALE EEEE CHIAVENNA-LOMBARDIA",
    "PRIMARIA V SOTTOCOMMISSIONE IC MORRICONE",
    "VIII SOTTOCOMMISSIONE - PRIMARIA COMUNE",
    "PRIMARIA ORALE II Comm. IC Valente LAZIO",
    "CONCORSO PNRR2 SARDEGNA • PROVA SCRITTA",
    "ORALE EEEE ICS MOLTENO LECCO",
    "ANCONA 2 commissione ADSS",
    "Reg LOMBARDIA Spunti/ aiuti per le tracce EEEE",
    "CIVITANOVA prima sottocommissione",
    "AAAA isiss Majorana S. Maria a Vico (ce)‼️",
    "PRIMARIA- Commissione VII I.C. Impastato -PRIMARIA",
    "Infanzia, via panisperna II Sottocommissione",
    "I sottocommissione infanzia orale (cristoforo colombo)",
    "Orale primaria IC 2 DAMIANI- MORBEGNO",
    "INFANZIA PALIANO",
    "Concorso 2024 primaria Lombardia",
    "Orale Primaria SPINI MORBEGNO",
    "ORALE CONCORSO EEEE ICS COMO LAGO",
    "Orale Grosotto - Primaria Lombardia",
    "Orale EEEE - Cadorna (Milano)",
    "PNRR2 A022 Concorso Sardegna",
    "PNRR2 Lombardia Secondaria primo e secondo grado",
    "Concorso PNRR2 Piemonte",
    "A017-A01 e-campus IV edizione",
    "⚖️Didattica del Diritto⚖️ - Ecampus 30cfu",
    "30-60 iscritti a eCampus percorsi abilitanti GRUPPO PRINCIPALE",
    "Concorso docenti PNRR 2 2025 Info/confronto/supporto",
    "Sottocommissione 1 - I.C. de filippo PRIMARIA EEEE",
    "II Sottocommissione KING EEEE",
    "IC ORZINUOVI CONCORSO PRIMARIA",
    "G.Romanino Brescia",
    "IC Castelcovati",
    "CALCINATO BS Primaria",
    "PNRR2 Lombardia Secondaria primo e secondo grado",
    "Mini Call Sicilia Lombardia ADMM",
    "Mini Call veloce ADMM Emilia Romagna",
    "PNNR2 CAMPANIA A012/A022",
    "AAAA De Amicis",
    "IC A. TIRABOSCHI, PALADINA (BG)",
    ]
    
    
    Mex_Luca = "Piacere, sono Luca. Io ed il mio team offriamo servizio per la preparazione della lezione simulata e per l'UDA in tutte le parti e per tutte le classi di concorso, dalla consenga della traccia alla preparazione delle slides, ogni aspetto viene trattato, per dare la possibilità di prepararvi al meglio. Chi fosse interessato può contattarci al 378 060 8777. Grazie e buon lavoro a tutti. Team Help Tesi."
    
    Mex_Luca_pacato = "Per chi fosse interessato, qui ci sono articoli che possono essere utili per la preparazione al concorso. https://aiutotesi.altervista.org/blog/blog_UDA_lista.php. Inoltre io ed il mio team diamo una mano nella preparazione. Chi fosse interessato può contattarci al 378 060 8777. Grazie e buon lavoro a tutti."
    
    Mex_per_entrata_gruppo = "Questo è un altro gruppo dove si parla del concorso <br> https://chat.whatsapp.com/KL0jAgGqz3vIUbcKLdWxtE"
    Mex_Giovanna = "Preparati al meglio per il tuo esame orale del concorso docente con Help Thesis! \n\n     Offriamo supporto personalizzato per UDA e lezioni simulate per tutte le classi di concorso. \n\nPrenota subito il tuo posto: contattaci al 378 06 08 777 o scrivi a aiuto.tesi.official@gmail.com. Non perdere l’occasione di arrivare pronto e sicuro!"
    
    mex_libro_pubblicit = "Ti stai preparando per il concorso? Abbiamo scritto un libro che può esserti utile. Un'anteprima gratuita è disponibile in messaggio o sul sito https://aiutotesi.altervista.org/uda.html. Inoltre possiamo aiutarti per la prova orale. Contattaci al 378 060 8777."
    
    
    i = 0
    #immagine_indirizzo = r"C:\Users\UTENTE\Downloads\Copertina_libro.PNG"
    immagine_indirizzo = r"C:\Users\lspan\Desktop\ImmaginiSitoTesi\cliccabile.pdf"
    for el in listaUDA:
        i = i + 1
        print("\n\nStampo sulla pagina" + str(el))
        print("elemento "+ str(i) + "/" +str(len(listaUDA)))
        
        open_whatsapp_and_click_chat(el, Mex_Giovanna, immagine_indirizzo)
        
        
        time.sleep(3)  # Attendi qualche secondo tra un invio e l'altro

    # Se vuoi, alla fine, NON chiudi il browser
    # driver.quit()

    end_time = time.time()  # Arresto cronometro (toc)

    # Calcola e stampa differenza (in secondi)
    elapsed = end_time - start_time
    print(f"\n\nTempo totale di esecuzione dello script: {elapsed:.2f} secondi.")
    
    
    