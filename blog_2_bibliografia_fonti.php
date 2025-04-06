<?php
// Avvia l'output buffering per catturare il contenuto specifico della pagina
ob_start();
?>

<div class="container">
  <header class="blog-header">
    <h1>Come creare la bibliografia e da dove cercarla</h1>
    <p class="text-muted">Strategie e risorse per una bibliografia solida e affidabile.</p>
  </header>
  
  <article class="blog-content">
    <p>
      La bibliografia è uno degli elementi fondamentali di ogni tesi, perché testimonia la solidità delle tue fonti e garantisce la correttezza del lavoro accademico. In questa guida vedremo <strong>come individuare fonti valide</strong> e <strong>come impostare una bibliografia ben strutturata</strong>, in modo da rendere la tua tesi più autorevole e facilitare la consultazione da parte di chi la legge.
    </p>
    
    <h5>1. Definire il campo di ricerca</h5>
    <p>
      Prima ancora di cercare le fonti, chiarisci i confini del tuo argomento: quali sono i temi centrali che vuoi approfondire e quali quelli marginali? Un buon inquadramento ti aiuterà a <strong>identificare le parole chiave</strong> e a impostare query di ricerca mirate su banche dati e motori di ricerca scientifici, evitando dispersioni inutili.
      <br><em>Consiglio pratico</em>: annota su un foglio o in un file apposito gli obiettivi principali e le domande di ricerca che vuoi esplorare, così da restare focalizzato durante la ricerca.
    </p>
    
    <h5>2. Dove cercare le fonti</h5>
    <p>
      Le fonti di qualità non si trovano solo con una semplice ricerca su Google. Ecco alcuni luoghi (digitali e non) dove puoi iniziare la tua indagine:
    </p>
    <ul>
      <li><strong>Biblioteche universitarie</strong>: sfrutta i cataloghi interni e le banche dati specializzate.</li>
      <li><strong>Cataloghi online</strong> (es. WorldCat): per scoprire libri e articoli in biblioteche di tutto il mondo.</li>
      <li><strong>Database e riviste scientifiche</strong> come JSTOR, Scopus, Google Scholar.</li>
      <li><strong>Siti istituzionali</strong> e report ufficiali: utili per ottenere dati e linee guida di qualità.</li>
    </ul>
    
    <h5>3. Selezionare fonti affidabili</h5>
    <p>
      Non tutte le fonti trovate online sono attendibili. Valuta:
    </p>
    <ul>
      <li><strong>Peer review</strong>: le pubblicazioni riviste da altri esperti.</li>
      <li><strong>Autore e affiliazione</strong>: informazioni sull'autore e l'ente di appartenenza.</li>
      <li><strong>Anno di pubblicazione</strong>: l'attualità della fonte rispetto al tema.</li>
    </ul>
    
    <h5>4. Tipologie di fonti</h5>
    <p>
      Una bibliografia completa include libri, articoli di riviste, saggi, documenti online e tesi precedenti.
    </p>
    
    <h5>5. Strutturare la bibliografia</h5>
    <p>
      Segui le linee guida del tuo ateneo (APA, MLA, Chicago, ecc.) e, se possibile, utilizza software di gestione bibliografica come Zotero o Mendeley per automatizzare le citazioni.
    </p>
    
    <h5>6. Perché investire tempo nella bibliografia?</h5>
    <p>
      Una bibliografia ben organizzata aggiunge valore al tuo lavoro, dimostrando rigore e approfondimento nella ricerca.
    </p>
  </article>
  
  <!-- Elenco articoli in anteprima -->
  <div class="blog-list" style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">
    <!-- Articolo 1 -->
    <article class="blog-card">
      <h3>Come creare l'indice di una tesi</h3>
      <p>
        L’indice di una tesi non è un semplice elenco di titoli, ma costituisce la mappa concettuale del tuo elaborato...
      </p>
      <a href="/blog_tesi/blog_1_creare_indice.php" class="btn-servizio">
        Leggi l'articolo
      </a>
    </article>
    <!-- Articolo 2 -->
    <article class="blog-card">
      <h3>Come inserire la bibliografia nel testo</h3>
      <p>
        Linee guida per citare correttamente le fonti all’interno della tua tesi...
      </p>
      <a href="/blog_tesi/blog_3_inserire_bibliografia_testo.php" class="btn-servizio">
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
$title          = "Blog - Fonti Bibliografiche: Suggerimenti Pratici";
$og_title       = $title;
$og_description = "Scopri i migliori suggerimenti pratici per creare una bibliografia solida e affidabile per la tua tesi.";
$og_image       = "https://aiutotesi.altervista.org/blog_tesi/tesi_blog_2.png";

// Includi il template base e renderizza la pagina
require 'base_blog.php';
renderTemplate($title, $og_title, $og_description, $og_image, $content);
?>
