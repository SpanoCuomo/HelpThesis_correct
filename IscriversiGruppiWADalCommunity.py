import time
import subprocess
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def kill_all_chrome():
    for proc in ("chrome.exe", "chromedriver.exe"):
        subprocess.call(
            ["taskkill", "/F", "/IM", proc, "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def setup_driver(user_data_dir: str, profile_directory: str, timeout: int = 60) -> webdriver.Chrome:
    kill_all_chrome()
    time.sleep(2)

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_directory}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get("https://web.whatsapp.com")
    # Attesa robusta
    WebDriverWait(driver, timeout).until(
        EC.any_of(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']")),
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Menu' or @aria-label='Menu principale']"))
        )
    )
    return driver

def join_community_and_list_groups_by_name(
    driver: webdriver.Chrome,
    community_name: str,
    timeout: int = 15,
    sleep_between: float = 1.0
) -> List[str]:
    # la home WA Web è già caricata dal setup
    # 2) Cerca e clicca la community
    search_box = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']"))
    )
    search_box.clear(); search_box.click()
    search_box.send_keys(community_name)
    time.sleep(sleep_between)

    community_item = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[@title=\"{community_name}\"]"))
    )
    community_item.click()
    time.sleep(sleep_between)

    # 3.a) Apri il pannello "Visualizza Gruppi" della community
    try:
        view_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@aria-label,'Visualizza gruppi')]"
                " | //span[contains(text(),'Visualizza gruppi') or contains(text(),'Visualizza Gruppi')]"
            ))
        )
        view_btn.click()
        time.sleep(sleep_between)
    except TimeoutException:
        print("[WARN] Bottone 'Visualizza Gruppi' non trovato; procedo comunque a cercare i link nel feed.")
 
    # 4) Estrai i link di invito ai gruppi dal pannello (se presente), altrimenti da tutta la pagina
    try:
        panel = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
        invite_links = {
            a.get_attribute("href")
            for a in panel.find_elements(By.XPATH, ".//a[contains(@href,'chat.whatsapp.com')]")
            if a.get_attribute("href")
        }
    except TimeoutException:
        invite_links = {
            a.get_attribute("href")
            for a in driver.find_elements(By.XPATH, "//a[contains(@href,'chat.whatsapp.com')]")
            if a.get_attribute("href")
        }


















    group_names: List[str] = []
    main_win = driver.current_window_handle

    for link in invite_links:
        driver.execute_script("window.open(arguments[0], '_blank');", link)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(sleep_between)
        try:
            btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Unisciti al gruppo')]"))
            )
            btn.click()
            time.sleep(sleep_between)
        except TimeoutException:
            pass

        try:
            hdr = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//header//div[@role='button'][@title]"))
            )
            name = hdr.get_attribute("title")
        except TimeoutException:
            name = driver.title or link

        group_names.append(name)
        driver.close()
        driver.switch_to.window(main_win)
        time.sleep(sleep_between)

    return group_names

if __name__ == "__main__":
    USER_DATA_DIR = r"C:\Users\UTENTE\Desktop\Chrome_Selenium_Profile"
    PROFILE_DIR   = "Default"
    COMMUNITY_NAME = "30 CFU Ed 3 Promo MT30TFA25 O MT30"

    driver = setup_driver(USER_DATA_DIR, PROFILE_DIR)
    gruppi = join_community_and_list_groups_by_name(driver, COMMUNITY_NAME)
    print("Gruppi trovati:")
    for g in gruppi:
        print(" -", g)
    driver.quit()
