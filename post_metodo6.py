import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
from selenium.webdriver.chrome.options import Options


def post_from_page_to_another_page(
    page_name,
    target_page_url,
    message,
    post_as_page=True,
    image_path=None,   # se vogliamo caricare un’immagine o un video
):
    """Funzione che prova a postare su una determinata pagina/profilo/URL,
    con possibilità di caricare un’immagine o un video."""
    verbose = False
    try:
        

        # Screenshot di debug
        save_screenshot(driver, "0_home_facebook.png")

        # Se voglio postare come Pagina, provo a "switchare contesto"
        if post_as_page:
            if verbose == True:
                print("[DEBUG] Provo a switchare contesto a Pagina:", page_name)
            try:
                css_sel = "div[aria-label='Il tuo profilo']"
                if verbose == True:
                    print(f"[DEBUG] Cerco profile_menu con CSS: {css_sel}")
                profile_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_sel))
                )
                _scroll_into_view_and_click(driver, profile_menu, "profile_menu")
                time.sleep(2)

                xp_page = f"//span[text()='{page_name}']"
                if verbose == True:
                    print(f"[DEBUG] Cerco page_option con XPATH: {xp_page}")
                page_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xp_page))
                )
                _scroll_into_view_and_click(driver, page_option, "page_option")
                time.sleep(5)
                if verbose == True:
                    print("[DEBUG] Switchato al contesto Pagina:", page_name)

            except Exception as e:
                print("[WARN] Non sono riuscito a switchare a Pagina (forse non serve o selettore errato).")
                print("Dettagli errore switch:", e)
        if verbose == True:
            print(f"[DEBUG] Ora vado su: {target_page_url}")
        driver.get(target_page_url)
        time.sleep(5)
        save_screenshot(driver, "1_target_page.png")

        # 1) Clic sul box "Scrivi qualcosa..." / "Crea un post..." ecc.
        possibili_testi = [
            "Scrivi qualcosa",
            "Crea un post",
            "Scrivi un post pubblico",
            "Crea un post pubblico",
            "Scrivi qualcosa a",
        ]
        box_trovato = False
        for testo in possibili_testi:
            xp_box = f"//span[contains(text(), '{testo}')]/ancestor::div[@role='button']"
            if verbose == True:
                print(f"[DEBUG] Cerco XPATH: {xp_box}")
            try:
                create_post_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp_box))
                )
                _scroll_into_view_and_click(driver, create_post_box, "create_post_box")
                if verbose == True:
                    print(f"[OK] Trovato e cliccato box: '{testo}'")
                box_trovato = True
                time.sleep(2)
                save_screenshot(driver, f"2_clicked_box_{testo}.png")
                break
            except TimeoutException:
                print(f"[DEBUG] Timeout: non trovo pulsante box con testo '{testo}'")
            except Exception as ex:
                print(f"[DEBUG] Altra eccezione su box '{testo}':", ex)

        if not box_trovato:
            print("[ERRORE] Non trovo nessun pulsante per creare un post!")
            return

        # 2) Attendiamo (facoltativo) la comparsa del dialog 'Crea post'
        try:
            xp_dialog = "//div[@role='dialog' and .//span[contains(text(),'Crea post')]]"
            if verbose == True:
                print("[DEBUG] Aspetto dialog 'Crea post' con XPATH:", xp_dialog)
            create_post_dialog = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xp_dialog))
            )
            if verbose == True:
                print("[OK] Dialog 'Crea post' visibile.")
        except TimeoutException:
            print("[WARN] Non appare un overlay 'Crea post', continuo lo stesso...")

        # 3) Inseriamo il testo nel field contenteditable
        possibili_editor = [
            "//div[@contenteditable='true' and contains(@aria-label,'Scrivi qualcosa')]",
            "//div[@contenteditable='true' and contains(@aria-label,'Crea un post')]",
            "//div[@contenteditable='true' and contains(@aria-label,'Scrivi qualcosa a')]",
            "//div[@contenteditable='true' and contains(@aria-placeholder,'Scrivi qualcosa')]",
        ]
        editor_inserito = False
        for xp_ed in possibili_editor:
            if verbose == True:
                print("[DEBUG] Cerco editor con XPATH:", xp_ed)
            try:
                editor = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp_ed))
                )
                _scroll_into_view(driver, editor)
                if verbose == True:
                    print("[DEBUG] Editor trovato, inserisco il messaggio.")
                editor.send_keys(message)
                if verbose == True:
                    print("[OK] Inserito il testo del post.")
                editor_inserito = True
                time.sleep(1)
                save_screenshot(driver, "3_editor_inserito.png")
                break
            except TimeoutException:
                print(f"[DEBUG] Non trovo l'editor con XPATH: {xp_ed}")
            except Exception as ex:
                print(f"[DEBUG] Altra eccezione su xp_ed={xp_ed} =>", ex)

        if not editor_inserito:
            print("[ERRORE] Non trovo un campo di input con 'Scrivi qualcosa' QUI.")
        else:
            print("[DEBUG] Testo del post inserito correttamente.")

        # 4) Se voglio aggiungere un file (foto/video)
        if image_path:
            print(f"[DEBUG] Provo a caricare un file: {image_path}")
            click_photo_video_and_upload(driver, image_path)

        # 5) Clic sul pulsante "Pubblica"
        xp_publish = (
            "//div[@role='button' and @aria-label='Pubblica' and not(@aria-disabled='true')]"
        )
        if verbose == True:
            print("[DEBUG] Cerco pulsante 'Pubblica' con XPATH:", xp_publish)
        try:
            publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xp_publish))
            )
            _scroll_into_view_and_click(driver, publish_button, "publish_button")
            if verbose == True:
                print("[OK] Cliccato 'Pubblica'.")
            time.sleep(5)
            save_screenshot(driver, "4_post_published.png")
        except TimeoutException:
            print("[ERRORE] Non trovo il pulsante 'Pubblica' abilitato.")
            # In alcuni layout potrebbe comparire con aria-disabled="false"

        print("[FINE] Post pubblicato (se la pagina lo consente).")

    except Exception as e:
        print("[EXCEPTION GENERALE]", e)
    finally:
        # es. screenshot finale di debug
        save_screenshot(driver, "z_final.png")
        



def click_photo_video_and_upload(driver, image_path):
    """
    1) Clic sul pulsante esterno "Foto/video".
    2) Clic sul pulsante interno "Aggiungi foto/video" (se serve).
    3) Trova <input type='file' accept='image'...> e fai send_keys(file_path).
    """
    verbose = False
    try:
        # Clic su 'Foto/video' (o 'Aggiungi foto/video')
        # In questo snippet, esattamente come nel codice “funzionante”:
        xp_photo_btn = "//div[@aria-label='Foto/video' or @aria-label='Aggiungi foto/video']"
        photo_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xp_photo_btn))
        )
        photo_button.click()
        if verbose == True:
            print("[DEBUG] Click pulsante 'Foto/video'.")
        time.sleep(2)

        # Poi trova input[type=file]
        inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        if verbose == True:
            print("[DEBUG] Trovati", len(inputs), "input file.")
        # Prova col primo o col secondo, a seconda dell'ordine
        # Spesso il [0] è quello giusto, ma a volte serve [1].
        if len(inputs) > 1:
            file_input = inputs[-1]  # prendi l'ultimo
        else:
            file_input = inputs[0]

        file_input.send_keys(image_path)
        print("[OK] Inviato il file:", image_path)
        time.sleep(5)

    except Exception as ex:
        print("[ERRORE] Fallito caricamento immagine:", ex)


def _scroll_into_view(driver, element):
    """ Scrolla l’elemento in vista, senza cliccare. """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

def _scroll_into_view_and_click(driver, element, debug_name="unknown"):
    """ Scrolla l’elemento in vista e poi clicca, con log di debug. """
    verbose = False
    if verbose == True:
        print(f"[DEBUG] _scroll_into_view_and_click su: {debug_name}")
    _scroll_into_view(driver, element)
    try:
        element.click()
    except ElementClickInterceptedException as e:
        
        print("[DEBUG] ElementClickInterceptedException su:", debug_name, " => retry dopo 1s")
        time.sleep(1)
        _scroll_into_view(driver, element)
        element.click()
    except Exception as ex:
        print("[DEBUG] Eccezione generica su click di", debug_name, ":", ex)

def save_screenshot(driver, filename_prefix):
    """ Salva screenshot con timestamp, per debug. """
    pass


# ESEMPIO DI ESECUZIONE
if __name__ == "__main__":
    
    start_time = time.time()  # Avvio cronometro (tic)
    user_data_dir=r"C:\Users\UTENTE\AppData\Local\Google\Chrome\User Data"
    profile_directory="Profile 5"
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.facebook.com/")
    time.sleep(5)
    
    
    print("[DEBUG] Avvio browser con user_data_dir:", user_data_dir)
    print("[DEBUG] Avvio browser con profile_directory:", profile_directory)
    
    
    ### Gruppi che non so cosa siano
    #https://www.facebook.com/groups/2941802416087165/
    
    
    
    #di seguito, inserisco le pagine FB da cui posso postare da pagina (HelpThesis)
    # Chiaramente, sono quelle per UDA 
    target_page_url_list_FB_UDA_da_pagina = [
    #"https://www.facebook.com/groups/137462603725184/",     
    "https://www.facebook.com/groups/810412816110104",    "https://www.facebook.com/groups/1391094278281229/",       "https://www.facebook.com/groups/632814196817302/",    "https://www.facebook.com/groups/1906895769522241/",    "https://www.facebook.com/groups/456030584956479/",   "https://www.facebook.com/groups/1108239415925826/",    "https://www.facebook.com/groups/669371907218733/",    "https://www.facebook.com/groups/313799159030926/",   "https://www.facebook.com/groups/273817799946010/",    "https://www.facebook.com/groups/997326198008158/",    "https://www.facebook.com/groups/499202680090113/",   "https://www.facebook.com/groups/810412816110104/",    "https://www.facebook.com/groups/concorsimiur/",    "https://www.facebook.com/groups/concorsiacattedra/",   "https://www.facebook.com/groups/587804574892487/",    "https://www.facebook.com/groups/228939985060066/",    "https://www.facebook.com/groups/228708040944623/",   "https://www.facebook.com/groups/1054698134552352/",    "https://www.facebook.com/groups/317959814985111/",    "https://www.facebook.com/groups/2864592923858977/",   "https://www.facebook.com/groups/929283011464844/",    "https://www.facebook.com/groups/843336906109167/",    "https://www.facebook.com/groups/precari.scuola.docenti.ata",   "https://www.facebook.com/groups/3868133203413913",    "https://www.facebook.com/groups/917093268639754",    "https://www.facebook.com/groups/1273736532680877",   "https://www.facebook.com/groups/399194970829052",    ]     
    
    
    
    
    tesi_da_pagina = [
    "https://www.facebook.com/groups/1707578962691377",    "https://www.facebook.com/groups/1585925211899522",    "https://www.facebook.com/groups/1941536666039810",   "https://www.facebook.com/groups/499411173404344",    "https://www.facebook.com/groups/712643683692259",   "https://www.facebook.com/groups/UniversitaMilanoBicocca/?locale=it_IT",    "https://www.facebook.com/groups/453192751428510",   "https://www.facebook.com/groups/359831087482124",    ]        
    
    
    
    
    
    
    
    
    pagine_FB_Tesi_da_profilo = [
    "https://www.facebook.com/groups/429097701963375/",    "https://www.facebook.com/groups/908270576036040/",    "https://www.facebook.com/groups/110542255705652/",   "https://www.facebook.com/groups/10658296178/",    "https://www.facebook.com/groups/1561801267407264/",    "https://www.facebook.com/groups/987254675834137/",   "https://www.facebook.com/groups/247587496098645/",    "https://www.facebook.com/groups/219676868195190/",    "https://www.facebook.com/groups/1406824622964025/",   "https://www.facebook.com/groups/2228340492/",    "https://www.facebook.com/groups/1159825607467280/",    "https://www.facebook.com/groups/823182862030829/",   "https://www.facebook.com/groups/278699974441929/",    "https://www.facebook.com/groups/542133157216367/",    "https://www.facebook.com/groups/2207767823/",   "https://www.facebook.com/groups/2213780535/",    "https://www.facebook.com/groups/1941536666039810/",    "https://www.facebook.com/groups/luisscommunity/",   "https://www.facebook.com/groups/283665805577008/",    "https://www.facebook.com/groups/20563912201/",    "https://www.facebook.com/groups/3405207606416092/",   "https://www.facebook.com/groups/712643683692259/",    "https://www.facebook.com/groups/1620107648207790/",    "https://www.facebook.com/groups/499411173404344/",   "https://www.facebook.com/groups/1700555059983526/",    "https://www.facebook.com/groups/aiutotesi/",    "https://www.facebook.com/groups/687430589913069/",   "https://www.facebook.com/groups/35569958143/",    "https://www.facebook.com/groups/897226311307799/",    "https://www.facebook.com/groups/2024805981022984/",   "https://www.facebook.com/groups/285417932067286/",    "https://www.facebook.com/groups/100945319983591/",    "https://www.facebook.com/groups/703496549822529/",   "https://www.facebook.com/groups/1516070948631361/",    "https://www.facebook.com/groups/441872244890879/",    "https://www.facebook.com/groups/2275505859339274/",   "https://www.facebook.com/groups/28956585846/",    "https://www.facebook.com/groups/30393639960/",    "https://www.facebook.com/groups/196408308125184/",   "https://www.facebook.com/groups/279383633981324/",    "https://www.facebook.com/groups/152358618169380/",    "https://www.facebook.com/groups/45051708568/",   "https://www.facebook.com/groups/447128768661519/",    "https://www.facebook.com/groups/12070402766/",    "https://www.facebook.com/groups/2744982559131286/",    "https://www.facebook.com/groups/520443616782429/",    "https://www.facebook.com/groups/642039175896119/",    "https://www.facebook.com/groups/333644306940/",   "https://www.facebook.com/groups/1693562790987375/",    "https://www.facebook.com/groups/499411173404344",          ]
    
    
    
    
    
    
    
    
    pagina_FB_UDA_da_profilo = [
    "https://www.facebook.com/groups/1137198763762499/",    "https://www.facebook.com/groups/651328332776379/",    "https://www.facebook.com/groups/799888718129162/",    "https://www.facebook.com/groups/948586745268308/",   "https://www.facebook.com/groups/25159011507078212/",    "https://www.facebook.com/groups/ilmondoscuola/",    "https://www.facebook.com/groups/972764969738087/",    "https://www.facebook.com/groups/scuolainforma/",   "https://www.facebook.com/groups/grupposcuola/",    "https://www.facebook.com/groups/1650862481834970/",    "https://www.facebook.com/groups/277884802397218/",    "https://www.facebook.com/groups/945255773369024/",   "https://www.facebook.com/groups/719439560368463/",    "https://www.facebook.com/groups/442616192572458/",    "https://www.facebook.com/groups/2941802416087165/",    "https://www.facebook.com/groups/890469759547900/",   "https://www.facebook.com/groups/472473792808435/",    "https://www.facebook.com/groups/947669399443666/",    "https://www.facebook.com/groups/2024805981022984/",    "https://www.facebook.com/groups/173850744410409/",   "https://www.facebook.com/groups/197097505352300/",    "https://www.facebook.com/groups/673009937319034/",    "https://www.facebook.com/groups/531999858522473/",    "https://www.facebook.com/groups/563940565915336/",   "https://www.facebook.com/groups/772776827909353/",        ]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    Mex_Giovanna = "Preparati al meglio per il tuo esame orale del concorso docente con Help Thesis! \n\n     Offriamo supporto personalizzato per UDA e lezioni simulate per tutte le classi di concorso. \n\nPrenota subito il tuo posto: contattaci al 378 06 08 777 o scrivi a aiuto.tesi.official@gmail.com. Non perdere l’occasione di arrivare pronto e sicuro!"
    
    
    Mex_Luca_WA_UDA = "Attenzione: Chi non è interessato, può semplicemente proseguire oltre, come se nulla fosse.\n\n Piacere, sono Luca. Io ed il mio team offriamo servizio per la preparazione della lezione simulata e per l'UDA in tutte le parti e per tutte le classi di concorso, dalla consenga della traccia alla preparazione delle slides.\n Chi fosse interessato può contattarci al 378 060 8777 oppure al 3349855526.\n\n Grazie e buon lavoro a tutti.\n Team Help Tesi."
    
    Mex_Luca_FB_UDA = "Piacere, sono Luca. Io ed il mio team offriamo servizio per la preparazione della lezione simulata e per l'UDA in tutte le parti e per tutte le classi di concorso, dalla consenga della traccia alla preparazione delle slides. \nChi fosse interessato può contattarci al 378 060 8777 oppure al 3349855526.\n\n Grazie e buon lavoro a tutti.\n Team Help Tesi."
    
    Mex_Luca_pacato = "Per chi fosse interessato, qui ci sono articoli che possono essere utili per la preparazione al concorso. https://aiutotesi.altervista.org/blog/blog_UDA_lista.php. Inoltre io ed il mio team diamo una mano nella preparazione. Chi fosse interessato può contattarci al 378 060 8777. Grazie e buon lavoro a tutti."
    
    
    mex_pagine_FB_Tesi_da_profilo = "Ciao sono Luca, dottorato in ingegneria aerospaziale. \n\n Offro diversi servizi, tra cui aiuto nella stesura di tesi di laurea, project work ed altro ancora. \n Mi occupo di tutti gli aspetti, dalla creazione dell'indice alla ricerca bibliografica. Non mi offro a prezzi bassi e non capisco il voler risparmiare sulla tesi dato che è il passo più importante del percorso, quello da cui dipende la data di laurea e buona parte del voto.\n Garantisco però la qualità dell'elaborato: molti miei lavori sono stati pubblicati su riviste universitarie.\n Ho un piccolo team a cui mi appoggio per ampliare la mia offerta ma sono onesto: se so di non poterti dare una mano, lo dico subito, senza farti perdere tempo o soldi.\n\n Contattami senza impegno al 378 060 8777."
    
    mex_pagine_FB_Tesi_da_pagina = "Ciao sono Luca. \n\n Io ed il mio team ti aiutiamo nella redazione di tesi universitarie, project work e molto altro. \n Ci occupiamo di ogni songolo aspetto per procurarti un lavoro di qualità in tempi brevi. \n\n Contattaci senza impegno al 378 060 8777."
    
    
    
    mex_pagine_FB_Project_da_profilo = "Ciao sono Luca, dottorato in ingegneria aerospaziale. \n\n Offro diversi servizi, tra cui aiuto nella stesura di tesi di laurea, project work ed altro ancora. \n Mi occupo di tutti gli aspetti, dalla creazione dell'indice alla ricerca bibliografica. Non mi offro a prezzi bassi e non capisco il voler risparmiare sulla tesi dato che è il passo più importante del percorso, quello da cui dipende la data di laurea e buona parte del voto.\n Garantisco però la qualità dell'elaborato: molti miei lavori sono stati pubblicati su riviste universitarie.\n Ho un piccolo team a cui mi appoggio per ampliare la mia offerta ma sono onesto: se so di non poterti dare una mano, lo dico subito, senza farti perdere tempo o soldi.\n\n Contattami senza impegno al 378 060 8777."
    
    
    Mex_UDA_Pubbli_Giovanna = "Buongiorno a tutti!! \n Di seguito alcuni link e numeri utili  \n\nPer qualsiasi informazione scrivetemi pure☺️ \nSito lezioni simulate e manuali di preparazione\n https://aiutotesi.altervista.org/uda.html \n Numero team docenti supporto prova orale (per lezione simulata e/o uda) 378 060 8777 \n Gruppo whatsapp \n https://chat.whatsapp.com/KL0jAgGqz3vIUbcKLdWxtE \n Gruppo telegram\n https://t.me/+mL7jvfPS6EA1MDNk"
    
    
    mex_libro_pubblicit = "Ti stai preparando per il concorso PNRR2? Abbiamo scritto un libro che può esserti utile. Un'anteprima gratuita è disponibile in messaggio o sul sito https://aiutotesi.altervista.org/uda.html. Inoltre possiamo aiutarti per la prova orale. Contattaci al 378 060 8777."
    
    
    
    
    
    i = 0
    
    
    lista_utilizzata =  target_page_url_list_FB_UDA_da_pagina
    #messaggio_pubblicato =  mex_pagine_FB_Tesi_da_pagina
    messaggio_pubblicato = Mex_UDA_Pubbli_Giovanna
    #immagine = r"C:\Users\UTENTE\Downloads\Copertina_libro.PNG"
    immagine = r"C:\Users\UTENTE\Downloads\WhatsApp Image 2025-03-22 at 13.52.42.jpeg"
    #immagine = r"C:\Users\UTENTE\Desktop\tesi_profilo.jpg"
    #immagine = r"C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\Help_.PNG"
    
    for el in lista_utilizzata:
        i = i + 1
        print("\n\nStampo sulla pagina" + str(el))
        print("elemento "+ str(i) + "/" +str(len(lista_utilizzata)))
        post_from_page_to_another_page(
            page_name="La Mia Pagina Ufficiale",
            target_page_url=str(el),
            message=(messaggio_pubblicato           
            ),
            post_as_page=False,  # se vuoi testare come pagina, metti True
            #image_path=r"C:\Users\UTENTE\Desktop\TFA_inserire_12_Novembre2024.mp4"  # .mp4 funziona uguale
            #image_path=r"C:\Users\UTENTE\Desktop\tesi_profilo.jpg"  # .mp4 funziona uguale
            image_path = immagine
        )
    
    print("[DEBUG] Chiudo il browser.")
    driver.quit()
    
    end_time = time.time()  # Arresto cronometro (toc)

    # Calcola e stampa differenza (in secondi)
    elapsed = end_time - start_time
    print(f"\n\nTempo totale di esecuzione dello script: {elapsed:.2f} secondi.")
    
    
    
    
    #iscriviti sul profilo: https://www.facebook.com/groups/563940565915336/
    #https://www.facebook.com/groups/772776827909353/
    #https://www.facebook.com/groups/566805560349962/
    #https://www.facebook.com/groups/652708666889740/
    #https://www.facebook.com/groups/346193192943304/
    #https://www.facebook.com/groups/568675736559718
    #https://www.facebook.com/groups/321583555392258
    #https://www.facebook.com/groups/399194970829052