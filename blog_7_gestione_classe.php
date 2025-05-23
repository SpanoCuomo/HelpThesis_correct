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

<h1>Gestione della classe</h1>



<p>
  Una <strong>buona gestione della classe</strong> è fondamentale per garantire un ambiente
  di apprendimento sereno, collaborativo e produttivo. Organizzare spazi, tempi e relazioni
  interpersonali in modo efficace aiuta a <em>minimizzare le distrazioni</em> e a favorire
  il rispetto reciproco, supportando al meglio il percorso di ogni studente.
</p>

<h2>Elementi chiave</h2>
<ul>
  <li>
    <strong>Regole condivise:</strong> definire poche regole chiare, costruite insieme
    alla classe. Quando gli studenti partecipano alla definizione di aspettative e
    comportamenti, si sentono più responsabilizzati.
  </li>
  <li>
    <strong>Routine:</strong> creare abitudini all’inizio o alla fine della lezione
    (saluti, controllo presenze, sintesi o recap finale) che diano punti di riferimento
    agli studenti, riducendo l’ansia e favorendo la concentrazione.
  </li>
  <li>
    <strong>Piano B:</strong> avere sempre un’attività alternativa nel caso in cui
    qualcosa non funzioni come previsto o se alcuni alunni terminano in anticipo, evitando
    momenti di vuoto che possono generare confusione.
  </li>
  <li>
    <strong>Spazi ben organizzati:</strong> predisporre l’aula in modo che tutti gli
    studenti possano vedere e sentirsi visti (es. disposizione a ferro di cavallo o
    tavoli per lavori di gruppo). Un ambiente fisico accogliente rende la classe
    più vivibile e inclusiva.
  </li>
</ul>

<h2>Strategie di comunicazione</h2>
<p>
  Una comunicazione efficace è alla base della gestione della classe. Parlare in modo
  chiaro e <strong>calmo</strong>, guardare gli studenti negli occhi e mostrare
  <strong>empatia</strong> nei confronti delle loro difficoltà aiutano a creare un
  clima di fiducia. Evita il sarcasmo e cerca di offrire <strong>feedback
  costruttivo</strong>, valorizzando i progressi e suggerendo come migliorare.
</p>

<p>
  Al contempo, è importante <em>intervenire tempestivamente</em> su comportamenti
  inadeguati in modo fermo ma rispettoso, spiegando le conseguenze delle azioni e
  mantenendo sempre un approccio educativo. In questo modo, si aiuta la classe a
  comprendere le dinamiche di gruppo e il valore delle regole.
</p>

<h2>Promuovere un clima positivo</h2>
<ul>
  <li>
    <strong>Rinforzi positivi:</strong> premiare i progressi, anche piccoli, contribuisce
    a migliorare la sicurezza e la motivazione degli studenti.
  </li>
  <li>
    <strong>Collaborazione:</strong> favorire attività di gruppo e progetti collaborativi
    permette di responsabilizzare gli studenti e insegnare il rispetto reciproco.
  </li>
  <li>
    <strong>Ascolto attivo:</strong> dedicare tempo all’ascolto delle proposte e delle
    problematiche della classe crea un senso di appartenenza e aiuta a prevenire i conflitti.
  </li>
</ul>

<h2>Gestire i conflitti</h2>
<p>
  I conflitti, se affrontati in modo costruttivo, possono diventare
  <strong>opportunità di crescita</strong> sia per i singoli che per l’intero gruppo. Alcuni
  suggerimenti:
</p>
<ul>
  <li>
    Mantieni <strong>la calma</strong> e offri a chi è coinvolto la possibilità di
    spiegarsi senza interruzioni.
  </li>
  <li>
    Attua <strong>soluzioni negoziate</strong>: guidare gli studenti a trovare un punto
    d’incontro, sviluppando competenze di problem solving e rispetto reciproco.
  </li>
  <li>
    Se necessario, fissa un colloquio individuale o in piccoli gruppi per chiarire
    malintesi o tensioni.
  </li>
</ul>

<h2>Benefici di una classe ben gestita</h2>
<p>
  Con una corretta gestione della classe, <strong>la didattica diventa più efficace</strong>.
  Gli studenti si sentono tutelati, coinvolti e pronti a imparare, mentre l’insegnante può
  dedicare più tempo alle spiegazioni e meno a “spegnere incendi” o ristabilire l’ordine.
</p>
<p>
  In un ambiente positivo e strutturato, inoltre, gli studenti sono più propensi ad
  assumersi responsabilità, sviluppare competenze trasversali (come l’autonomia e
  la collaborazione) e partecipare in modo proattivo alle lezioni.
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