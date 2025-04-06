<?php
function renderTemplate($title, $og_title, $og_description, $og_image, $content) {
    ?>
    <!DOCTYPE html>
    <html lang="it">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title><?php echo $title; ?></title>
      
      <!-- Meta Open Graph -->
      <meta property="og:title" content="<?php echo $og_title; ?>" />
      <meta property="og:description" content="<?php echo $og_description; ?>" />
      <meta property="og:image" content="<?php echo $og_image; ?>" />
      <script>!function(d,l,e,s,c){e=d.createElement("script");e.src="//ad.altervista.org/js.ad/size=728X90/?ref="+encodeURIComponent(l.hostname+l.pathname)+"&r="+Date.now();s=d.scripts;c=d.currentScript||s[s.length-1];c.parentNode.insertBefore(e,c)}(document,location)</script>
      <!-- Favicon -->
      <link rel="icon" href="https://aiutotesi.altervista.org/ImmaginiSitoTesi/Homepage/favicon_32_32.png" sizes="32x32" />
      
      <!-- Bootstrap CSS -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      
      <!-- CSS comune: include qui tutti gli stili che vuoi riutilizzare -->
      <style>
        /* Stili di base */
        body {
          background-color: #e66325;
          color: #333;
          min-height: 100vh;
          margin: 0;
          font-family: Arial, Helvetica, sans-serif;
          line-height: 1.6;
        }
        a {
          text-decoration: none;
          color: inherit;
        }
        .container {
          max-width: 800px;
          margin: 2rem auto;
          padding: 1rem;
          background: #fff;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          text-align: left;
        }
        h1 {
          font-size: 2rem;
          margin-bottom: 1rem;
          color: #e66325;
          text-align: center;
        }
        h2 {
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
          color: #333;
        }
        p {
          font-size: 1rem;
          color: #555;
          margin-bottom: 1rem;
        }
        .btn-back {
          display: inline-block;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          font-weight: bold;
          background-color: #555;
          color: #fff;
          text-align: center;
          transition: background-color 0.3s ease, transform 0.3s ease;
          margin-top: 2rem;
        }
        .btn-back:hover {
          background-color: #333;
          transform: scale(1.05);
        }
        
        /* Stili per la sezione Blog (anteprime) */
        .blog-list {
          display: flex;
          flex-wrap: wrap;
          gap: 1rem;
          justify-content: center;
          margin-top: 2rem;
        }
        .blog-card {
          background-color: #f9f9f9;
          padding: 1.5rem;
          border-radius: 8px;
          border: 1px solid #eee;
          max-width: 350px;
          flex: 1 1 calc(53.333% - 1rem);
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          text-align: left;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
          cursor: pointer;
        }
        .blog-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .blog-card h3 {
          font-size: 1.3rem;
          margin-bottom: 0.5rem;
          color: #333;
        }
        .blog-card p {
          font-size: 1rem;
          color: #555;
          margin-bottom: 1rem;
        }
        .blog-card .btn-servizio {
          display: inline-block;
          background-color: #e66325;
          color: #fff;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          text-decoration: none;
          font-weight: bold;
          transition: background-color 0.3s ease;
        }
        .blog-card .btn-servizio:hover {
          background-color: #cc521b;
        }
        
        /* Navigazione tra post */
        .post-navigation {
          display: flex;
          justify-content: space-between;
          margin-top: 2rem;
        }
        .post-navigation a {
          background-color: #555;
          color: #fff;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          text-decoration: none;
        }
        .post-navigation a:hover {
          background-color: #333;
        }
        
        /* Bottone WhatsApp fisso */
        .whatsapp-float {
          position: fixed;
          bottom: 20px;
          right: 20px;
          width: 60px;
          height: 60px;
          background-color: #25d366;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 2px 5px rgba(0,0,0,0.3);
          z-index: 1000;
          transition: transform 0.3s ease;
        }
        .whatsapp-float:hover {
          transform: scale(1.1);
        }
        .whatsapp-float img {
          width: 35px;
          height: 35px;
        }
      </style>
      
      <!-- Altri CSS o script comuni se necessari -->
    </head>
    <body>
      <!-- Header comune -->
      <header>
        <!-- Qui puoi inserire una navbar o un logo -->
      </header>
      
      <!-- Contenuto specifico della pagina -->
      <div class="container">
        <?php echo $content; ?>
      </div>
      
      <!-- Footer comune -->
      <footer class="footer">
        <div class="container">
          <p>© 2017-2025 | Tutti i diritti riservati © HelpThesis</p>
        </div>
      </footer>
      
      <!-- Bottone WhatsApp fisso -->
      <a href="https://wa.me/393780608777" target="_blank" class="whatsapp-float">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="Chatta su WhatsApp">
      </a>
      
      <!-- Bootstrap JS -->
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
      
      <!-- Altri script comuni se necessari -->
    </body>
    </html>
    <?php
}
?>
