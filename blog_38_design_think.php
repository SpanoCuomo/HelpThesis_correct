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






<h1>Design Thinking: creatività e problem solving a scuola</h1>

<p>
  Il <strong>Design Thinking</strong> è un approccio nato nel mondo dell’innovazione
  e del design, ma applicabile con successo anche in ambito educativo. Si basa su un
  <em>processo iterativo</em> che mette al centro le persone (in questo caso gli studenti)
  e punta a risolvere problemi in modo <strong>creativo</strong> e <strong>collaborativo</strong>.
  Introdurre il Design Thinking in classe significa promuovere competenze come
  l’empatia, la capacità di analisi, l’ideazione di soluzioni originali e la
  sperimentazione continua.
</p>

<h2>Le fasi del Design Thinking</h2>
<ol>
  <li>
    <strong>Empatizzare:</strong> comprendere a fondo il contesto, le esigenze e
    le motivazioni di chi vivrà la soluzione (ad esempio, gli stessi studenti, altri
    compagni, la comunità scolastica). In classe, ciò può tradursi in interviste,
    questionari o momenti di discussione per mettersi “nei panni” delle persone
    interessate.
  </li>
  <li>
    <strong>Definire:</strong> sintetizzare le informazioni raccolte per formulare
    il problema in modo chiaro e specifico. In questa fase, si circoscrive l’obiettivo
    o la sfida che il team vuole affrontare (es. “Come possiamo migliorare gli
    spazi comuni della scuola per favorire la socializzazione?”).
  </li>
  <li>
    <strong>Ideare:</strong> brainstorming e generazione di idee senza giudizio o
    censure. Gli studenti sono incoraggiati a pensare “fuori dagli schemi”,
    a proporre soluzioni e ad ascoltare quelle degli altri. Più idee si producono,
    maggiore è la possibilità di trovare spunti innovativi.
  </li>
  <li>
    <strong>Prototipare:</strong> realizzare versioni preliminari (disegni, modelli,
    simulazioni, presentazioni digitali) delle idee emerse. Non serve essere
    perfetti: si tratta di dare una <em>forma tangibile</em> alla propria visione
    per poterla valutare e migliorare.
  </li>
  <li>
    <strong>Testare:</strong> raccogliere feedback sul prototipo. Si chiede a chi
    userà la soluzione (compagni, docenti, personale scolastico) di provarla
    e fornire commenti. In base ai riscontri, si ritorna a perfezionare l’idea,
    rientrando in una logica iterativa di miglioramento costante.
  </li>
</ol>

<h2>I vantaggi del Design Thinking in classe</h2>
<ul>
  <li>
    <strong>Apprendimento attivo:</strong> gli studenti sono coinvolti in prima persona
    come problem solver e progettisti, sviluppando un <em>approccio propositivo</em>
    alla realtà.
  </li>
  <li>
    <strong>Collaborazione e comunicazione:</strong> l’intero processo richiede
    momenti di confronto e scambio di idee, potenziando competenze relazionali
    e di lavoro di squadra.
  </li>
  <li>
    <strong>Spirito critico:</strong> la fase di test e miglioramento insegna a
    <em>accogliere il feedback</em> come parte integrante della crescita, evitando
    di percepire l’errore come un fallimento.
  </li>
  <li>
    <strong>Flessibilità mentale:</strong> la rapidità con cui si passa dall’idea
    all’azione e viceversa aiuta a allenare la resilienza e la capacità di adattamento.
  </li>
</ul>

<h2>Come introdurre il Design Thinking nella didattica</h2>
<ol>
  <li>
    <strong>Scegli un tema rilevante:</strong> individua una sfida reale (es. migliorare
    le dinamiche di classe, progettare un evento, risolvere un problema di quartiere)
    che coinvolga e motivi gli studenti.
  </li>
  <li>
    <strong>Forma i gruppi di lavoro:</strong> crea team eterogenei per capacità,
    interessi e background. Fornisci pochi ma chiari obiettivi: lascia spazio
    all’autonomia ma garantisci una guida per non disperdere le energie.
  </li>
  <li>
    <strong>Stabilisci tempi e fasi:</strong> scandisci le varie tappe (empatia, definizione,
    ideazione, prototipazione, test) con scadenze realistiche. Ciò aiuta a mantenere
    una certa <em>disciplina progettuale</em>.
  </li>
  <li>
    <strong>Invita esperti o stakeholder esterni:</strong> se possibile, porta in classe
    persone che possano arricchire la fase di empatia o quella di test (ad esempio
    un rappresentante del Comune, un esperto di design, un ex studente che lavora
    nell’ambito).
  </li>
  <li>
    <strong>Documenta il processo:</strong> incoraggia i ragazzi a tenere traccia di
    idee, bozze, riflessioni ed errori. Un diario di bordo o un <em>portfolio</em>
    può rivelarsi prezioso per la valutazione finale.
  </li>
</ol>

<h2>Valutazione e feedback</h2>
<p>
  Valutare il <strong>Design Thinking</strong> non significa concentrarsi solo sul
  risultato conclusivo (il prototipo), ma anche, e soprattutto, sul <em>processo</em>:
  come hanno collaborato i membri del gruppo, in che modo hanno accolto (o fornito)
  feedback, quanto sono stati capaci di rielaborare e sperimentare. Utilizzare rubriche
  di valutazione che tengano conto degli aspetti relazionali e creativi aiuta a
  mettere in luce la crescita complessiva degli studenti.
</p>

<h2>Conclusioni</h2>
<p>
  Il <strong>Design Thinking</strong> rappresenta una metodologia didattica innovativa
  che va oltre la semplice teoria, allenando l’<em>inventiva</em> e il <em>pensiero critico</em>.
  Inserirlo nel contesto scolastico significa offrire agli studenti un’occasione
  per imparare facendo, sbagliando e migliorando, diventando <strong>protagonisti</strong>
  del cambiamento nella propria scuola e, più in generale, nella società.
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