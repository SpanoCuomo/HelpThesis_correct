# Inserire una volta immagine, una volta video, altrimenti che ho a fare le immagini?
# Vedi se puoiparalizzarlo ma non so se ne valga la pena
# inserisci tutte le storie e screen da posts.php
# Magari vedere anche le risposte dei clienti e parti di esercizi già svolti

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 
 
import json
from contextlib import contextmanager
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
import requests
import re
import os
import random
import subprocess
import sys
from itertools import zip_longest
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
from urllib.parse import urlparse
from selenium.webdriver.common.action_chains import ActionChains
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from colorama import init as colorama_init, Fore, Style


driver = None
debug_mode = True

PC_Grande = True




# --- DIR log/artifacts ---
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "whatsapp_status_imgs")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
LOG_DIR = os.path.join(DOWNLOAD_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOGFILE = os.path.join(LOG_DIR, f"wa_{RUN_ID}.log")

def setup_logger():
    logger = logging.getLogger("wa")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = RotatingFileHandler(LOGFILE, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt); fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt); ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    logger.addHandler(fh); logger.addHandler(ch)
    logger.info(f"Log file: {LOGFILE}")
    return logger

logger = setup_logger()

def dump_artifacts(driver, tag):
    ts = int(time.time())
    png = os.path.join(DOWNLOAD_DIR, f"{tag}_{ts}.png")
    html = os.path.join(DOWNLOAD_DIR, f"{tag}_{ts}.html")
    try:
        driver.save_screenshot(png)
        Path(html).write_text(driver.page_source, encoding="utf-8")
        logger.warning(f"ARTIFACTS saved: {png} | {html}")
    except Exception:
        logger.exception(f"dump_artifacts failed for {tag}")
    return png, html

def log_browser_console(driver, prefix="BROWSER"):
    try:
        logs = driver.get_log("browser")
        for entry in logs[-100:]:
            logger.debug(f"{prefix} {entry.get('level')} {entry.get('timestamp')}: {entry.get('message')}")
    except Exception:
        # alcuni driver non espongono i log
        pass

@contextmanager
def step(name):
    t0 = time.time()
    logger.info(f"▶ {name}")
    try:
        yield
        logger.info(f"✅ {name} ({time.time()-t0:.2f}s)")
    except Exception:
        logger.exception(f"❌ {name} failed after {time.time()-t0:.2f}s")
        raise


def stampa_colore(testo, colore="default"):
    colori = {
        "verde": "\033[92m",
        "rosso": "\033[91m",
        "giallo": "\033[93m",
        "default": "\033[0m"
    }
    msg = colori.get(colore, colori["default"]) + testo + colori["default"]
    print(msg)
    # Log strutturato
    if colore == "rosso":
        logger.error(testo)
    elif colore == "giallo":
        logger.warning(testo)
    else:
        logger.info(testo)


def setup_driver(user_data_dir, profile_directory):
    chrome_options = Options()
    os.makedirs(user_data_dir, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # 👉 abilita i log del browser
    try:
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    except Exception:
        pass

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.maximize_window()
    except Exception:
        pass
    logger.info(f"Using profile: {user_data_dir} | {profile_directory}")
    return driver



# --- Abilita colori ANSI su CMD/PowerShell (Windows) e UTF-8 per emoji ---
def enable_console_colors():
    """
    Abilita i colori ANSI su Windows CMD/PowerShell.
    1) Tenta con Colorama (se presente).
    2) In fallback usa le WinAPI per attivare le VT sequences.
    3) Prova a portare stdout/stderr in UTF-8 (emoji, accenti).
    """
    # su Linux/macOS non serve nulla
    if os.name != "nt":
        return
    try:
        import colorama
        # Colorama >= 0.4.6: abilita automaticamente le VT sequences
        colorama.just_fix_windows_console()
        # Per versioni più vecchie: colorama.init()
    except Exception:
        # Fallback senza dipendenze: abilita VT via WinAPI
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            for handle in (-11, -12):  # STD_OUTPUT_HANDLE=-11, TD_ERROR_HANDLE=-12
                h = kernel32.GetStdHandle(handle)
                mode = ctypes.c_uint32()
                if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                   ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                   kernel32.SetConsoleMode(h, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

        except Exception:
            # Se anche questo fallisce, semplicemente niente colori su vecchie console.
            pass
    # (facoltativo) forziamo UTF-8 per stampare emoji e accenti correttamente
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Chiamare subito all'avvio, prima di stampare qualunque cosa
enable_console_colors()

Numero_post_Inserire = 10

# Variabile globale per riutilizzare lo stesso driver



def force_click(driver, el):
    driver.execute_script("""
        const el = arguments[0];
        const clickable = el.closest('button,[role=button],[role=tab],a,div[tabindex]') || el;
        clickable.scrollIntoView({block: 'center', inline: 'center'});
        clickable.dispatchEvent(new MouseEvent('mouseover', {bubbles:true, cancelable:true}));
        clickable.dispatchEvent(new MouseEvent('mousedown', {bubbles:true, cancelable:true}));
        clickable.dispatchEvent(new MouseEvent('mouseup',   {bubbles:true, cancelable:true}));
        clickable.dispatchEvent(new MouseEvent('click',     {bubbles:true, cancelable:true}));
    """, el)

def apri_tab_aggiornamenti(driver, timeout=20):
    """
    Clicca l'icona/tab 'Stato' (tooltip 'Stato') con fallback 'Status/Aggiornamenti/Updates'.
    Ritorna True se la sezione Stato è aperta (rileva '+' o lista stati o tab selezionato).
    """
    end = time.time() + timeout
    selectors = [
        # tooltip/aria/title IT/EN
        "//*[@aria-label='Stato' or @title='Stato' or contains(@aria-label,'Stato') or contains(@title,'Stato')]",
        "//*[@aria-label='Status' or @title='Status' or contains(@aria-label,'Status') or contains(@title,'Status')]",
        "//*[@aria-label='Aggiornamenti' or @title='Aggiornamenti' or contains(@aria-label,'Aggiornamenti')]",
        "//*[@aria-label='Updates' or @title='Updates' or contains(@aria-label,'Updates')]",
        # testid/icone
        "//*[@data-testid='updates' or @data-testid='status-tab' or @data-testid='statusV3' or @data-testid='status-v3-tab']",
        "//*[@data-icon='status' or contains(@data-icon,'status')]",
    ]

    def stato_aperto():
        if driver.find_elements(By.XPATH, "//*[@data-testid='statusV3Add' or @data-testid='status-v3-add']"):
            return True
        if driver.find_elements(By.XPATH, "//*[contains(@data-testid,'status') and contains(@data-testid,'list')]"):
            return True
        if driver.find_elements(By.XPATH, "//*[@aria-label='Stato' and (@aria-selected='true' or @aria-pressed='true')]"):
            return True
        if driver.find_elements(By.XPATH, "//*[@aria-label='Status' and (@aria-selected='true' or @aria-pressed='true')]"):
            return True
        return False

    logger.info("Open 'Stato' tab: trying selectors...")
    while time.time() < end:
        if stato_aperto():
            return True
        for xp in selectors:
            try:
                els = driver.find_elements(By.XPATH, xp)
                logger.debug(f"tab 'Stato': xp={xp} found={len(els)}")
                if not els:
                    continue
                force_click(driver, els[0])
                time.sleep(0.4)
                if stato_aperto():
                    logger.info("Open 'Stato': OK")
                    return True
            except Exception as e:
                logger.debug(f"tab 'Stato': click failed xp={xp} err={e}")
        time.sleep(0.2)
    logger.warning("Open 'Stato': timeout")
    return False


def invia_storia(driver, file_path, testo=""):
    with step("Open 'Stato' tab"):
        if not apri_tab_aggiornamenti(driver, timeout=20):
            dump_artifacts(driver, "wa_tab_fail")
            stampa_colore("[ERRORE] Apertura 'Stato' fallita", "rosso")
            return False

    with step("Open composer '+'"):
        if not apri_compositore_status(driver, timeout=20):
            dump_artifacts(driver, "wa_plus_fail")
            stampa_colore("[ERRORE] Impossibile aprire il compositore", "rosso")
            return False

    with step("Seleziona 'Foto e video' nel popup"):
        if not apri_picker_foto_video_status(driver, timeout=12):
            dump_artifacts(driver, "wa_picker_fail")
            stampa_colore("[ERRORE] Non trovo/clicco 'Foto e video' nel popup", "rosso")
            return False

    with step(f"Upload media: {os.path.basename(file_path)}"):
        ok_up = upload_status_media(driver, file_path, timeout=120)  # tempo alto per i video
        if not ok_up:
            dump_artifacts(driver, "wa_upload_fail")
            return False

    with step("Wait preview & set caption"):
        try:
            if testo:
                # imposta la caption nel DIALOG del composer (non globalmente)
                imposta_didascalia(driver, testo, timeout=30)
        except Exception:
            logger.warning("Caption non impostata (eccezione)")

    with step("Invia lo stato"):
        ok_send = click_invia_con_fallback(driver, timeout=180)
        if not ok_send:
            # dump profondo dei candidati bottone
            debug_dump_send_candidates(driver, tag="wa_send_probe")
            dump_artifacts(driver, "wa_send_not_ready")
            logger.error("Invio: nessun bottone e fallback tastiera falliti")
            return False

    with step("Verifica pubblicazione (dialog chiuso)"):
        if not wait_dialog_chiuso(driver, timeout=25):
            # se il dialog resta aperto potremmo avere ancora overlay o invio non partito
            debug_dump_send_candidates(driver, tag="wa_dialog_still_open")
            dump_artifacts(driver, "wa_send_dialog_non_chiuso")
            logger.warning("Il dialog non si è chiuso: la pubblicazione potrebbe non essere avvenuta")
            return False

    return True



def _visible_any(driver, xpaths):
    """True se TROVA almeno un elemento VISIBILE fra gli xpath."""
    for xp in xpaths:
        try:
            els = driver.find_elements(By.XPATH, xp)
            for el in els:
                try:
                    if el.is_displayed():
                        return True
                except StaleElementReferenceException:
                    continue
        except Exception:
            continue
    return False

def wa_wait_ready(driver, timeout=60):
    """
    Attende che WhatsApp Web sia pronto.
    Ritorna:
      "ready"   se la lista chat o il tab aggiornamenti è VISIBILE,
      "qr"      se il QR è VISIBILE,
      "timeout" se scade l'attesa.
    """
    end = time.time() + timeout
    while time.time() < end:
        # 1) Preferisci stato "ready" se la UI è visibile
        ready_xps = [
            "//*[@id='pane-side' and not(contains(@style,'display: none'))]",
            "//*[@aria-label='Elenco chat' or @aria-label='Chat list']",
            "//*[@data-testid='chat-list']",
            "//*[@data-testid='updates' or @aria-label='Stato' or @aria-label='Status']",
        ]
        if _visible_any(driver, ready_xps):
            return "ready"

        # 2) QR solo se davvero VISIBILE (no matcher generici col testo 'QR')
        qr_xps = [
            "//*[@data-testid='qrcode']",
            "//canvas[@aria-label='Scan me' or contains(@aria-label,'QR')]",
        ]
        if _visible_any(driver, qr_xps):
            return "qr"

        time.sleep(0.5)
    return "timeout"

def click_first_that_exists(driver, xpaths, timeout=10, via_js=True):
    end = time.time() + timeout
    tries = 0
    while time.time() < end:
        for xp in xpaths:
            tries += 1
            els = driver.find_elements(By.XPATH, xp)
            logger.debug(f"click_first: xp={xp} found={len(els)}")
            if els:
                el = els[0]
                try:
                    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xp)))
                except Exception:
                    pass
                try:
                    if via_js:
                        driver.execute_script("arguments[0].click();", el)
                    else:
                        el.click()
                    logger.debug(f"click_first: clicked xp={xp}")
                    return True
                except Exception as e:
                    logger.debug(f"click_first: click failed xp={xp} err={e}")
                    try:
                        force_click(driver, el)
                        logger.debug(f"click_first: force_clicked xp={xp}")
                        return True
                    except Exception as ee:
                        logger.debug(f"click_first: force_click failed xp={xp} err={ee}")
        time.sleep(0.2)
    logger.warning(f"click_first: timeout after {tries} tries")
    return False

def apri_compositore_status(driver, timeout=15):
    """
    Apre il compositore 'Nuovo stato' (il pulsante '+').
    """
    plus_xps = [
        "//*[@data-testid='statusV3Add' or @data-testid='status-v3-add']",
        "//span[contains(@data-icon,'status-v3-plus') or @data-icon='plus']/ancestor::*[@role='button']",
        "//*[@aria-label='Nuovo aggiornamento' or @aria-label='New status' or @title='Nuovo aggiornamento' or @title='New status']",
    ]
    if click_first_that_exists(driver, plus_xps, timeout=timeout, via_js=True):
        try:
            WebDriverWait(driver, 12).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//input[@type='file' and (contains(@accept,'image') or contains(@accept,'video'))] | "
                    "//*[self::canvas or self::video or self::img]"
                ))
            )
            return True
        except Exception:
            return False
    return False

def apri_picker_foto_video_status(driver, timeout=12):
    """
    Nel popup del composer 'Stato' clicca la voce 'Foto e video' (IT) o 'Photo/Video' (EN).
    Dopo il click, aspetta che compaia un input file o un’anteprima.
    """
    logger.info("Provo a cliccare 'Foto e video' nel popup")
    end = time.time() + timeout
    xps = [
        # match preciso sul testo visibile
        "//*[normalize-space(.)='Foto e video']",
        "//*[@role='menu']//*[normalize-space(.)='Foto e video']",
        "//*[@role='dialog']//*[normalize-space(.)='Foto e video']",
        # fallback inglese
        "//*[normalize-space(.)='Photo & video' or normalize-space(.)='Photos & videos' or normalize-space(.)='Photo/Video']",
        "//*[@role='menu']//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'photo') and contains(.,'video')]",
        # se l’elemento è dentro un popover generico
        "//*[contains(@data-testid,'menu') or contains(@data-testid,'popover')]//*[normalize-space(.)='Foto e video']",
    ]
    while time.time() < end:
        for xp in xps:
            els = driver.find_elements(By.XPATH, xp)
            logger.debug(f"picker 'Foto e video': xp={xp} found={len(els)}")
            if not els:
                continue
            el = els[0]
            try:
                # risaliamo al container cliccabile (menuitem/button)
                clickable = driver.execute_script(
                    "return arguments[0].closest('[role=menuitem],[role=button],button,li,div[tabindex]') || arguments[0];",
                    el
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", clickable)
                driver.execute_script("arguments[0].click();", clickable)
                time.sleep(0.3)
                # dopo il click dovrebbe comparire input o anteprima
                if driver.find_elements(By.XPATH, "//input[@type='file']") or \
                   driver.find_elements(By.XPATH, "//*[self::img or self::video or self::canvas]"):
                    logger.info("Clic su 'Foto e video' riuscito")
                    return True
            except Exception as e:
                logger.debug(f"click 'Foto e video' fallito: {e}")
        time.sleep(0.2)
    logger.warning("Non sono riuscito a cliccare 'Foto e video' (timeout)")
    return False

missing_media = []


def fetch_to_local(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        filename = os.path.basename(urlparse(path_or_url).path)
        local_path = os.path.join(DOWNLOAD_DIR, filename)
        if not os.path.exists(local_path):
            try:
                resp = requests.get(path_or_url, stream=True)
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
            except requests.exceptions.HTTPError:
                print(f"[WARN] Media non trovato: {path_or_url}")
                missing_media.append(path_or_url)
                return None
            except Exception as e:
                print(f"[WARN] Errore scaricando {path_or_url}: {e}")
                missing_media.append(path_or_url)
                return None
        return local_path
    else:
        return path_or_url

def kill_all_chrome():
    stampa_colore("📌 Sto provando a chiudere Chrome e ChromeDriver...", "giallo")
    chiuso = True
    for proc in ("chrome.exe", "chromedriver.exe"):
        risultato = subprocess.call(
            ["taskkill", "/F", "/IM", proc, "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if risultato == 0:
            stampa_colore(f"✅ {proc} terminato correttamente.", "verde")
        else:
            stampa_colore(f"⚠️ {proc} non trovato o non terminato.", "rosso")
            chiuso = False

    if chiuso:
        stampa_colore("Tutti i processi Chrome sono stati terminati correttamente.", "verde")
    else:
        stampa_colore("Alcuni processi non erano in esecuzione o non sono stati chiusi.", "giallo")
      

def extract_posts_from_php(source, base_url):
    if source.startswith("http"):
        response = requests.get(source)
        content = response.text
    else:
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

    # Normalizza prima, poi compila i pattern
    content = " ".join(content.split())

    pattern_slug = re.compile(r"""['"]slug['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_image = re.compile(r"""['"]image['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_summary = re.compile(r"""['"]summary['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_video = re.compile(r"""['"]video['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_screen = re.compile(r"""['"]screen['"]\s*=>\s*['"]([^'"]+)['"]""")
    pattern_stories = re.compile(r"""['"]stories['"]\s*=>\s*['"]([^'"]+)['"]""")

    slugs = pattern_slug.findall(content)
    images = pattern_image.findall(content)
    summaries = pattern_summary.findall(content)
    videos = pattern_video.findall(content)
    screens = pattern_screen.findall(content) if pattern_screen.findall(content) else []
    stories = pattern_stories.findall(content) if pattern_stories.findall(content) else []

    posts_data = []
    for i, (slug, img, summ, vid) in enumerate(
        zip_longest(slugs, images, summaries, videos, fillvalue="")
    ):
        scr = screens[i] if i < len(screens) else ""
        sto = stories[i] if i < len(stories) else ""
        posts_data.append({
            "slug": slug,
            "image": img,
            "summary": summ,
            "video": vid,
            "screen": scr,
            "stories": sto,
            "full_url": base_url + slug if slug else "",
        })
    return posts_data

def find_status_file_input(driver, timeout=10):
    """
    Trova l'input file del composer Stato (anche se nascosto).
    Ritorna il WebElement o None.
    """
    candidates = [
        "//input[@type='file' and (contains(@accept,'image') or contains(@accept,'video'))]",
        "//*[@data-testid='status']//*[contains(@accept,'image') or contains(@accept,'video') and self::input]",
        "//input[@type='file' and contains(@data-testid,'file-input')]",
    ]
    end = time.time() + timeout
    last_exc = None
    while time.time() < end:
        for xp in candidates:
            try:
                els = driver.find_elements(By.XPATH, xp)
                logger.debug(f"find_status_file_input: xp={xp} found={len(els)}")
                if not els:
                    continue
                # Preferisci l'ultimo (spesso quello effettivo è creato dinamicamente)
                el = els[-1]
                return el
            except Exception as e:
                last_exc = e
        time.sleep(0.2)
    if last_exc:
        logger.debug(f"find_status_file_input: last_exc={last_exc}")
    return None

def dismiss_overlays(driver):
    """
    Chiude eventuali overlay (permessi, tooltip) che bloccano i click/preview.
    """
    candidates = [
        "//*[@role='dialog']//button[.='Non ora' or .='Non consentire' or .='Chiudi' or .='Close' or .='Not now']",
        "//*[@data-testid='x' or @data-testid='close' or @aria-label='Chiudi' or @aria-label='Close']",
    ]
    for xp in candidates:
        try:
            els = driver.find_elements(By.XPATH, xp)
            if els:
                driver.execute_script("arguments[0].click();", els[0])
                time.sleep(0.2)
                logger.debug(f"dismiss_overlays: clicked {xp}")
        except Exception:
            pass

def upload_status_media(driver, file_path, timeout=90):
    """
    Dopo aver selezionato 'Foto e video' nel popup:
    - trova TUTTI gli input file (anche se nascosti)
    - prova a fare send_keys() su ciascuno
    - attende la comparsa dell'anteprima (img/video/canvas)
    Ritorna True se l'anteprima appare, False altrimenti.
    """
    abs_path = os.path.abspath(file_path)
    logger.info(f"Upload media: {abs_path}")

    def all_inputs():
        XPS = [
            # input standard
            "//input[@type='file' and (contains(@accept,'image') or contains(@accept,'video'))]",
            # input sotto nodi 'status'
            "//*[@data-testid='status']//input[@type='file']",
            # input con testid generici
            "//input[@type='file' and contains(@data-testid,'file-input')]",
        ]
        out = []
        for xp in XPS:
            try:
                found = driver.find_elements(By.XPATH, xp)
                logger.debug(f"upload_status_media: xp={xp} found={len(found)}")
                out.extend(found)
            except Exception:
                pass
        # dedup per id selenium
        uniq, seen = [], set()
        for el in out:
            try:
                if el.id not in seen:
                    seen.add(el.id)
                    uniq.append(el)
            except Exception:
                continue
        return uniq

    # assicurati che il composer sia aperto e che la voce 'Foto e video' sia stata selezionata
    # (necessario perché altrimenti l'input non viene creato)
    if not all_inputs():
        apri_compositore_status(driver, timeout=6)
        apri_picker_foto_video_status(driver, timeout=6)

    tried = 0
    for attempt in range(3):  # WA a volte ricrea l'input; fai più giri
        inputs = all_inputs()
        if not inputs:
            # riprova a far comparire il picker
            apri_picker_foto_video_status(driver, timeout=4)
            inputs = all_inputs()

        # prova ogni input disponibile
        for inp in inputs:
            tried += 1
            try:
                # rendi l'input "usabile" anche se nascosto
                driver.execute_script("""
                    arguments[0].style.display = 'block';
                    arguments[0].removeAttribute('hidden');
                    arguments[0].removeAttribute('disabled');
                """, inp)
                inp.send_keys(abs_path)
                logger.debug(f"upload_status_media: send_keys OK su input #{tried}")

                # attesa anteprima (immagine/video/canvas) o messaggio di errore
                end = time.time() + timeout
                while time.time() < end:
                    dismiss_overlays(driver)
                    if driver.find_elements(By.XPATH, "//*[self::img or self::video or self::canvas]"):
                        logger.info("upload_status_media: anteprima presente")
                        return True
                    if driver.find_elements(By.XPATH, "//*[contains(.,'non supportato') or contains(.,'not supported')]"):
                        logger.error("upload_status_media: formato non supportato")
                        return False
                    time.sleep(0.5)
            except Exception as e:
                logger.debug(f"upload_status_media: send_keys fallito su input #{tried}: {e}")

        # piccolo respiro e un altro giro (input può essere ricreato)
        time.sleep(0.5)

    logger.error("upload_status_media: nessun input ha prodotto l'anteprima (timeout)")
    return False

def _get_status_dialog(driver):
    """
    Ritorna il container del composer (dialog/popup) se presente, altrimenti None.
    """
    dialogs = driver.find_elements(By.XPATH, "//*[@role='dialog' or @data-testid='modal-layer']")
    return dialogs[-1] if dialogs else None


def imposta_didascalia(driver, testo, timeout=30):
    """
    Imposta la didascalia SOLO dentro al dialog del composer Stato.
    Se il campo non c'è, non fallisce: logga e prosegue (alcune UI non hanno caption distinta).
    """
    root = _get_status_dialog(driver)
    if not root:
        logger.warning("imposta_didascalia: dialog non trovato")
        return False

    end = time.time() + timeout
    # possibili target nel dialog
    xps = [
        ".//*[@placeholder='Aggiungi una didascalia' or @placeholder='Aggiungi didascalia' or @placeholder='Scrivi una didascalia' or @placeholder='Add a caption' or @placeholder='Write a caption']",
        ".//*[@data-testid='status-v3-caption' or @data-testid='media-caption-input' or @data-testid='caption-input']",
        ".//div[@contenteditable='true' and @role='textbox' and (contains(@class,'selectable-text') or contains(@data-testid,'caption'))]",
        ".//*[contains(normalize-space(.),'Aggiungi una didascalia') or contains(normalize-space(.),'Aggiungi didascalia') or contains(normalize-space(.),'Add a caption')]/ancestor::*[@role='textbox' or @contenteditable='true'][1]",
    ]
    while time.time() < end:
        for xp in xps:
            try:
                els = root.find_elements(By.XPATH, xp)
                if not els:
                    continue
                fld = els[0]
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", fld)
                driver.execute_script("arguments[0].click();", fld)
                time.sleep(0.1)
                # pulisci e scrivi
                try:
                    fld.clear()
                except Exception:
                    pass
                fld.send_keys(Keys.CONTROL, "a")
                fld.send_keys(Keys.DELETE)
                fld.send_keys(testo)
                logger.debug("imposta_didascalia: testo impostato nel campo caption del dialog")
                return True
            except Exception as e:
                logger.debug(f"imposta_didascalia: tentativo fallito xp={xp} err={e}")
        time.sleep(0.3)
    logger.warning("imposta_didascalia: campo didascalia non trovato nel dialog (proseguo senza)")
    return False


def _find_send_in_dialog(driver):
    """
    Cerca il bottone 'Invia/Pubblica' DENTRO il dialog del composer e restituisce
    l'elemento cliccabile (button/div con role=button).
    """
    root = _get_status_dialog(driver)
    scope = root if root else driver  # in casi estremi prova globalmente

    # Selettori vari (testid, aria, icona send)
    selectors = [
        ".//*[@data-testid='status-v3-send' or @data-testid='send']",
        ".//*[@aria-label='Invia' or @aria-label='Send' or contains(@aria-label,'Pubblica') or contains(@aria-label,'Publish')]",
        ".//*[self::button or @role='button'][.//span[contains(@data-icon,'send')]]",
        ".//span[contains(@data-icon,'send')]/ancestor::*[self::button or @role='button' or self::div][1]",
    ]

    for sel in selectors:
        try:
            candidates = scope.find_elements(By.XPATH, sel)
            for el in candidates:
                # risaliamo al container cliccabile
                clickable = driver.execute_script(
                    "return arguments[0].closest('button,[role=button],div[tabindex]') || arguments[0];",
                    el
                )
                if not clickable:
                    continue
                # verifica non disabilitato sul nodo o parent
                disabled_here = (clickable.get_attribute("disabled") or
                                 clickable.get_attribute("aria-disabled") in ("true", True))
                parent = driver.execute_script("return arguments[0].parentElement;", clickable)
                disabled_parent = False
                if parent:
                    disabled_parent = ( (parent.get_attribute("disabled")) or
                                        (parent.get_attribute("aria-disabled") in ("true", True)) )
                if disabled_here or disabled_parent:
                    continue
                # visibile?
                try:
                    if not clickable.is_displayed():
                        continue
                except Exception:
                    pass
                return clickable
        except Exception:
            continue
    return None


def click_invia_con_fallback(driver, timeout=180):
    """
    Attende che il bottone diventi disponibile nel dialog e clicca.
    Se non compare, prova Enter/Ctrl+Enter come fallback.
    """
    end = time.time() + timeout
    while time.time() < end:
        dismiss_overlays(driver)
        btn = _find_send_in_dialog(driver)
        if btn:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                logger.info("Invio: click su bottone SEND")
                return True
            except Exception as e:
                logger.debug(f"Invio: click fallito, ritento... {e}")
        time.sleep(0.5)

    # Fallback: tentiamo invio da tastiera sul dialog
    logger.warning("Invio: bottone non trovato, provo Enter/Ctrl+Enter come fallback")
    root = _get_status_dialog(driver)
    try:
        target = root if root else driver.find_element(By.TAG_NAME, "body")
        ActionChains(driver).move_to_element(target).click().perform()
        time.sleep(0.1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(1.0)
        # secondo tentativo
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        return True
    except Exception as e:
        logger.debug(f"Invio fallback tastiera fallito: {e}")
        return False


def wait_dialog_chiuso(driver, timeout=20):
    """
    Dopo il click su Invia, attendi che il dialog del composer si chiuda (segno che è stato pubblicato).
    """
    end = time.time() + timeout
    while time.time() < end:
        if not _get_status_dialog(driver):
            return True
        time.sleep(0.5)
    return False


def wait_status_ready_to_send(driver, timeout=120):
    """
    Attende che il pulsante 'Invia' diventi cliccabile (video: serve tempo di elaborazione).
    """
    send_xps = [
        "//*[@data-testid='send' or @data-testid='status-v3-send']",
        "//div[@role='button' and (@aria-label='Invia' or @aria-label='Send' or contains(@aria-label,'Pubblica'))]",
        "//span[contains(@data-icon,'send')]/ancestor::*[@role='button']",
        "//button[contains(@aria-label,'Invia') or contains(@aria-label,'Send')]",
    ]
    end = time.time() + timeout
    while time.time() < end:
        dismiss_overlays(driver)
        for xp in send_xps:
            try:
                btns = driver.find_elements(By.XPATH, xp)
                if not btns:
                    continue
                btn = btns[0]
                # abilitato?
                disabled = btn.get_attribute("aria-disabled")
                if disabled in ("true", True):
                    logger.debug("wait_ready_to_send: send disabilitato, continuo...")
                    continue
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                return btn
            except Exception:
                continue
        time.sleep(0.5)
    return None



def invia_storie_whatsapp(pc_grande: bool = True, numero_post: int = 1) -> int:
    """
    Scarica i media da posts.php, apre WhatsApp Web e pubblica fino a `numero_post` storie.
    Ritorna il numero di invii riusciti.
    """
    numero_post = max(1, int(numero_post))

    # Profilo Chrome persistente
    if pc_grande:
        user_data_dir = r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
        stampa_colore("✅ Sono nel PC grande", "verde")
    else:
        user_data_dir = r"C:\Users\lspan\Desktop\Chrome_Selenium_Profile"
        profile_directory = "Default"
        stampa_colore("✅ Sono nel PC piccolo", "verde")

    driver = None
    sent = 0

    try:
        # ============================
        # 1) Setup driver
        # ============================
        with step("Setup driver"):
            driver = setup_driver(user_data_dir, profile_directory)
            stampa_colore(f"✅ Setup_driver: {driver}", "verde")

        # ============================
        # 2) Scarico elenco post e scelgo i media (video/img, fallback screen)
        # ============================
        base_url = "https://aiutotesi.altervista.org/blog/"
        php_url_raw = "https://aiutotesi.altervista.org/blog/posts.php?raw=1"

        with step("Scarico posts.php e scelgo media"):
            local_php = fetch_to_local(php_url_raw)
            if not local_php or not os.path.exists(local_php):
                stampa_colore("❌ Impossibile scaricare posts.php?raw=1", "rosso")
                return 0

            posts = extract_posts_from_php(local_php, base_url)
            random.shuffle(posts)

            urls = []
            next_is_video = True
            seen = set()
            for p in posts:
                rel = ""
                if next_is_video and p.get("video"):
                    rel = p["video"]
                    next_is_video = False
                elif p.get("image"):
                    rel = p["image"]
                    next_is_video = True
                elif p.get("screen"):
                    rel = p["screen"]  # non cambia il toggle

                if rel:
                    full = base_url + rel
                    if full not in seen:
                        urls.append(full)
                        seen.add(full)
                if len(urls) >= numero_post:
                    break

            logger.info(f"posts parsed={len(posts)} | scelti={len(urls)}")
            if not urls:
                stampa_colore("❌ Nessun media disponibile da posts.php", "rosso")
                return 0

        # ============================
        # 3) Download media locali
        # ============================
        with step("Download media"):
            local_paths = {}
            with ThreadPoolExecutor(max_workers=5) as exe:
                future_to_url = {exe.submit(fetch_to_local, u): u for u in urls}
                for fut in as_completed(future_to_url):
                    url = future_to_url[fut]
                    local = fut.result()
                    if local:
                        stampa_colore(f"✅ Scaricato correttamente: {url}", "verde")
                        local_paths[url] = local
                    else:
                        stampa_colore(f"❌ Errore nel download: {url}", "rosso")

            logger.info(f"media scaricati OK={len(local_paths)} / {len(urls)}")
            if not local_paths:
                stampa_colore("❌ Nessun media scaricato: interrompo.", "rosso")
                return 0

        # ============================
        # 4) Apri WhatsApp Web e attendi UI pronta
        # ============================
        with step("Apri WhatsApp Web"):
            driver.get("https://web.whatsapp.com/")
            # bootstrap DOM
            for _ in range(50):
                try:
                    if driver.execute_script("return document.readyState") == "complete":
                        break
                except Exception:
                    pass
                time.sleep(0.2)

        with step("Attendo UI ready"):
            stato = wa_wait_ready(driver, timeout=200)
            stampa_colore(f"⏱️ Stato interfaccia: {stato}", "giallo")

            if stato == "qr":
                dump_artifacts(driver, "wa_qr")
                stampa_colore("🔒 WhatsApp richiede la scansione del QR. Scansiona e rilancia.", "giallo")
                return 0
            if stato != "ready":
                dump_artifacts(driver, "wa_timeout")
                stampa_colore("⏳ UI non pronta (timeout).", "rosso")
                return 0

        # ============================
        # 5) Invio storie
        # ============================
        for p in posts:
            # scegli, per quel post, il primo media tra video -> image -> screen già scaricato
            chosen_url = None
            for rel in (p.get("video"), p.get("image"), p.get("screen")):
                if not rel:
                    continue
                full = base_url + rel
                if full in local_paths:
                    chosen_url = full
                    break
            if not chosen_url:
                continue  # nessun media disponibile per questo post

            local = local_paths[chosen_url]
            testo = f"{p['summary']} {base_url}{p['slug']}"
            logger.info(f"→ PROVO a inviare: {os.path.basename(local)} | slug={p['slug']}")

            ok = invia_storia(driver, local, testo)
            if ok:
                stampa_colore("✅ Storia inviata.", "verde")
                sent += 1
            else:
                stampa_colore("❌ Invio storia fallito, passo al prossimo media.", "rosso")
                dump_artifacts(driver, "wa_send_loop_fail")

            if sent >= numero_post:
                break

            # pausa breve tra gli invii (video potrebbero richiedere più tempo)
            ext = os.path.splitext(local)[1].lower()
            time.sleep(8 if ext in (".mp4", ".mov", ".mkv", ".webm") else 4)

        return sent

    finally:
        # ============================
        # 6) Cleanup driver
        # ============================
        time.sleep(1.5)
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        logger.info(f"Invii riusciti: {sent}/{numero_post}")
