# Prova-Codex

Questo repository contiene un semplice videogioco 3D stile Frogger sviluppato per il browser.

## Gioco Frogger 3D

Il codice si trova nella cartella `frogger3d` ed è composto dai seguenti file:

- `index.html`: pagina principale del gioco. Include Three.js tramite CDN.
- `styles.css`: semplici stili per la pagina.
- `main.js`: logica del gioco.

Nella versione attuale la rana e le auto non sono più semplici geometrie
cubiche: sono composte da piccoli modelli 3D realizzati con le primitive di
Three.js per rendere il gioco più realistico.

Il gioco memorizza inoltre i punteggi migliori (fino a cinque) nel browser e
aggiunge ostacoli ogni tre attraversamenti riusciti.

Per provare il gioco è sufficiente aprire `frogger3d/index.html` con un browser moderno e utilizzare le frecce della tastiera per muovere la rana.
