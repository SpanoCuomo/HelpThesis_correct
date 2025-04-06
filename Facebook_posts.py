







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
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Imposta il livello desiderato (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output su console
        # logging.FileHandler("app.log", encoding="utf-8")  # Se vuoi scrivere i log su file
    ]
)
logger = logging.getLogger(__name__)


def post_from_page_to_another_page(
    page_name,
    target_page_url,
    message,
    post_as_page=True,
    image_path=None,  # se vogliamo caricare un’immagine o un video
):
    """Funzione che prova a postare su una determinata pagina/profilo/URL,
    con possibilità di caricare un’immagine o un video."""
    try:
        # Screenshot di debug
        save_screenshot(driver, "0_home_facebook.png")

        # Se voglio postare come Pagina, provo a "switchare contesto"
        if post_as_page:
            logger.debug("Provo a switchare contesto a Pagina: %s", page_name)
            try:
                css_sel = "div[aria-label='Il tuo profilo']"
                logger.debug("Cerco profile_menu con CSS: %s", css_sel)
                profile_menu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_sel))
                )
                _scroll_into_view_and_click(driver, profile_menu, "profile_menu")
                time.sleep(2)

                xp_page = f"//span[text()='{page_name}']"
                logger.debug("Cerco page_option con XPATH: %s", xp_page)
                page_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xp_page))
                )
                _scroll_into_view_and_click(driver, page_option, "page_option")
                time.sleep(5)
                logger.debug("Switchato al contesto Pagina: %s", page_name)
            except Exception as e:
                logger.warning("Non sono riuscito a switchare a Pagina (forse non serve o selettore errato). Dettagli: %s", e)
        
        logger.debug("Ora vado su: %s", target_page_url)
        driver.get(target_page_url)
        time.sleep(5)
        save_screenshot(driver, "1_target_page.png")

        # 1) Clic sul box "Scrivi qualcosa..." / "Crea un post..."
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
            logger.debug("Cerco XPATH: %s", xp_box)
            try:
                create_post_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp_box))
                )
                _scroll_into_view_and_click(driver, create_post_box, "create_post_box")
                logger.info("Trovato e cliccato box: '%s'", testo)
                box_trovato = True
                time.sleep(2)
                save_screenshot(driver, f"2_clicked_box_{testo}.png")
                break
            except TimeoutException:
                logger.debug("Timeout: non trovo pulsante box con testo '%s'", testo)
            except Exception as ex:
                logger.debug("Altra eccezione su box '%s': %s", testo, ex)

        if not box_trovato:
            logger.error("Non trovo nessun pulsante per creare un post!")
            return

        # 2) Attende la comparsa del dialog 'Crea post'
        try:
            xp_dialog = "//div[@role='dialog' and .//span[contains(text(),'Crea post')]]"
            logger.debug("Aspetto dialog 'Crea post' con XPATH: %s", xp_dialog)
            create_post_dialog = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xp_dialog))
            )
            logger.debug("Dialog 'Crea post' visibile.")
        except TimeoutException:
            logger.warning("Non appare un overlay 'Crea post', continuo lo stesso...")

        # 3) Inserimento del testo nel field contenteditable
        possibili_editor = [
            "//div[@contenteditable='true' and contains(@aria-label,'Scrivi qualcosa')]",
            "//div[@contenteditable='true' and contains(@aria-label,'Crea un post')]",
            "//div[@contenteditable='true' and contains(@aria-label,'Scrivi qualcosa a')]",
            "//div[@contenteditable='true' and contains(@aria-placeholder,'Scrivi qualcosa')]",
        ]
        editor_inserito = False
        for xp_ed in possibili_editor:
            logger.debug("Cerco editor con XPATH: %s", xp_ed)
            try:
                editor = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xp_ed))
                )
                _scroll_into_view(driver, editor)
                logger.debug("Editor trovato, inserisco il messaggio.")
                editor.send_keys(message)
                logger.info("Testo del post inserito correttamente.")
                editor_inserito = True
                time.sleep(1)
                save_screenshot(driver, "3_editor_inserito.png")
                break
            except TimeoutException:
                logger.debug("Non trovo l'editor con XPATH: %s", xp_ed)
            except Exception as ex:
                logger.debug("Altra eccezione su xp_ed=%s => %s", xp_ed, ex)

        if not editor_inserito:
            logger.error("Non trovo un campo di input con 'Scrivi qualcosa' QUI.")

        # 4) Se voglio aggiungere un file (foto/video)
        if image_path:
            logger.debug("Provo a caricare un file: %s", image_path)
            click_photo_video_and_upload(driver, image_path)

        # 5) Clic sul pulsante "Pubblica"
        xp_publish = ("//div[@role='button' and @aria-label='Pubblica' and not(@aria-disabled='true')]")
        logger.debug("Cerco pulsante 'Pubblica' con XPATH: %s", xp_publish)
        try:
            publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xp_publish))
            )
            _scroll_into_view_and_click(driver, publish_button, "publish_button")
            logger.info("Cliccato 'Pubblica'.")
            time.sleep(5)
            save_screenshot(driver, "4_post_published.png")
        except TimeoutException:
            logger.error("Non trovo il pulsante 'Pubblica' abilitato.")

        logger.info("Post pubblicato (se la pagina lo consente).")

    except Exception as e:
        logger.exception("Eccezione generale durante il post: %s", e)
    finally:
        # Screenshot finale per debug
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

def TXT_2_list(nomefile):
    with open(nomefile, "r", encoding="utf-8") as file:
            urls = json.load(file)

    ListaDaUsare = list(dict.fromkeys(urls))
    return ListaDaUsare


    
    
    
   
    

    

    
Mex_Giovanna = "Preparati al meglio per il tuo esame orale del concorso docente con Help Thesis! \n\n     Offriamo supporto personalizzato per UDA e lezioni simulate per tutte le classi di concorso. \n\nPrenota subito il tuo posto: contattaci al 378 06 08 777 o scrivi a aiuto.tesi.official@gmail.com. Non perdere l’occasione di arrivare pronto e sicuro!"
Mex_Luca_WA_UDA = "Attenzione: Chi non è interessato, può semplicemente proseguire oltre, come se nulla fosse.\n\n Piacere, sono Luca. Io ed il mio team offriamo servizio per la preparazione della lezione simulata e per l'UDA in tutte le parti e per tutte le classi di concorso, dalla consenga della traccia alla preparazione delle slides.\n Chi fosse interessato può contattarci al 378 060 8777 oppure al 3349855526.\n\n Grazie e buon lavoro a tutti.\n Team Help Tesi."
Mex_Luca_FB_UDA = "Piacere, sono Luca. Io ed il mio team offriamo servizio per la preparazione della lezione simulata e per l'UDA in tutte le parti e per tutte le classi di concorso, dalla consenga della traccia alla preparazione delle slides. \nChi fosse interessato può contattarci al 378 060 8777 oppure al 3349855526.\n\n Grazie e buon lavoro a tutti.\n Team Help Tesi."
Mex_Luca_pacato = "Per chi fosse interessato, qui ci sono articoli che possono essere utili per la preparazione al concorso. https://aiutotesi.altervista.org/blog/blog_UDA_lista.php. Inoltre io ed il mio team diamo una mano nella preparazione. Chi fosse interessato può contattarci al 378 060 8777. Grazie e buon lavoro a tutti."
mex_pagine_FB_Tesi_da_profilo = "Ciao sono Luca, dottorato in ingegneria aerospaziale. \n\n Offro diversi servizi, tra cui aiuto nella stesura di tesi di laurea, project work ed altro ancora. \n Mi occupo di tutti gli aspetti, dalla creazione dell'indice alla ricerca bibliografica. Non mi offro a prezzi bassi e non capisco il voler risparmiare sulla tesi dato che è il passo più importante del percorso, quello da cui dipende la data di laurea e buona parte del voto.\n Garantisco però la qualità dell'elaborato: molti miei lavori sono stati pubblicati su riviste universitarie.\n Ho un piccolo team a cui mi appoggio per ampliare la mia offerta ma sono onesto: se so di non poterti dare una mano, lo dico subito, senza farti perdere tempo o soldi.\n\n Contattami senza impegno al 378 060 8777."
mex_pagine_FB_Tesi_da_pagina = "Ciao sono Luca. \n\n Io ed il mio team ti aiutiamo nella redazione di tesi universitarie, project work e molto altro. \n Ci occupiamo di ogni songolo aspetto per procurarti un lavoro di qualità in tempi brevi. \n\n Contattaci senza impegno al 378 060 8777."
mex_pagine_FB_Project_da_profilo = "Ciao sono Luca, dottorato in ingegneria aerospaziale. \n\n Offro diversi servizi, tra cui aiuto nella stesura di tesi di laurea, project work ed altro ancora. \n Mi occupo di tutti gli aspetti, dalla creazione dell'indice alla ricerca bibliografica. Non mi offro a prezzi bassi e non capisco il voler risparmiare sulla tesi dato che è il passo più importante del percorso, quello da cui dipende la data di laurea e buona parte del voto.\n Garantisco però la qualità dell'elaborato: molti miei lavori sono stati pubblicati su riviste universitarie.\n Ho un piccolo team a cui mi appoggio per ampliare la mia offerta ma sono onesto: se so di non poterti dare una mano, lo dico subito, senza farti perdere tempo o soldi.\n\n Contattami senza impegno al 378 060 8777."
Mex_UDA_Pubbli_Giovanna = "Buongiorno a tutti!! \n Di seguito alcuni link e numeri utili  \n\nPer qualsiasi informazione scrivetemi pure☺️ \nSito lezioni simulate e manuali di preparazione\n https://aiutotesi.altervista.org/uda.html \n Numero team docenti supporto prova orale (per lezione simulata e/o uda) https://wa.me/3780608777 \n Gruppo whatsapp \n https://chat.whatsapp.com/KL0jAgGqz3vIUbcKLdWxtE \n Gruppo telegram\n https://t.me/+mL7jvfPS6EA1MDNk"
mex_libro_pubblicit = "Ti stai preparando per il concorso PNRR2? Abbiamo scritto un libro che può esserti utile. Un'anteprima gratuita è disponibile in messaggio o sul sito https://aiutotesi.altervista.org/uda.html. Inoltre possiamo aiutarti per la prova orale. Contattaci al 378 060 8777."


    
    




# ESEMPIO DI ESECUZIONE
if __name__ == "__main__":
    
    start_time = time.time()  # Avvio cronometro (tic)
    user_data_dir=r"C:\Users\lspan\AppData\Local\Google\Chrome\User Data"
    profile_directory="Profile 2"
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
    
    
    i = 0
    
    
    lista_utilizzata =  "UDA_da_pagina.txt"
    #lista_utilizzata = "FB_Tesi_Da_Pagina.txt"
    #messaggio_pubblicato =  mex_pagine_FB_Tesi_da_pagina
    messaggio_pubblicato = Mex_UDA_Pubbli_Giovanna
    #immagine = r"C:\Users\UTENTE\Downloads\Copertina_libro.PNG"
    #immagine = r"C:\Users\lspan\Desktop\Uda_Sfondo_celeste.jpg"
    #immagine = r"C:\Users\lspan\Desktop\ImmaginiSitoTesi\cliccabile.pdf"
    #immagine = r"https://aiutotesi.altervista.org/Uda_Sfondo_celeste.jpg"
    immagine = r"C:\Users\UTENTE\Desktop\tesi_profilo.jpg"
    #immagine = r"C:\Users\UTENTE\Desktop\ImmaginiSitoTesi\Help_.PNG"
    
    
    for el in TXT_2_list(lista_utilizzata):
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













