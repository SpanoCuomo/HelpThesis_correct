<?php
// Includi l’elenco dei post e individua il post corrente
include('posts.php');

// Se non viene passato 'slug', usa il nome del file corrente
if (!isset($_GET['slug'])) {
  $currentSlug = basename(__FILE__);
} else {
  $currentSlug = $_GET['slug'];
}

// Trova l'indice del post corrente
$currentIndex = -1;
foreach ($posts as $i => $post) {
  if ($post['slug'] === $currentSlug) {
    $currentIndex = $i;
    break;
  }
}
if ($currentIndex === -1) {
  echo "Post non trovato.";
  exit;
}

// Salva il post corrente in una variabile dedicata
$currentPost = $posts[$currentIndex];

// Calcola l'indice dell'articolo precedente e successivo (navigazione circolare)
$total = count($posts);
$prevIndex = ($currentIndex - 1 + $total) % $total;
$nextIndex = ($currentIndex + 1) % $total;

// Avvia l'output buffering per catturare il contenuto specifico della pagina
ob_start();
?>


<script>!function(d,l,e,s,c){e=d.createElement("script");e.src="//ad.altervista.org/js.ad/size=728X90/?ref="+encodeURIComponent(l.hostname+l.pathname)+"&r="+Date.now();s=d.scripts;c=d.currentScript||s[s.length-1];c.parentNode.insertBefore(e,c)}(document,location)</script>



<h1>Project-Based Learning: imparare progettando</h1>

<p>
  Il <strong>Project-Based Learning (PBL)</strong> è una metodologia didattica che vede
  gli studenti impegnati nella <em>realizzazione concreta di un progetto</em>. L'idea di fondo
  è che la conoscenza si costruisca meglio quando viene utilizzata per risolvere problemi
  reali o per creare prodotti tangibili. Gli studenti, lavorando in modo cooperativo o
  collaborativo, diventano protagonisti del processo, mentre l’insegnante si trasforma
  in <strong>facilitatore</strong> e guida.
</p>

<h2>Perché scegliere il PBL</h2>
<ul>
  <li>
    <strong>Apprendimento attivo:</strong> gli studenti sperimentano, ricercano
    informazioni, prendono decisioni e mettono in pratica ciò che hanno appreso,
    sviluppando spirito critico e autonomia.
  </li>
  <li>
    <strong>Coinvolgimento e motivazione:</strong> avere un obiettivo concreto,
    come la creazione di un prototipo o la risoluzione di un problema sociale,
    aumenta la motivazione e la partecipazione.
  </li>
  <li>
    <strong>Integrazione di competenze:</strong> nel PBL, spesso, si lavora
    su progetti multidisciplinari che uniscono più aree (scienze, lettere,
    tecnologie, arte), offrendo una visione d’insieme.
  </li>
  <li>
    <strong>Sviluppo di soft skill:</strong> collaborazione, problem solving,
    gestione del tempo, comunicazione e leadership diventano parte integrante
    del percorso.
  </li>
</ul>

<h2>Le fasi chiave del PBL</h2>
<ol>
  <li>
    <strong>Ideazione e definizione:</strong> si parte da una <em>domanda guida</em>
    o da un problema reale. È importante che sia sufficientemente complesso
    e stimolante da richiedere un lavoro approfondito.
  </li>
  <li>
    <strong>Pianificazione:</strong> il gruppo o la classe stabilisce obiettivi,
    risorse, ruoli, tempistiche. Questa fase include la suddivisione dei compiti
    e la definizione di eventuali sotto-progetti.
  </li>
  <li>
    <strong>Sviluppo del progetto:</strong> gli studenti raccolgono informazioni,
    formulano ipotesi, realizzano materiali, sperimentano e <em>rivedono</em>
    in base ai risultati ottenuti (cicli di prova e correzione).
  </li>
  <li>
    <strong>Presentazione:</strong> si espone il lavoro finale (un prodotto,
    una relazione, una rappresentazione, un video) di fronte alla classe,
    ad altri docenti o addirittura a una platea esterna.
  </li>
  <li>
    <strong>Valutazione e riflessione:</strong> oltre a valutare il risultato,
    si analizza il processo. Cosa ha funzionato? Cosa si può migliorare?
    Quali competenze sono state effettivamente acquisite?
  </li>
</ol>

<h2>Come progettare un’esperienza di PBL efficace</h2>
<ul>
  <li>
    <strong>Definire obiettivi chiari:</strong> individua quali competenze
    disciplinari e trasversali vuoi far sviluppare, tenendo conto dei livelli
    di partenza della classe.
  </li>
  <li>
    <strong>Organizzare gruppi di lavoro:</strong> alterna momenti di lavoro
    individuale e di gruppo, in modo che ognuno possa contribuire secondo
    le proprie abilità.
  </li>
  <li>
    <strong>Prevedere check-point:</strong> stabilisci “tappe intermedie”
    in cui verificare i progressi, fornire feedback e aggiustare la rotta
    se necessario.
  </li>
  <li>
    <strong>Integrare strumenti digitali:</strong> piattaforme come Trello,
    Google Workspace o strumenti di condivisione (padlet, bacheche virtuali)
    semplificano la collaborazione e il monitoraggio del progetto.
  </li>
</ul>

<h2>Valutazione e feedback</h2>
<p>
  Nel <strong>Project-Based Learning</strong>, la valutazione non riguarda solo
  il prodotto finale, ma anche (e soprattutto) il <em>processo</em> e i <em>ruoli</em>
  assunti dai singoli durante il percorso. Per farlo, si possono utilizzare:
</p>
<ul>
  <li>
    <strong>Rubriche:</strong> griglie di valutazione che includano criteri come
    originalità, approfondimento, collaborazione, comunicazione, problem solving.
  </li>
  <li>
    <strong>Auto e peer evaluation:</strong> momenti in cui gli studenti valutano
    il proprio contributo e quello dei compagni, imparando a dare e ricevere
    feedback costruttivi.
  </li>
  <li>
    <strong>Diario di bordo:</strong> un documento (cartaceo o digitale) in cui
    gli studenti annotano sfide, riflessioni, idee e tappe importanti dello sviluppo
    del progetto.
  </li>
</ul>

<h2>Conclusioni</h2>
<p>
  L’<strong>apprendimento basato su progetti</strong> trasforma la classe in un
  “<em>cantiere di idee</em>” dove la teoria diventa pratica e la collaborazione
  diventa l’ingrediente fondamentale per raggiungere obiettivi condivisi.
  Grazie al PBL, si sviluppano competenze solide e durature, perché costruite
  su un <em>fare consapevole</em> e su una costante riflessione collettiva.
</p>































































<!-- Sezione "Altri articoli del nostro Blog" (dinamica) -->
<div class="blog-intro">
  <h2>Altri articoli del nostro Blog</h2>
  <p>
    Se ti è piaciuto questo contenuto, potresti trovare interessanti altri articoli dedicati ad argomenti simili.
  </p>
</div>



<div class="blog-list">
  <!-- Articolo precedente -->
  <article class="blog-card">
    <h3><?php echo $posts[$prevIndex]['title']; ?></h3>
    <p><?php echo $posts[$prevIndex]['summary']; ?></p>
    <a href="/blog/<?php echo $posts[$prevIndex]['slug']; ?>?slug=<?php echo $posts[$prevIndex]['slug']; ?>" class="btn-servizio">
      Leggi l'articolo
    </a>
  </article>

  <!-- Articolo successivo -->
  <article class="blog-card">
    <h3><?php echo $posts[$nextIndex]['title']; ?></h3>
    <p><?php echo $posts[$nextIndex]['summary']; ?></p>
    <a href="/blog/<?php echo $posts[$nextIndex]['slug']; ?>?slug=<?php echo $posts[$nextIndex]['slug']; ?>" class="btn-servizio">
      Leggi l'articolo
    </a>
  </article>
</div>



<br>


<h5>Il nostro team offre consulenza nella redazione di lavori per concorso, corsi 30/60 CFU e TFA.</h5> 
<p>Puoi contattarci gratuitamente al  <a href="tel:3780608777"><strong>378-060-8777</strong></a>, anche tramite <a href="https://wa.me/3780608777" target="_blank"> <strong>WA</strong></a>.</p>
<h5>  <a href="https://aiutotesi.altervista.org/uda.html#target_esterno">Oppure puoi acquistare il nostro libro, disponibile nella Home</a>

</h5>



<!-- Pulsante per tornare alla Home -->
<div style="text-align:center; margin-top: 2rem;">
  <a href="/uda.html" class="btn-back">Torna alla Home</a>
</div>







<?php
// Cattura il contenuto specifico nel buffer
$content = ob_get_clean();

// Definisci le variabili per meta tag e titolo relative al post corrente
$title          = $currentPost['title'];
$og_title       = $currentPost['title'];
$og_description = $currentPost['summary'];
$og_image       = $currentPost['image'];

// Includi il template base e renderizza la pagina
require 'base_blog.php';
renderTemplate($title, $og_title, $og_description, $og_image, $content);
?>