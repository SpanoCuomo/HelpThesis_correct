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

<h1>CLIL: apprendimento integrato di lingua e contenuti</h1>
<h2>CLIL (Content and Language Integrated Learning)</h2>

<p>
  Il <strong>CLIL</strong> (<em>Content and Language Integrated Learning</em>) è un
  approccio didattico che prevede l’insegnamento di una materia non linguistica
  (come scienze, storia o matematica) <em>direttamente in lingua straniera</em>.
  L’obiettivo è <strong>integrare</strong> l’apprendimento linguistico con quello
  disciplinare, creando un contesto di studio più motivante e vicino alla realtà.
</p>

<p>
  Questo metodo nasce dall’idea che la lingua si impari meglio quando viene utilizzata
  in situazioni autentiche: per esempio, studiare la storia in inglese permette allo
  studente di apprendere sia i contenuti storici, sia il lessico specifico e le strutture
  linguistiche in modo naturale.
</p>

<h2>Perché adottare il CLIL</h2>
<ul>
  <li><strong>Autenticità:</strong> gli studenti apprendono la lingua in situazioni
      concrete, direttamente legate alle discipline scolastiche.</li>
  <li><strong>Aumento della motivazione:</strong> l’uso della lingua straniera per
      esplorare argomenti reali crea maggiore coinvolgimento.</li>
  <li><strong>Maggiore autonomia:</strong> gli studenti sviluppano capacità di ricerca
      e consultazione di fonti in lingua, imparando a gestire in modo attivo le
      informazioni.</li>
  <li><strong>Competenze trasversali:</strong> si potenziano abilità di <em>problem solving</em>,
      pensiero critico e collaborazione, essenziali nel mondo del lavoro.</li>
</ul>

<h2>Consigli pratici</h2>
<p>
  <strong>1. Inizia con argomenti semplici:</strong><br>
  Se è la tua prima esperienza CLIL, scegli temi familiari ai tuoi studenti. In questo
  modo, la complessità contenutistica e quella linguistica rimangono gestibili.
</p>
<p>
  <strong>2. Utilizza materiali calibrati sul livello degli studenti:</strong><br>
  Testi, video e risorse digitali dovrebbero essere adeguati alle competenze linguistiche
  della classe. L’uso di schemi, mappe concettuali, immagini e glossari di termini chiave
  può risultare molto utile.
</p>
<p>
  <strong>3. Fai ricorso al “supporto” (scaffolding):</strong><br>
  Guida progressivamente gli studenti verso la comprensione del testo e l’uso autonomo
  della lingua. Puoi, per esempio, fornire esempi pratici, esercizi guidati, attività
  cooperative e momenti di riflessione metalinguistica.
</p>
<p>
  <strong>4. Incoraggia l’uso attivo della lingua:</strong><br>
  Prevedi discussioni in piccoli gruppi, lavori di ricerca o progetti multimediali in cui
  i ragazzi possano sperimentare la lingua in modo attivo e creativo.
</p>

<h2>Benefici a lungo termine</h2>
<p>
  L’esperienza CLIL, oltre a rafforzare le competenze linguistiche, permette di coltivare
  una <strong>mentalità aperta e internazionale</strong>. Gli studenti sviluppano
  flessibilità cognitiva e la capacità di affrontare problemi complessi in più lingue,
  competenza sempre più richiesta in ambito accademico e professionale.
</p>

<h2>Prospettive e approfondimenti</h2>
<p>
  L’approccio CLIL non si limita alle scuole superiori: sta diventando sempre più diffuso
  anche nella scuola primaria e, in alcuni casi, in ambito universitario. Se desideri
  esplorare ulteriormente questa metodologia, puoi consultare le <em>Linee Guida CLIL</em>
  del tuo Ministero dell’Istruzione o cercare corsi di formazione dedicati. Esistono
  inoltre numerose <strong>comunità di pratica online</strong> (forum, gruppi sui social,
  piattaforme didattiche) dove condividere esperienze e materiali.
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