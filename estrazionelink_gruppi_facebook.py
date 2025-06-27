<<<<<<< HEAD
from bs4 import BeautifulSoup

# Legge il contenuto del file HTML
with open("facebook_tfa_sostegno.html", "r", encoding="utf-8") as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, "html.parser")

# Trova tutti i tag <a> che contengono "facebook.com/groups/" nell'attributo href
group_links = soup.find_all("a", href=lambda href: href and "facebook.com/groups/" in href)

# Stampiamo solo i link, filtrando eventuali duplicati se necessario
links = set()
for link in group_links:
    url = link.get("href")
    if url:
        links.add(url)

for url in links:
    print(url)
=======
from bs4 import BeautifulSoup

# Legge il contenuto del file HTML
with open("facebook_tfa_sostegno.html", "r", encoding="utf-8") as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, "html.parser")

# Trova tutti i tag <a> che contengono "facebook.com/groups/" nell'attributo href
group_links = soup.find_all("a", href=lambda href: href and "facebook.com/groups/" in href)

# Stampiamo solo i link, filtrando eventuali duplicati se necessario
links = set()
for link in group_links:
    url = link.get("href")
    if url:
        links.add(url)

for url in links:
    print(url)
>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)
