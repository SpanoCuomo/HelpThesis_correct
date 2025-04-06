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



<h1>Valutazione autentica nelle UDA</h1>

<p>
  La <strong>valutazione autentica</strong> rappresenta il cuore di una UDA efficace, poiché
  consente di verificare le reali competenze degli studenti attraverso compiti in
  situazioni vicine alla realtà. In questo modo, la valutazione diventa un momento di
  crescita e di riflessione, anziché un mero giudizio basato su test standardizzati o
  verifiche tradizionali.
</p>

<h2>Perché puntare alla valutazione autentica</h2>
<ul>
  <li>
    <strong>Coinvolgimento:</strong> i compiti pratici, ancorati a contesti reali, stimolano
    la partecipazione attiva e la motivazione degli studenti.
  </li>
  <li>
    <strong>Competenze trasversali:</strong> lavorare su casi di studio, simulazioni o
    progetti permette di sviluppare abilità come il problem solving, la collaborazione
    e la riflessione critica.
  </li>
  <li>
    <strong>Rilevanza:</strong> gli studenti percepiscono l’utilità immediata di quanto
    imparano, favorendo un apprendimento più profondo e duraturo.
  </li>
</ul>

<h2>Strumenti chiave</h2>

<h3>Prove pratiche</h3>
<p>
  Le <strong>prove pratiche</strong> consentono di valutare le competenze in azione:
  ad esempio, un esperimento di laboratorio, la realizzazione di un prototipo, una
  presentazione orale o la gestione di un progetto di gruppo. È essenziale definire
  con chiarezza le aspettative, così che gli studenti sappiano esattamente cosa fare
  e come farlo.
</p>

<h3>Rubriche di valutazione</h3>
<p>
  Le <strong>rubriche</strong> sono griglie di osservazione che descrivono i livelli
  di performance attesi per ciascun criterio di valutazione. L’obiettivo è rendere
  trasparente il processo valutativo, in modo che lo studente capisca dove si trova
  e come può migliorare. Le rubriche devono essere:
</p>
<ul>
  <li>
    <em>Chiare:</em> i descrittori devono essere comprensibili e legati a indicatori
    osservabili.
  </li>
  <li>
    <em>Coerenti:</em> i livelli di competenza devono seguire una progressione logica,
    dal base all’eccellenza.
  </li>
  <li>
    <em>Condivise:</em> gli studenti dovrebbero avere accesso alle rubriche fin dall’inizio
    dell’attività, per orientare il proprio lavoro.
  </li>
</ul>

<h3>Compiti autentici</h3>
<p>
  I <strong>compiti autentici</strong> sono sfide didattiche che riproducono situazioni
  verosimili del mondo reale. Ad esempio, chiedere agli studenti di elaborare un progetto
  per migliorare un aspetto del quartiere, realizzare un reportage fotografico o gestire
  una campagna di sensibilizzazione. Questo tipo di compito spinge gli studenti a mettere
  in pratica conoscenze e abilità, consentendo di verificare realmente il livello di
  competenza acquisito.
</p>

<h3>Feedback formativo</h3>
<p>
  Il <strong>feedback formativo</strong> va oltre il voto: deve essere puntuale, continuo
  e orientato al miglioramento. Ecco alcune caratteristiche fondamentali:
</p>
<ul>
  <li>
    <strong>Specifico:</strong> lo studente deve capire esattamente in cosa ha brillato
    e dove può migliorare.
  </li>
  <li>
    <strong>Tempestivo:</strong> fornito il prima possibile, quando l’esperienza è ancora
    fresca nella mente.
  </li>
  <li>
    <strong>Riflessivo:</strong> lo studente deve poter rivedere, rielaborare e, se
    possibile, ripetere la prova per progredire.
  </li>
</ul>

<h2>Organizzare la valutazione nelle UDA</h2>
<p>
  L’organizzazione di <em>prove pratiche, rubriche, compiti autentici</em> e
  <em>feedback formativo</em> nella progettazione di un’Unità Didattica di Apprendimento
  (UDA) richiede un’attenta pianificazione:
</p>
<ul>
  <li>
    <strong>Parti dagli obiettivi di competenza:</strong> definisci quali traguardi
    formativi vuoi che gli studenti raggiungano.
  </li>
  <li>
    <strong>Pianifica i compiti autentici:</strong> valuta le risorse disponibili,
    i tempi e i possibili ostacoli logistici. Immagina situazioni realistiche e
    coinvolgenti per gli studenti.
  </li>
  <li>
    <strong>Costruisci le rubriche di valutazione:</strong> assegna criteri e livelli
    chiari e condividili con gli studenti prima di iniziare l’attività.
  </li>
  <li>
    <strong>Prevedi momenti di feedback:</strong> integra sessioni di revisione, auto-
    e peer-assessment, in cui gli studenti possano mettersi in discussione e imparare
    dagli errori.
  </li>
</ul>

<h2>Vantaggi per studenti e docenti</h2>
<p>
  La valutazione autentica offre benefici concreti:
</p>
<ul>
  <li>
    <strong>Per gli studenti:</strong> promuove l’autonomia, la presa di decisioni e
    il senso di responsabilità; li motiva perché vedono subito l’utilità di ciò che fanno.
  </li>
  <li>
    <strong>Per i docenti:</strong> fornisce dati più ricchi e qualitativi sui progressi
    reali degli studenti, aiutando a personalizzare i percorsi e a individuare eventuali
    difficoltà in tempo utile.
  </li>
</ul>

<p>
  In definitiva, la <strong>valutazione autentica</strong> all’interno delle UDA rappresenta
  uno strumento potente per allineare l’insegnamento alle esigenze e alle potenzialità
  di ogni studente, rendendo l’apprendimento significativo e realmente formativo.
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