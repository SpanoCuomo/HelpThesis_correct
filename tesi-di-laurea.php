<?php
// Avvia l'output buffering per catturare il contenuto specifico della pagina
ob_start();
?>

<!-- Inizio Contenuto Specifico della pagina "Tesi di Laurea" -->
<div class="container">
  <!-- Header della pagina -->
  <div class="header">
    <h1>Tesi di Laurea</h1>
    <p>Supporto professionale per la stesura, revisione e correzione della tua tesi.</p>
  </div>

  <!-- Sezione Descrizione -->
  <div class="description">
    <h2>Come possiamo aiutarti?</h2>
    <p>
      Offriamo consulenza per ogni fase: scelta dell’argomento, ricerca bibliografica, 
      stesura dei capitoli, revisione e correzione. Il nostro obiettivo è rendere il tuo lavoro 
      unico, chiaro e ben strutturato.
    </p>
    <h2>I nostri servizi includono:</h2>
    <p>
      1. Stesura di capitoli, introduzione e conclusioni.<br>
      2. Formattazione secondo le linee guida dell’ateneo (norme APA, Chicago, MLA...).<br>
      3. Revisione grammaticale, controllo plagio e correzioni di stile.<br>
      4. Presentazioni PowerPoint per la discussione finale.<br>
    </p>
    
    <h2>Consulenza per Tesi di Laurea</h2>
    <p>
      Stai affrontando la stesura della tua <strong>tesi di laurea</strong> e hai bisogno di un aiuto professionale? Offriamo:
    </p>
    <ul>
      <li><strong>Supporto nella scelta dell’argomento</strong>: ti guidiamo nella selezione del tema, tenendo conto dei tuoi interessi e degli obiettivi di ricerca.</li>
      <li><strong>Revisione e correzione</strong>: revisioniamo strutture, contenuti e stile per assicurare chiarezza, coerenza e correttezza ortografica e grammaticale.</li>
      <li><strong>Bibliografia e fonti</strong>: ti aiutiamo a individuare, analizzare e citare correttamente le fonti bibliografiche più pertinenti.</li>
    </ul>
    <p>
      Grazie alla nostra esperienza, potrai risparmiare tempo prezioso e ottenere un elaborato completo e ben strutturato.
    </p>
  </div>

  <h2>Alcuni esempi di Tesi</h2>
  <p>Consulta il materiale campione per valutare la nostra qualità di scrittura e impaginazione.</p>

  <!-- Sezione Preview: link a PDF campione -->
  <div class="navigation_prew">
    <a href="ImmaginiSitoTesi/Celle_combustibile_preview_latex.pdf" 
       class="preview-page" 
       style="background-image: url('ImmaginiSitoTesi/Celle_combustibile_preview_latex.png');">
      <span class="overlay-text">Esempio Celle a Combustibile</span>
    </a>
    <a href="ImmaginiSitoTesi/paper_hyplane_preview.pdf" 
       class="preview-page" 
       style="background-image: url('ImmaginiSitoTesi/paper_hyplane_preview.png');">
      <span class="overlay-text">Esempio Aerodinamica</span>
    </a>
  </div>

  <!-- Script per la gestione del modal PDF -->
  <script>
  document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById("pdfModal");
    var iframe = document.getElementById("pdfPreview");
    var downloadButton = document.getElementById("downloadPreview");
    var purchaseButton = document.getElementById("purchaseFull");
    var paypalContainer = document.getElementById("paypal-button-modal");
    var modalButtons = document.getElementById("modal-buttons");
    
    // Gestione dei link di anteprima
    var previewLinks = document.querySelectorAll('.preview-page, .book-cover-preview');
    previewLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        var previewSrc = link.getAttribute('data-preview') || link.href;
        var fullSrc = link.getAttribute('data-full') || link.href;
        iframe.src = previewSrc;
        downloadButton.href = previewSrc;
        purchaseButton.setAttribute('data-full', fullSrc);
        modalButtons.style.display = "flex";
        paypalContainer.style.display = "none";
        paypalContainer.innerHTML = "";
        modal.style.display = "block";
      });
    });
    
    var closeBtn = document.querySelector('.modal-content .close');
    closeBtn.addEventListener('click', function() {
      modal.style.display = "none";
      iframe.src = "";
    });
    
    window.addEventListener('click', function(e) {
      if (e.target == modal) {
        modal.style.display = "none";
        iframe.src = "";
      }
    });
    
    purchaseButton.addEventListener('click', function(e) {
      e.preventDefault();
      modalButtons.style.display = "none";
      paypalContainer.style.display = "block";
      paypal.Buttons({
        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{
              amount: { value: '12.00', currency_code: 'EUR' }
            }]
          });
        },
        onApprove: function(data, actions) {
          return actions.order.capture().then(function(details) {
            var postData = { orderID: data.orderID };
            return fetch('verifica_ordine.php', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(json => {
              if (json.status === 'ok') {
                var token = json.token;
                window.location.href = 'download.php?token=' + token;
              } else {
                alert('Qualcosa non va. Stato: ' + json.status);
              }
            })
            .catch(err => {
              console.error('Errore AJAX:', err);
              alert('Si è verificato un errore nel verificare l’ordine.');
            });
          });
        },
        onCancel: function(data) {
          paypalContainer.style.display = "none";
          modalButtons.style.display = "flex";
        },
        onError: function(err) {
          console.error('Errore nel pagamento:', err);
          alert('Si è verificato un errore. Riprova o contatta l’assistenza.');
        }
      }).render('#paypal-button-modal');
    });
  });
  </script>
  
  <!-- Modal Overlay per la preview del PDF -->
  <div id="pdfModal" class="modal">
    <div class="modal-content">
      <span class="close">&times;</span>
      <iframe src="" id="pdfPreview"></iframe>
      <div class="modal-buttons" id="modal-buttons">
        <a id="downloadPreview" class="btn btn-primary" download>Scarica Anteprima</a>
        <button id="purchaseFull" class="btn btn-secondary">Acquista Lavoro Completo</button>
      </div>
      <div id="paypal-button-modal" style="display: none;"></div>
    </div>
  </div>
  
  <!-- Navigazione: Pulsante per tornare alla Home -->
  <div class="navigation_CENT">
    <a href="/index.html" class="btn btn-secondary">Torna alla Home</a>
  </div>
  
  <!-- Link ad altri servizi -->
  <h3>Scopri anche:</h3>
  <div class="navigation">
    <a href="/uda.html" class="btn btn-primary">UDA e Lezioni Simulate</a>
    <a href="/progetti-universitari.html" class="btn btn-primary">Progetti Scientifici</a>
    <a href="/TFA.html" class="btn btn-primary">TFA</a>
  </div>
  
</div>

<!-- (Facoltativo) script di Bootstrap -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<!-- (Facoltativo) Includi qui eventuali altri script personalizzati -->

<?php
// Cattura il contenuto specifico nel buffer
$content = ob_get_clean();

// Definisci le variabili per meta tag e titolo
$title          = "Blog - Inserire Bibliografia: Suggerimenti Pratici";
$og_title       = "Blog - Inserire Bibliografia: Suggerimenti Pratici";
$og_description = "Scopri i migliori suggerimenti pratici per inserire correttamente la bibliografia nel testo della tua tesi.";
$og_image       = "https://aiutotesi.altervista.org/blog_tesi/tesi_blog_3.png";

// Includi il template base e renderizza la pagina
require 'base_blog.php';
renderTemplate($title, $og_title, $og_description, $og_image, $content);
?>
