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
        xp_send_status = "//button[@aria-label='Invia']"
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_send_status))
        )
        send_button.click()
        print("[OK] Status pubblicato correttamente.")
    except Exception as e:
        print("[ERRORE] Problemi nella pubblicazione dello status:", e)

list =posts = [
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_1_metodologie_didattiche.php",
        "title": "Metodologia didattiche",
        "subtitle": "Una panoramica sulle strategie didattiche innovative e tradizionali",
        "summary": "Scopri come le metodologie didattiche, da quelle tradizionali a quelle innovative, trasformano l'apprendimento.",
        "description": "Descrizione delle metodologie didattiche nella scuola italiana, dai modelli tradizionali alle strategie innovative.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_1_metodologie_didattiche.PNG"
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_2_Come_preparare_UDA_vincente.php",
        "title": "Come creare un UDA vincente",
        "subtitle": "Dalla scelta del tema alla definizione degli obiettivi",
        "summary": "Una guida pratica per realizzare Unità Didattiche efficaci e coinvolgenti.",
        "description": "Come realizzare Unità Didattiche efficaci e coerenti.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_2_Come_preparare_UDA_vincente.PNG"
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_3_Lezione_Simulata.php",
        "title": "Lezione simulata: suggerimenti pratici",
        "subtitle": "Tecniche e strumenti per una lezione coinvolgente",
        "summary": "Scopri come organizzare una lezione simulata di successo per migliorare l’apprendimento.",
        "description": "Suggerimenti e tecniche per una lezione simulata efficace.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_3_Lezione_Simulata.PNG"
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_4_compiti_autentici.php",
        "title": "Compiti autentici",
        "subtitle": "Esperienze di apprendimento reale",
        "summary": "Scopri come i compiti autentici stimolano la creatività e il problem solving degli studenti.",
        "description": "Il valore dei compiti autentici nell'apprendimento e nella valutazione.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_4_compiti_autentici.PNG"
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_5_clil.php",
        "title": "CLIL: apprendimento integrato di lingua e contenuti",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Scopri come rendere le tue lezioni più interattive e personalizzate grazie a piattaforme e risorse digitali.",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_5_clil.PNG",
        "content": " fj "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_6_didattica_digitale.php",
        "title": "Didattica digitale: risorse e strumenti online",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Questo metodo nasce dall’idea che la lingua si impari meglio quando viene utilizzata in situazioni autentiche: per esempio...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_6_didattica_digitale.PNG",
        "content": " tu "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_7_gestione_classe.php",
        "title": "Gestione della classe",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Definire poche regole chiare, costruite insieme alla classe. Quando gli studenti partecipano...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_7_gestione_classe.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_8_Competenze_chiave_nelle_UDA.php",
        "title": "Competenze chiave nelle UDA",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Adottare le competenze chiave come orizzonte educativo fa sì che la didattica non sia solo trasmissione...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_8_Competenze_chiave_nelle_UDA.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_9_Strategie_inclusive.php",
        "title": "Strategie inclusive per la lezione simulata",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Fornire contenuti multimediali (video, slide, podcast) da visionare a casa consente agli studenti con...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_9_Strategie_inclusive.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_10_Valutazione_autentica.php",
        "title": "Valutazione autentica nelle UDA",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "I compiti pratici, ancorati a contesti reali, stimolano la partecipazione attiva e la motivazione degli studenti...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_10_Valutazione_autentica.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_11_Peer_Teaching_Cooperative_Learning.php",
        "title": "Peer Teaching e Cooperative Learning",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Gli studenti imparano insegnando o spiegando ai compagni. Questo sistema valorizza...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_11_Peer_Teaching_Cooperative_Learning.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_12_Progettare_UDA_interdisciplinari.php",
        "title": "Progettare UDA interdisciplinari",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Analizzare un tema da prospettive diverse (storica, scientifica, letteraria, artistica) consente una comprensione più ampia...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_12_Progettare_UDA_interdisciplinari.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_13_Didattica_laboratoriale.php",
        "title": "Didattica laboratoriale",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Questo metodo può essere facilmente integrato nelle UDA (Unità Didattiche di Apprendimento) e nelle...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_13_Didattica_laboratoriale.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_14_UDL_e_inclusione.php",
        "title": "UDL e inclusione",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Il Universal Design for Learning (UDL) è un insieme di principi e linee guida che mirano a rendere la didattica accessibile a tutti...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_14_UDL_e_inclusione.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_15_Apprendimento_creativo_e_gamification.php",
        "title": "Apprendimento creativo e gamification",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "L’apprendimento creativo e la gamification (o ludicizzazione) si fondano sull’idea che...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_15_Apprendimento_creativo_e_gamification.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_16_Feedback_e_autovalutazione.php",
        "title": "Feedback e autovalutazione",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "Nel processo di apprendimento, il feedback e l’autovalutazione rivestono un ruolo chiave per guidare gli studenti a ...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_16_Feedback_e_autovalutazione.PNG",
        "content": " j "
    },
    {
        "slug": "https://aiutotesi.altervista.org/blog/blog_17_Interazione_scuola_famiglia.php",
        "title": "Interazione scuola-famiglia",
        "subtitle": "Strumenti e risorse online per innovare la didattica",
        "summary": "L’interazione tra scuola e famiglia rappresenta un elemento cruciale per promuovere il successo formativo e lo sviluppo...",
        "description": "I vantaggi di integrare strumenti online, piattaforme e metodologie digitali per potenziare l’insegnamento e l’apprendimento.",
        "image": "C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\blog_17_Interazione_scuola_famiglia.PNG",
        "content": " j "
    }
]










if __name__ == "__main__":
    # Assicurati di avere definito la funzione setup_driver() altrove
    driver = setup_driver(
        user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data",
        profile_directory="Profile 5"
    )
    
    # Apri WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    # Attendi per il caricamento della pagina e la scansione del QR se necessario
    time.sleep(15)
    
    # Esempio: pubblica status per i post dal numero 2 al 7 (indice 1 fino a 6)
    for post in posts[8:10]:
        # Recupera il percorso dell'immagine e il testo (description) dal post
        image_path = post["image"]
        # Aggiungiamo lo slug al testo in modo che l'URL sia visibile nello status
        text = post["description"]  + post["slug"]
        
        # Invia lo status con l'immagine e il testo
        invia_storia(driver, image_path, text)
        
        # Aspetta qualche secondo fra uno status e l'altro (modifica in base alle tue necessità)
        time.sleep(10)
    
    # Dopo aver completato tutte le operazioni:
    driver.quit()
