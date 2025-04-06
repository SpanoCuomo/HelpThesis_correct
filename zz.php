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

// Calcola l'indice dell'articolo precedente e successivo (navigazione circolare)
$total = count($posts);
$prevIndex = ($currentIndex - 1 + $total) % $total;
$nextIndex = ($currentIndex + 1) % $total;

// Avvia l'output buffering per catturare il contenuto specifico della pagina
ob_start();
?>

<h1>Come preparare un’UDA vincente</h1>

<p>
  Una <strong>UDA vincente</strong> (Unità Didattica di Apprendimento) nasce dalla perfetta sinergia tra
  obiettivi formativi chiari, metodi didattici ben strutturati e strategie di valutazione efficaci.
  L’UDA dovrebbe guidare lo studente verso <u>competenze trasversali</u> e disciplinari, seguendo
  una logica inclusiva che risponda alle diverse esigenze di apprendimento.
</p>
<p>
  In questo articolo approfondiremo i principali aspetti da considerare quando si progetta
  un’Unità Didattica di Apprendimento che possa davvero fare la differenza, non solo agli occhi
  della commissione (in caso di concorso o esame), ma soprattutto per gli studenti che la vivono.
</p>

<h2>1. Identifica i bisogni formativi</h2>
<p>
  <!-- ... (resto del contenuto) ... -->
</p>

<h2>2. Organizza i contenuti in maniera modulare</h2>
<p>
  <!-- ... (resto del contenuto) ... -->
</p>

<!-- ... ecc. (tutte le tue sezioni 3,4,5,6,7 e conclusioni) ... -->


<!-- Sezione "Altri articoli del nostro Blog" (dinamica) -->
<div class="blog-intro">
  <h2>Altri articoli del nostro Blog</h2>
  <p>
    Se ti è piaciuto questo contenuto, potresti trovare interessanti altri articoli dedicati ad argomenti simili.
  </p>
</div>

<div class="blog-list">
  <?php foreach ($posts as $postItem): ?>
    <!-- Mostra il post solo se NON è quello corrente -->
    <?php if ($postItem['slug'] !== $currentSlug): ?>
      <article class="blog-card">
        <h3><?php echo $postItem['title']; ?></h3>
        <p><?php echo $postItem['summary']; ?></p>
        <a href="/blog/<?php echo $postItem['slug']; ?>?slug=<?php echo $postItem['slug']; ?>" class="btn-servizio">
          Leggi l'articolo
        </a>
      </article>
    <?php endif; ?>
  <?php endforeach; ?>
</div>

<!-- Pulsante per tornare alla Home -->
<div style="text-align:center; margin-top: 2rem;">
  <a href="/uda.html" class="btn-back">Torna alla Home</a>
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











<?php
// Cattura il contenuto specifico nel buffer
$content = ob_get_clean();

// Definisci le variabili per meta tag e titolo
$title          = "Blog - Come preparare un’UDA vincente";
$og_title       = $title;
$og_description = "Una UDA vincente nasce dalla perfetta sinergia tra obiettivi formativi chiari, metodi didattici ben strutturati e strategie di valutazione efficaci.";
$og_image       = "https://aiutotesi.altervista.org/blog/UDA_blog_2.PNG";

// Includi il template base e renderizza la pagina
require 'base_blog.php';
renderTemplate($title, $og_title, $og_description, $og_image, $content);
?>
