<?php
// Avvia l'output buffering per catturare il contenuto specifico della pagina
ob_start();
?>

<div class="container">
  <header class="blog-header">
    <h1>Come inserire la bibliografia nel testo</h1>
    <p class="text-muted">Linee guida per citare correttamente le fonti all’interno della tua tesi.</p>
  </header>
  
  <article class="blog-content">
    <p>
      Una delle difficoltà più frequenti per chi scrive la tesi riguarda la modalità corretta per citare le fonti all’interno del testo. Esistono vari stili bibliografici, ognuno con le sue regole specifiche. Vediamo insieme i passaggi fondamentali per evitare errori di forma e di sostanza.
    </p>
    
    <h5>1. Scegli (o verifica) lo stile richiesto</h5>
    <p>
      In primo luogo, controlla se il tuo corso di laurea o il tuo relatore ha indicato uno <em>stile di citazione</em> preciso (APA, Chicago, MLA, Vancouver…). Ogni stile prevede una sintassi propria per i riferimenti nel testo e per la formattazione della bibliografia finale.
    </p>
    
    <h5>2. Citazioni dirette e indirette</h5>
    <ul>
      <li>
        <strong>Citazione diretta</strong>: quando riporti fedelmente le parole di un autore, metti il testo tra virgolette o in blocco separato se è più lungo di alcune righe. Ad esempio, in APA si indica tra parentesi (Cognome, Anno, p. xx).
      </li>
      <li>
        <strong>Citazione indiretta</strong>: quando parafrasi un concetto, devi comunque indicare l’autore e l’anno (o altra informazione) secondo lo stile scelto.
      </li>
    </ul>
    
    <h5>3. Esempi pratici in diversi stili</h5>
    <p><strong>Stile APA (American Psychological Association)</strong></p>
    <p>
      <em>Nel testo:</em> (Rossi, 2020) oppure Rossi (2020) afferma che...<br>
      <em>Nella bibliografia:</em> Rossi, G. (2020). <em>Il titolo del libro</em>. Editore.
    </p>
    <p><strong>Stile MLA (Modern Language Association)</strong></p>
    <p>
      <em>Nel testo:</em> (Rossi 45).<br>
      <em>Nella bibliografia:</em> Rossi, Giovanni. <em>Il titolo del libro</em>. Editore, 2020.
    </p>
    
    <h5>4. Usare un software di gestione bibliografica</h5>
    <p>
      Per semplificare la gestione delle citazioni e della bibliografia finale, programmi come <em>Zotero</em>, <em>Mendeley</em> o <em>EndNote</em> permettono di inserire le fonti nel testo con un click e di generare automaticamente la bibliografia secondo lo stile richiesto.
    </p>
    
    <h5>5. Evita il plagio</h5>
    <p>
      Ricorda di indicare sempre le tue fonti. Anche quando parafrasi, inserisci una citazione (o una nota) che rimandi alla bibliografia. Copiare intere frasi senza virgolette e senza riferimenti è un grave errore e può compromettere l’esito della tesi.
    </p>
    
    <p>
      Impostare correttamente le citazioni è un gesto di serietà accademica e rispetto per il lavoro altrui. Con un po’ di pratica e gli strumenti giusti, diventa un’operazione semplice e veloce.
    </p>
  </article>

  <!-- Elenco articoli in anteprima -->
  <div class="blog-list" style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">
    <!-- Articolo 1 -->
    <article class="blog-card" style="
      background-color: #f9f9f9;
      padding: 1.5rem;
      border-radius: 8px;
      border: 1px solid #eee;
      max-width: 350px;
      flex: 1 1 calc(33.333% - 1rem);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      text-align: left;
      cursor: pointer;
    ">
      <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem; color: #333;">
        Come creare l'indice di una tesi
      </h3>
      <p style="font-size: 1rem; color: #555; margin-bottom: 1rem;">
        L’indice di una tesi non è un semplice elenco di titoli, ma costituisce la mappa concettuale del tuo elaborato...
      </p>
      <a href="/blog_tesi/blog_1_creare_indice.php" class="btn-servizio">
        Leggi l'articolo
      </a>
    </article>

    <!-- Articolo 2 -->
    <article class="blog-card" style="
      background-color: #f9f9f9;
      padding: 1.5rem;
      border-radius: 8px;
      border: 1px solid #eee;
      max-width: 350px;
      flex: 1 1 calc(33.333% - 1rem);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      text-align: left;
      cursor: pointer;
    ">
      <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem; color: #333;">
        Come creare la bibliografia e da dove cercarla
      </h3>
      <p style="font-size: 1rem; color: #555; margin-bottom: 1rem;">
        Strategie e risorse per una bibliografia solida e affidabile...
      </p>
      <a href="/blog_tesi/blog_2_bibliografia_fonti.php" class="btn-servizio">
        Leggi l'articolo
      </a>
    </article>
  </div>

  <!-- Pulsante per tornare alla Home -->
  <div style="text-align:center; margin-top: 2rem;">
    <a href="/tesi-di-laurea.html" class="btn-back">Torna alla Home</a>
  </div>
</div>













<?php
// Cattura il contenuto specifico nel buffer
$content = ob_get_clean();

// Definisci le variabili per meta tag e titolo
$title          = "Blog - Come preparare un'UDA vincente";
$og_title       = $title;
$og_description = "Una UDA vincente nasce dalla perfetta sinergia tra obiettivi formativi chiari, metodi didattici ben strutturati e strategie di valutazione efficaci. L’UDA guida lo studente verso competenze trasversali e disciplinari.";
$og_image       = "https://aiutotesi.altervista.org/blog/UDA_blog_2.PNG";

// Includi il template base e renderizza la pagina
require 'base_blog.php';
renderTemplate($title, $og_title, $og_description, $og_image, $content);
?>
