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




<h1>E-portfolio: raccontare il percorso di apprendimento in modo dinamico</h1>

<p>
  Un <strong>e-portfolio</strong> è uno strumento digitale che permette di documentare
  e valorizzare il processo di apprendimento di uno studente (o di un docente in formazione).
  Non si tratta soltanto di una raccolta di elaborati, ma di una <em>narrazione</em>
  in cui ogni “pezzo” (testi, video, presentazioni, progetti) contribuisce a restituire
  una visione <strong>globale</strong> delle competenze acquisite e del cammino percorso.
</p>

<h2>Perché usare un e-portfolio</h2>
<ul>
  <li>
    <strong>Documentazione continua:</strong> gli studenti possono caricare in tempo reale
    i propri lavori, appunti, riflessioni o feedback ricevuti, creando una <em>memoria
    digitale</em> sempre aggiornata.
  </li>
  <li>
    <strong>Consapevolezza metacognitiva:</strong> rileggere e rivedere il proprio processo
    di apprendimento aiuta a individuare punti di forza, difficoltà, strategie di studio
    efficaci o da migliorare.
  </li>
  <li>
    <strong>Valutazione formativa:</strong> il docente può analizzare l’evoluzione
    dell’allievo nel tempo, andando oltre il singolo voto e cogliendo gli aspetti
    qualitativi del lavoro svolto.
  </li>
  <li>
    <strong>Portabilità e condivisione:</strong> i materiali digitali possono essere
    facilmente mostrati ai compagni, alle famiglie o a futuri datori di lavoro, offrendo
    un profilo <em>multidimensionale</em> delle proprie competenze.
  </li>
</ul>

<h2>Strumenti e piattaforme consigliate</h2>
<ul>
  <li>
    <strong>Google Sites:</strong> ideale per creare siti web semplici e intuitivi,
    organizzando le pagine tematicamente (progetti, riflessioni, media).
  </li>
  <li>
    <strong>Mahara:</strong> una piattaforma open source pensata proprio per
    la creazione di e-portfolio, con funzionalità social e possibilità
    di aggregare contenuti da varie fonti.
  </li>
  <li>
    <strong>Seesaw:</strong> molto usata in contesti scolastici, permette
    di condividere in tempo reale lavori e progressi con le famiglie, facilitando
    l’interazione.
  </li>
  <li>
    <strong>Padlet o Wakelet:</strong> se si vuole iniziare con uno strumento più
    informale, queste bacheche virtuali consentono di “pinnare” link, file e note
    in modo collaborativo.
  </li>
</ul>

<h2>Come strutturare un e-portfolio</h2>
<ol>
  <li>
    <strong>Home page di presentazione:</strong> una breve introduzione che
    spieghi la finalità dell’e-portfolio e fornisca informazioni su chi l’ha realizzato.
  </li>
  <li>
    <strong>Sezioni tematiche o disciplinari:</strong> suddividi i contenuti
    in aree (es. Italiano, Matematica, Lingue, Progetti, Esperienze extra)
    per facilitare la navigazione e la consultazione.
  </li>
  <li>
    <strong>Archiviazione cronologica:</strong> inserisci un “diario di bordo”
    o una sequenza temporale, utile a mostrare l’evoluzione dell’apprendimento
    e la riflessione sulle tappe raggiunte.
  </li>
  <li>
    <strong>Spazio per feedback e riflessioni:</strong> ogni elaborato può essere
    accompagnato da un commento dell’autore e/o del docente, per evidenziare
    successi, criticità e spunti di miglioramento.
  </li>
</ol>

<h2>Valutazione e riconoscimento</h2>
<p>
  L’e-portfolio può essere integrato nella valutazione formativa, attribuendo
  importanza non solo al <em>prodotto finale</em>, ma anche al <em>processo</em>:
  quanti progressi sono stati fatti, come lo studente ha superato le difficoltà,
  quanto ha saputo integrare competenze diverse?
  Alcune scuole e università rilasciano <strong>badge digitali</strong> o attestati
  specifici, riconoscendo pubblicamente le competenze documentate.
</p>

<h2>Consigli operativi</h2>
<ul>
  <li>
    <strong>Guidare gli studenti:</strong> soprattutto all’inizio, fornire istruzioni
    chiare su come caricare i materiali, organizzare le sezioni e formattare i contenuti.
  </li>
  <li>
    <strong>Garantire la privacy:</strong> attenzione a non pubblicare informazioni
    sensibili o immagini di altri studenti senza autorizzazione. Impostare correttamente
    i livelli di condivisione.
  </li>
  <li>
    <strong>Promuovere l’autonomia:</strong> incoraggiare gli alunni a personalizzare
    l’e-portfolio con elementi grafici, riflessioni personali e link a risorse esterne
    che arricchiscano il loro lavoro.
  </li>
  <li>
    <strong>Integrare con altre metodologie:</strong> il portfolio può dialogare
    con <em>didattica per competenze</em>, <em>compiti autentici</em> e valutazioni
    intermedie, fornendo uno sguardo articolato sul percorso formativo.
  </li>
</ul>

<h2>Conclusioni</h2>
<p>
  L’<strong>e-portfolio</strong> non è solo un archivio di elaborati, ma una vera
  “finestra” sulla crescita personale e scolastica dell’allievo. È uno strumento
  che promuove <em>autonomia</em>, riflessione metacognitiva e uno scambio più
  fluido e trasparente tra studente, docente e famiglia. In un’epoca in cui
  la <strong>documentazione digitale</strong> è sempre più centrale, introdurre
  l’e-portfolio significa <em>innovare</em> il modo di valutare e
  <em>valorizzare</em> l’apprendimento.
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