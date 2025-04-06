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

<h1>Didattica digitale: risorse e strumenti online</h1>

<p>
  Con l’evoluzione delle tecnologie informatiche e l’ampliarsi delle reti globali,
  <strong>l’integrazione del digitale nella didattica</strong> è diventata una leva
  fondamentale per innovare i processi di insegnamento e apprendimento. Questo approccio
  consente di proporre <em>lezioni più interattive</em>, personalizzabili a seconda di
  stili di apprendimento e livelli di competenza differenti, mantenendo sempre vivo l’interesse
  degli studenti.
</p>

<h2>Perché puntare sul digitale?</h2>
<ul>
  <li><strong>Maggiore coinvolgimento:</strong> grazie a video, quiz interattivi, gamification 
      e simulazioni 3D, gli studenti diventano parte attiva del processo di apprendimento, 
      favorendo motivazione e spirito critico.</li>
  <li><strong>Flessibilità di fruizione:</strong> i materiali digitali, disponibili in 
      qualsiasi momento e da qualunque dispositivo, incentivano lo <em>studio autonomo</em> 
      e offrono possibilità di approfondimento personalizzate.</li>
  <li><strong>Collaborazione a distanza:</strong> attraverso piattaforme di e-learning 
      e strumenti di condivisione online, gli studenti possono <em>lavorare in team</em> 
      anche fuori dall’aula, sviluppando competenze digitali e relazionali.</li>
</ul>

<h2>Strumenti consigliati</h2>
<p>
  Il panorama delle tecnologie a supporto della didattica è ampio e in costante evoluzione.
  Tra le piattaforme più diffuse e apprezzate troviamo <strong>Google Workspace for Education</strong>, 
  <strong>Moodle</strong>, <strong>Edmodo</strong> e altre soluzioni gratuite o open-source.
  Ciascuna di queste offre ambienti virtuali per la gestione dei corsi, la condivisione di 
  materiali e la somministrazione di test.
</p>

<p>
  Oltre alle piattaforme strutturate, esistono innumerevoli risorse digitali: repository 
  di esercizi, videolezioni, <em>laboratori virtuali</em>, giochi didattici e strumenti 
  interattivi che facilitano la comprensione di concetti complessi. È sempre consigliabile
  valutare la validità didattica e l’accessibilità di queste risorse, in modo da creare
  percorsi formativi inclusivi.
</p>

<h2>Consigli per un utilizzo efficace</h2>
<ul>
  <li><strong>Obiettivi formativi chiari:</strong> definire con precisione le competenze 
      da raggiungere aiuta a selezionare tecnologie adeguate e a massimizzare il beneficio 
      per gli studenti.</li>
  <li><strong>Approccio graduale:</strong> introdurre gli strumenti digitali in modo 
      progressivo facilita l’adattamento e consente di valutare costantemente i risultati 
      ottenuti.</li>
  <li><strong>Formazione docente:</strong> una preparazione adeguata è essenziale per 
      sfruttare al meglio le potenzialità offerte dalle nuove tecnologie e proporre 
      attività didattiche efficaci.</li>
  <li><strong>Inclusività:</strong> considerare i diversi livelli di competenza digitale e 
      le specifiche esigenze degli studenti permette di garantire un apprendimento 
      equo ed efficace per tutti.</li>
</ul>

<p>
  Integrare il digitale nella didattica non significa <em>abbandonare i metodi tradizionali</em>,
  ma piuttosto arricchirli e renderli più flessibili. Il segreto è trovare il giusto
  equilibrio tra tecnologia e pedagogia, dedicando tempo e cura alla progettazione delle
  attività e alla verifica dei risultati.
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