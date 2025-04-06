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

<h1>Flipped Classroom: come capovolgere la lezione tradizionale</h1>

<p>
  La <strong>Flipped Classroom</strong>, o <em>classe capovolta</em>, è una metodologia che ribalta
  il tradizionale schema “spiegazione in classe ed esercizi a casa”. Invece di ascoltare la
  lezione passivamente, gli studenti studiano i contenuti teorici a casa (attraverso
  video, letture, podcast, slide interattive) e in classe si concentrano su attività
  pratiche, laboratori e momenti di confronto.
</p>

<h2>Perché adottare la classe capovolta</h2>
<ul>
  <li>
    <strong>Maggiore partecipazione:</strong> il tempo in classe si trasforma in uno spazio
    di confronto e di apprendimento attivo: gli studenti elaborano idee, risolvono problemi
    in gruppo e fanno esperimenti.
  </li>
  <li>
    <strong>Apprendimento personalizzato:</strong> ogni studente può rivedere il materiale
    teorico secondo i propri ritmi e stili di apprendimento, sfruttando pause e riavvolgimenti
    nei video o nei contenuti digitali.
  </li>
  <li>
    <strong>Interazione più profonda in aula:</strong> liberando tempo dalla lezione frontale,
    il docente può dedicarsi a seguire da vicino i singoli studenti, offrendo supporto mirato
    e correggendo eventuali fraintendimenti.
  </li>
</ul>

<h2>Come implementarla passo dopo passo</h2>
<ol>
  <li>
    <strong>Seleziona i contenuti:</strong> individua quali argomenti gli studenti
    possono affrontare a casa. Scegli materiali chiari e interattivi (video brevi,
    articoli, schede di sintesi).
  </li>
  <li>
    <strong>Prepara una guida:</strong> specifica agli studenti obiettivi e compiti
    relativi ai materiali da studiare. Puoi indicare domande guida, esercizi di
    autovalutazione o brevi quiz online.
  </li>
  <li>
    <strong>Progetta attività per la classe:</strong> dedica il tempo in aula a
    discussioni, simulazioni, laboratori o esercizi di gruppo. Crea situazioni in cui
    gli studenti siano protagonisti del proprio apprendimento.
  </li>
  <li>
    <strong>Monitora il processo:</strong> utilizza piccoli test, rubriche di valutazione
    o questionari per verificare quanto sia stato compreso a casa. Raccogli il
    feedback degli studenti per migliorare i contenuti o le modalità di fruizione.
  </li>
</ol>

<h2>Consigli pratici</h2>
<ul>
  <li>
    <strong>Varietà di risorse:</strong> cerca di proporre materiali multimediali
    diversi (video, testi, podcast, infografiche), così da coinvolgere vari stili
    di apprendimento e ridurre la noia.
  </li>
  <li>
    <strong>Organizzazione e chiarezza:</strong> fornisci una scaletta o un calendario
    con le date in cui verranno trattati i vari argomenti, evidenziando eventuali scadenze
    (es. quiz online da completare).
  </li>
  <li>
    <strong>Collaborazione fra docenti:</strong> se possibile, coordina la Flipped Classroom
    con altri insegnanti della stessa materia o di discipline affini. Creare un
    repository comune di risorse può semplificare il lavoro e arricchirlo di
    nuove prospettive.
  </li>
</ul>

<h2>Conclusioni</h2>
<p>
  La <strong>Flipped Classroom</strong> rappresenta un cambiamento culturale nel
  modo di insegnare e di apprendere. Trasforma la passività di una lezione frontale
  in un’esperienza didattica <em>centrata sullo studente</em>, che si sente più
  autonomo e coinvolto. La gestione del tempo in classe diventa più efficiente
  e, soprattutto, aumenta la qualità delle relazioni educative.
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