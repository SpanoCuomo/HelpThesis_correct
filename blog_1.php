<?php
include('base_blog.php');    // Il file che contiene il layout comune
include('posts.php');        // L'elenco dei post

// Ottieni lo slug corrente: il nome del file (es. "blog_1.php")
$current_slug = basename(__FILE__);

// Cerca l'indice dell'articolo corrente nell'array $posts
$currentIndex = -1;
foreach ($posts as $i => $post) {
  if ($post['slug'] === $current_slug) {
    $currentIndex = $i;
    break;
  }
}

// Determina i post precedente e successivo
$previous = ($currentIndex > 0) ? $posts[$currentIndex - 1] : null;
$next = ($currentIndex < count($posts) - 1) ? $posts[$currentIndex + 1] : null;

// Apro la pagina con il titolo specifico
header_blog("Come creare l'indice di una tesi");
?>
<h1>Come creare l’indice di una tesi</h1>
<p>
  L’indice di una tesi non è un semplice elenco di titoli, ma costituisce la 
  <strong>mappa concettuale</strong> del tuo elaborato. Una struttura ben chiara ed equilibrata rende la lettura più agevole e aiuta a orientare il lettore.
</p>

<h5>1. Definire la struttura principale</h5>
<p>
  Prima di redigere l’indice, è indispensabile avere una visione chiara della struttura generale della tesi...
</p>

<!-- Aggiungi qui il resto del contenuto dell'articolo -->

<div class="my-4">
  <a href="blog_2.php">Articolo successivo</a>
</div>

<div style="text-align:center; margin-top: 2rem;">
  <a href="index.php" class="btn-back">Torna alla Home</a>
</div>

<?php
// Chiudo la pagina
footer_blog();
?>
