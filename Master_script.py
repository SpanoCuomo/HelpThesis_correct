# master.py
import subprocess
import sys

# Lista degli script da eseguire, con percorso relativo o assoluto
scripts = [
    "Facebook_posts.py",
    "Storie_Facebook.py",
    "Storie_WA.py"
]

def run_scripts(scripts_list):
    for script in scripts_list:
        print(f"\n▶️ Eseguo {script}...")
        # Chiama l'interprete corrente (sys.executable) per garantire lo stesso ambiente
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        # Mostra stdout e stderr
        print("— STDOUT:")
        print(result.stdout or "(nessun output)")
        if result.stderr:
            print("— STDERR:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        # Controlla il codice di uscita
        if result.returncode != 0:
            print(f"⚠️ {script} è terminato con codice {result.returncode}. Interrompo la catena.", file=sys.stderr)
            sys.exit(result.returncode)
    print("\n✅ Tutti gli script sono stati eseguiti con successo!")

if __name__ == "__main__":
    run_scripts(scripts)
