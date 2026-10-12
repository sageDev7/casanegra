"""Piezas compartidas del sitio de Casanegra (head, header, menú, footer).
Las usan publicar.py (artículos) y el generador de páginas internas.
`p` es el prefijo de ruta hasta la raíz: "./" en la raíz, "../" dentro de /articulos/.
El index.html está escrito a mano: si cambia el header o el footer acá, actualizarlo también ahí."""
import json

SITE = "Casanegra & Asociados"
WA_NUMBER = "543516506222"
WA_DEF = "Hola, quisiera hacer una consulta al estudio."
FONTS = ("https://fonts.googleapis.com/css2?family=Marcellus&family=Schibsted+Grotesk:wght@400;500;600;700"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap")

# (texto, ruta desde la raíz, existe todavía)
NAV = [("Nosotros", "nosotros.html", True), ("Áreas", "areas.html", True), ("Ciudadanías", "ciudadanias.html", True),
       ("Inversiones", "inversiones.html", True), ("Artículos", "articulos.html", True), ("Contacto", "index.html#contacto", True)]

def esc(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def og_meta(p, og_img):
    """OG cuadrado del sitio por defecto; si el artículo trae su propia foto, esa (panorámica)."""
    if og_img:
        return (f'<meta property="og:image" content="{og_img}">\n'
                '<meta name="twitter:card" content="summary_large_image">')
    return (f'<meta property="og:image" content="{p}og.png">\n'
            '<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="1200">\n'
            '<meta name="twitter:card" content="summary">')

def head(p, title, desc, ld=None, robots=None, og_type="website", og_img=None):
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    ldh = ""
    for block in (ld if isinstance(ld, list) else [ld] if ld else []):
        ldh += '<script type="application/ld+json">\n' + json.dumps(block, ensure_ascii=False, indent=2) + "\n</script>\n"
    return f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{rb}<meta name="theme-color" content="#081426">
<link rel="icon" type="image/png" href="{p}favicon.png">
<link rel="apple-touch-icon" href="{p}favicon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="{SITE.replace('&', '&amp;')}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
{og_meta(p, og_img)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.46.0/dist/tabler-icons.min.css">
<link rel="stylesheet" href="{p}styles.css">
{ldh}</head>
<body>
'''

def _links(p, active, indent):
    out = []
    for t, h, ok in NAV:
        cur = ' aria-current="page"' if h == active else ""
        soon = "" if ok else ""
        out.append(f'{indent}<a href="{p}{h}"{cur}{soon}>{t}</a>')
    return "\n".join(out)

def header(p, active=None):
    return f'''
<!-- ============ HEADER ============ -->
<header class="hdr" id="hdr">
  <div class="wrap hdr-in">
    <a href="{p}index.html" class="brand" aria-label="Casanegra &amp; Asociados, inicio">
      <img src="{p}logo.png" alt="Casanegra &amp; Asociados" width="722" height="230">
    </a>
    <nav class="nav" aria-label="Principal">
{_links(p, active, "      ")}
    </nav>
    <a class="btn btn-gold btn-sm hdr-cta js-wa" href="#" data-msg="{WA_DEF}">Consultar</a>
    <button class="burger" id="burger" aria-label="Abrir menú" aria-controls="mnav" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>

<div class="mnav-ov" id="mnavOv"></div>
<nav class="mnav" id="mnav" aria-label="Menú">
  <img src="{p}logo.png" alt="" class="mnav-logo" width="722" height="230">
{_links(p, active, "  ")}
  <a class="btn btn-gold js-wa" href="#" data-msg="{WA_DEF}">Consultar por WhatsApp</a>
</nav>
'''

def footer(p):
    return f'''
<!-- ============ FOOTER ============ -->
<footer class="ftr" id="ftr">
  <div class="wrap ftr-in">
    <div class="ftr-brand">
      <img src="{p}logo.png" alt="Casanegra &amp; Asociados" width="722" height="230" loading="lazy">
      <p>Asesoramos, negociamos y litigamos en áreas de alta complejidad normativa. Córdoba, Argentina.</p>
      <ul class="ftr-social">
        <li><a href="https://www.instagram.com/estudio_casanegra" target="_blank" rel="noopener" aria-label="Instagram"><i class="ti ti-brand-instagram"></i></a></li>
        <li><a href="https://www.facebook.com/estcasanegra" target="_blank" rel="noopener" aria-label="Facebook"><i class="ti ti-brand-facebook"></i></a></li>
        <li><a href="https://www.linkedin.com/in/francisco-casanegra-610413191/" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="ti ti-brand-linkedin"></i></a></li>
      </ul>
    </div>
    <div class="ftr-col">
      <h4>Estudio</h4>
      <ul>
        <li><a href="{p}nosotros.html">Nosotros</a></li>
        <li><a href="{p}areas.html">Áreas de práctica</a></li>
        <li><a href="{p}articulos.html">Artículos</a></li>
        <li><a href="{p}index.html#contacto">Contacto</a></li>
      </ul>
    </div>
    <div class="ftr-col">
      <h4>Especialidades</h4>
      <ul>
        <li><a href="{p}ciudadanias.html">Ciudadanías y migraciones</a></li>
        <li><a href="{p}inversiones.html">Derecho del inversor</a></li>
        <li><a href="{p}articulos/ciudadania-argentina-por-inversion.html">Ciudadanía por inversión</a></li>
      </ul>
    </div>
    <div class="ftr-col">
      <h4>Contacto</h4>
      <ul class="ftr-data">
        <li><i class="ti ti-map-pin"></i><span>José Gigena 2058, Cerro de las Rosas, Córdoba</span></li>
        <li><i class="ti ti-brand-whatsapp"></i><a class="js-wa" href="#" data-msg="{WA_DEF}">+54 351 650-6222</a></li>
        <li><i class="ti ti-phone"></i><a href="tel:+543512016540">+54 351 201-6540</a></li>
        <li><i class="ti ti-mail"></i><a href="mailto:secretaria@estudiocasanegra.com">secretaria@estudiocasanegra.com</a></li>
      </ul>
    </div>
  </div>
  <div class="ftr-bottom">
    <p>© <span id="yr">2026</span> Estudio Jurídico Casanegra &amp; Asociados. Todos los derechos reservados.</p>
    <p><a href="{p}privacidad.html">Política de privacidad</a></p>
    <p>Desarrollado por <a href="https://www.instagram.com/sageedev/" target="_blank" rel="noopener">@sageeDev</a></p>
  </div>
</footer>

<a class="wa-float js-wa" id="waFloat" href="#" data-msg="{WA_DEF}" aria-label="Escribir por WhatsApp"><i class="ti ti-brand-whatsapp"></i></a>

<script src="{p}main.js"></script>
</body>
</html>
'''
