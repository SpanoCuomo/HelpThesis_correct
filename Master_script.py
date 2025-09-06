# master.py
import subprocess
import sys
from Storie_WA import invia_storie_whatsapp
import time
import datetime

# master.py
from Storie_Facebook import invia_storie_facebook
from Post_WA_3 import post_a_whatsapp
from Storie_Facebook import pubblica_unico_reel
# Ad esempio PC grande, arancione, 10 post, modalità auto (reel e storie alternate)
######post_a_whatsapp(pc_grande=True)
#invia_storie_facebook(pc_grande=True, arancione=True, numero_post=1, publish_mode="auto")
#invia_storie_facebook(pc_grande=True, arancione=False, numero_post=1, publish_mode="auto")

# Lista degli script da eseguire, con percorso relativo o assoluto
scripts = [
    "Facebook_posts.py",
    "Storie_Facebook.py",
    "Storie_WA.py"
]



# Configurazione intervallo (2 ore in secondi)
intervallo_ore = 0.2
intervallo_secondi = intervallo_ore * 60 * 60

# Numero di post per ogni esecuzione singola
numero_post_per_esecuzione = 1  

# PC utilizzato (True per grande, False per piccolo)
pc_grande = True

def invio_periodico():
    while True:
        ora_corrente = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🔔 [{ora_corrente}] Eseguo invio storie WhatsApp...")
        
        invia_storie_facebook(pc_id=1, page_id=1, numero_post=1,  publish_mode="auto")
        invia_storie_facebook(pc_id=1, page_id=2, numero_post=1,  publish_mode="auto")  
        
        pubblica_unico_reel(
            video_path="C://Users//UTENTE//Downloads//pubbli_libro.mp4",
            didascalia="Acquista il libro per la preparazione del test come assistente di cancelleria su Amazon, al https://amzn.eu/d/gvcef0E ",
            pc_id=1,     # PC grande
            page_id=3    # Mininterno (usa quello che ti serve: 1 Arancione, 2 Blu, 3 Mininterno)
            )
        pubblica_unico_reel(
            video_path="C://Users//UTENTE//Downloads//pubbli_libro.mp4",
            didascalia="Acquista il libro per la preparazione del test come assistente di cancelleria su Amazon, al https://amzn.eu/d/gvcef0E ",
            pc_id=1,     # PC grande
            page_id=1    # Mininterno (usa quello che ti serve: 1 Arancione, 2 Blu, 3 Mininterno)
            )
            
        pubblica_unico_reel(
            video_path="C://Users//UTENTE//Downloads//pubbli_libro.mp4",
            didascalia="Acquista il libro per la preparazione del test come assistente di cancelleria su Amazon, al https://amzn.eu/d/gvcef0E ",
            pc_id=1,     # PC grande
            page_id=2    # Mininterno (usa quello che ti serve: 1 Arancione, 2 Blu, 3 Mininterno)
            )
        #invia_storie_whatsapp(pc_grande=pc_grande, numero_post=numero_post_per_esecuzione)
        try:
            
            print(f"✅ Storia inviata con successo alle {ora_corrente}!\n")
        except Exception as e:
            print(f"⚠️ Errore durante l'invio storie: {e}\n")
        
        # Attendi per l'intervallo stabilito (2 ore)
        print(f"⏳ Aspetto {intervallo_ore} ore prima del prossimo invio...\n")
        time.sleep(intervallo_secondi)

if __name__ == "__main__":
    
    invio_periodico()

# def run_scripts(scripts_list):
#     for script in scripts_list:
#         print(f"\n▶️ Eseguo {script}...")
#         # Chiama l'interprete corrente (sys.executable) per garantire lo stesso ambiente
#         result = subprocess.run([sys.executable, script], capture_output=True, text=True)
#         # Mostra stdout e stderr
#         print("— STDOUT:")
#         print(result.stdout or "(nessun output)")
#         if result.stderr:
#             print("— STDERR:", file=sys.stderr)
#             print(result.stderr, file=sys.stderr)
#         # Controlla il codice di uscita
#         if result.returncode != 0:
#             print(f"⚠️ {script} è terminato con codice {result.returncode}. Interrompo la catena.", file=sys.stderr)
#             sys.exit(result.returncode)
#     print("\n✅ Tutti gli script sono stati eseguiti con successo!")

# if __name__ == "__main__":
#     run_scripts(scripts)
