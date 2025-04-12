from bs4 import BeautifulSoup

# Apri il file HTML in modalità lettura
with open("facebook_tfa_sostegno.html", "r", encoding="utf-8") as file:
    html_content = file.read()
    print(html_content)


soup = BeautifulSoup(html_content, "html.parser")

# Trova tutti i tag <a> che contengono "facebook.com/groups/" nell'attributo href
group_links = soup.find_all("a", href=lambda href: href and "facebook.com/groups/" in href)

group_names = set()
for link in group_links:
    # Prova a ottenere il nome dal valore di aria-label
    aria_label = link.get("aria-label", "").strip()
    if aria_label:
        # Se il valore aria-label contiene la dicitura "Immagine del profilo di",
        # rimuovila per ottenere il nome pulito del gruppo
        if aria_label.lower().startswith("immagine del profilo di"):
            group_name = aria_label[len("Immagine del profilo di"):].strip()
        else:
            group_name = aria_label
    else:
        # Altrimenti, usa il testo interno dell'elemento <a>
        group_name = link.get_text(strip=True)
    
    # Escludi eventuali valori non desiderati come "Visita"
    if group_name.lower() != "visita" and group_name:
        group_names.add(group_name)

print("Nomi dei gruppi trovati:")
for name in group_names:
    print(name)
