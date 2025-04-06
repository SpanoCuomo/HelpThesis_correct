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












<h1>Educazione socio-emotiva: competenze per crescere come persone</h1>

<p>
  L’<strong>Educazione Socio-Emotiva</strong> (chiamata anche SEL – Social Emotional Learning)
  rappresenta un insieme di pratiche didattiche e attività che mirano allo sviluppo
  integrale di ciascun studente, non solo sul piano cognitivo ma anche su quello
  <em>emotivo, relazionale e sociale</em>. È un approccio che mette al centro
  competenze come l’autoconsapevolezza, la gestione delle emozioni, l’empatia
  e la comunicazione efficace.
</p>

<h2>Perché è importante il SEL a scuola</h2>
<ul>
  <li>
    <strong>Benessere psicologico:</strong> aiutare i ragazzi a riconoscere e gestire
    le proprie emozioni riduce stress, ansia e problemi comportamentali.
  </li>
  <li>
    <strong>Miglioramento del clima di classe:</strong> relazioni positive e una
    comunicazione più empatica contribuiscono a creare un ambiente di apprendimento
    sereno e collaborativo.
  </li>
  <li>
    <strong>Risultati scolastici migliori:</strong> gli studi dimostrano che
    studenti emotivamente equilibrati e motivati ottengono performance accademiche
    più elevate.
  </li>
</ul>

<h2>I cinque pilastri del Social Emotional Learning</h2>
<ol>
  <li>
    <strong>Autoconsapevolezza:</strong> riconoscere il proprio bagaglio emotivo,
    i propri punti di forza e di debolezza, nonché i valori e le aspirazioni.
  </li>
  <li>
    <strong>Autogestione:</strong> saper regolare le emozioni, gestire lo stress,
    tenere a bada l’impulsività e perseverare di fronte alle difficoltà.
  </li>
  <li>
    <strong>Consapevolezza sociale:</strong> essere capaci di ascoltare l’altro,
    comprendere punti di vista diversi e mostrarsi empatici verso i bisogni
    altrui.
  </li>
  <li>
    <strong>Abilità relazionali:</strong> stabilire relazioni positive, comunicare
    in modo efficace e risolvere i conflitti in maniera costruttiva.
  </li>
  <li>
    <strong>Decisioni responsabili:</strong> compiere scelte etiche e ragionate,
    considerando conseguenze a breve e lungo termine sia su di sé sia sugli altri.
  </li>
</ol>

<h2>Come integrare il SEL in classe</h2>
<ul>
  <li>
    <strong>Momenti di discussione:</strong> introdurre brevi “cerchi di parola” all’inizio
    o alla fine della lezione, dove gli studenti possano esprimere pensieri, emozioni
    e riflessioni su tematiche personali o di attualità.
  </li>
  <li>
    <strong>Attività di gruppo e role play:</strong> simulazioni e giochi di ruolo
    che permettono di “allenare” la gestione delle emozioni e la cooperazione.
  </li>
  <li>
    <strong>Esercizi di mindfulness e rilassamento:</strong> semplici tecniche di
    respirazione, visualizzazione o consapevolezza corporea, per imparare a
    riconoscere e regolare le tensioni interne.
  </li>
  <li>
    <strong>Progetti di volontariato:</strong> iniziative solidali o di utilità
    sociale per sviluppare senso di responsabilità e cittadinanza attiva.
  </li>
</ul>

<h2>Il ruolo del docente</h2>
<p>
  L’insegnante diventa una guida e un modello di <em>comportamento emotivamente
  intelligente</em>. Mostrare empatia, ascoltare con attenzione, dare feedback
  costruttivi e gestire i conflitti in modo equilibrato sono esempi concreti
  che gli studenti interiorizzano e fanno propri. Inoltre, è fondamentale
  imparare a cogliere segnali di disagio negli alunni, per intervenire
  tempestivamente o segnalare le situazioni a chi di competenza.
</p>

<h2>Conclusioni</h2>
<p>
  Includere l’<strong>educazione socio-emotiva</strong> nel proprio piano di insegnamento
  non significa togliere spazio alle discipline, ma <em>valorizzare</em> il potenziale
  di ogni studente nella sua totalità. Le abilità socio-emotive apprese a scuola
  si riflettono nella vita quotidiana, contribuendo a formare persone più
  <strong>consapevoli</strong>, <strong>empatiche</strong> e in grado di costruire
  relazioni positive.
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