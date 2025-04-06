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
















<h1>Progettazione per competenze e valutazione formativa: dal “cosa sai” al “cosa sai fare”</h1>

<p>
  In un contesto in cui il mercato del lavoro e la società richiedono sempre più
  <strong>abilità trasversali</strong> e flessibili, la <em>didattica per competenze</em>
  è diventata essenziale. Questo approccio va oltre la semplice trasmissione di
  conoscenze teoriche, concentrandosi su come gli studenti riescano a utilizzare
  ciò che imparano in situazioni <strong>concrete e reali</strong>. Parallelamente,
  la <strong>valutazione formativa</strong> (o valutazione “per l’apprendimento”)
  mira a fornire feedback continui per orientare e sostenere il processo di crescita
  dello studente.
</p>

<h2>Perché progettare per competenze</h2>
<ul>
  <li>
    <strong>Orientamento alla realtà:</strong> una didattica basata sulle competenze
    prepara gli studenti a risolvere problemi e a prendere decisioni in situazioni
    autentiche, riproducendo sfide della vita quotidiana o professionale.
  </li>
  <li>
    <strong>Apprendimento duraturo:</strong> costruendo conoscenze e abilità integrate
    fra loro, gli studenti acquisiscono un bagaglio che rimane saldo nel tempo,
    perché costantemente allenato e sperimentato.
  </li>
  <li>
    <strong>Motivazione:</strong> capire lo scopo di ciò che si studia aumenta la
    voglia di imparare. L’apprendimento finalizzato a un “fare” rende le lezioni
    più coinvolgenti.
  </li>
</ul>

<h2>Come passare a una didattica per competenze</h2>
<ol>
  <li>
    <strong>Identificare le competenze chiave:</strong> stabilisci quali risultati
    di apprendimento (conoscenze, abilità, atteggiamenti) vuoi promuovere.
    Puoi far riferimento alle competenze chiave europee o alle indicazioni
    nazionali ministeriali.
  </li>
  <li>
    <strong>Pensare in termini di UDA (Unità di Apprendimento):</strong> progetta
    percorsi che integrino diverse discipline, focalizzati su una o più competenze
    da sviluppare. Includi compiti reali o simulazioni come attività-fulcro.
  </li>
  <li>
    <strong>Scegliere metodologie attive:</strong> lavori di gruppo, simulazioni,
    compiti autentici, flipped classroom, dibattiti strutturati. L’idea è che
    lo studente agisca in modo concreto, riflettendo su ciò che fa.
  </li>
  <li>
    <strong>Prevedere momenti di riflessione:</strong> lascia spazi in cui gli studenti
    possano rielaborare ciò che hanno appreso, confrontarsi, fare autovalutazione
    e ricevere feedback.
  </li>
</ol>

<h2>Valutazione formativa: un continuo dialogo</h2>
<p>
  La <strong>valutazione formativa</strong> si distingue dalla valutazione sommativa
  (che mira a dare un voto finale) perché accompagna l’intero processo di apprendimento.
  Il suo scopo è migliorare le prestazioni dello studente e indirizzarlo verso
  il raggiungimento degli obiettivi.
</p>

<h3>Strumenti di valutazione formativa</h3>
<ul>
  <li>
    <strong>Osservazioni in classe:</strong> annotare progressi, difficoltà e
    interazioni fra pari durante attività di gruppo o esercitazioni.
  </li>
  <li>
    <strong>Rubriche di valutazione:</strong> griglie che definiscono i criteri
    (es. conoscenza, abilità pratiche, collaborazione) e i livelli di prestazione
    per ognuno.
  </li>
  <li>
    <strong>Feedback tempestivo:</strong> commenti e suggerimenti dati subito dopo
    l’esecuzione di un compito. È fondamentale che siano <em>costruttivi</em> e specifici,
    non limitati a un mero giudizio.
  </li>
  <li>
    <strong>Portfolio o e-portfolio:</strong> raccolta strutturata dei lavori svolti
    dallo studente, utile per documentare i progressi e riflettere sulle tappe
    superate e i miglioramenti futuri.
  </li>
</ul>

<h2>Benefici a lungo termine</h2>
<p>
  Integrare la <strong>didattica per competenze</strong> con la <strong>valutazione formativa</strong>
  crea un circuito virtuoso: gli studenti prendono consapevolezza dei propri punti di forza
  e di quelli da migliorare, assumono un ruolo attivo e responsabile e sviluppano un insieme
  di abilità utili in vari contesti di vita. Questo tipo di approccio didattico valorizza
  la <em>costruzione di conoscenze significative</em>, in cui l’errore diventa parte integrante
  e stimolo per la crescita.
</p>

<h2>Conclusioni</h2>
<p>
  La trasformazione verso una <strong>didattica per competenze</strong> e una
  <strong>valutazione formativa</strong> non avviene dall’oggi al domani, ma vale lo sforzo.
  L’obiettivo non è più soltanto trasmettere nozioni, ma <em>formare individui</em> capaci
  di muoversi in contesti complessi, di usare ciò che sanno in modo critico e creativo.
  In poche parole, di diventare <strong>cittadini competenti</strong>.
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