"""Publica los artículos de _articulos/*.md como páginas estáticas (sin panel ni dependencias).

Uso (desde la carpeta del proyecto):   python _scripts/publicar.py

Genera:
  - articulos/<archivo>.html      una página por artículo (índice de secciones, notas al pie, compartir, relacionados)
  - articulos.html                listado con filtro por área
  - index.html                    los últimos 3 artículos entre <!-- ARTICULOS:INICIO --> y <!-- ARTICULOS:FIN -->
Ver _articulos/COMO-PUBLICAR.md para el formato de los archivos."""
import os, re, sys, html, unicodedata
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import head, header, footer, esc, WA_DEF

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(D, "_articulos")
OUT = os.path.join(D, "articulos")
SITE_NAME = "Estudio Jurídico Casanegra & Asociados"

AUTORES = {
    "francisco": ("Francisco Casanegra", "Abogado · Magíster en Derecho Administrativo", "FC"),
    "paula": ("Paula Casanegra", "Abogada · Socia del estudio", "PC"),
    "estudio": ("Casanegra & Asociados", "Equipo del estudio", "C&amp;A"),
}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# ------------------------------------------------------------------ utilidades
def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def fecha_larga(d): return f"{d.day} de {MESES[d.month - 1]} de {d.year}"
def fecha_corta(d): return f"{d.day:02d} {MESES[d.month - 1][:3].upper()} {d.year}"

def leer(path):
    raw = open(path, encoding="utf8").read().replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    for k in ("titulo", "fecha", "area", "resumen"):
        if not meta.get(k):
            sys.exit(f"Falta «{k}» en {os.path.basename(path)}")
    meta["date"] = date.fromisoformat(meta["fecha"])
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["md"] = m.group(2)
    meta["autor"] = meta.get("autor", "estudio").lower()
    img = meta.get("imagen", "").strip()
    if img:
        if not os.path.exists(os.path.join(D, "img", "articulos", img)):
            sys.exit(f"No encuentro la imagen «img/articulos/{img}» de {meta['slug']}.md")
        meta["img"] = img
    if meta["autor"] not in AUTORES:
        sys.exit(f"Autor desconocido «{meta['autor']}» en {meta['slug']}.md (opciones: {', '.join(AUTORES)})")
    return meta

# ------------------------------------------------------------------ markdown mínimo
def inline(s, refs):
    s = html.escape(s, quote=False)
    s = s.replace("\\.", ".")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    def fn(m):
        n = m.group(1); first = n not in refs; refs.add(n)
        rid = f' id="ref-{n}"' if first else ""
        return f'<sup class="fn-ref"><a href="#fn-{n}"{rid} aria-label="Nota {n}">{n}</a></sup>'
    return re.sub(r"\[\^(\d+)\]", fn, s)

def md_to_html(md):
    refs, notas, toc, out = set(), {}, [], []
    blocks = re.split(r"\n\s*\n", md.strip())
    for b in blocks:
        lines = [l.rstrip() for l in b.strip().split("\n") if l.strip()]
        if not lines:
            continue
        if all(re.match(r"^\[\^\d+\]:", l) for l in lines):
            for l in lines:
                n, t = re.match(r"^\[\^(\d+)\]:\s*(.*)$", l).groups(); notas[n] = t
            continue
        h = re.match(r"^(#{2,3})\s+(.*)$", lines[0])
        if h and len(lines) == 1:
            lvl = len(h.group(1)); txt = h.group(2)
            plain = re.sub(r"\[\^\d+\]", "", txt).strip()
            hid = slugify(plain)
            if lvl == 2:
                toc.append((hid, plain))
            out.append(f'<h{lvl} id="{hid}">{inline(txt, refs)}</h{lvl}>')
            continue
        if all(l.startswith(">") for l in lines):
            out.append("<blockquote><p>" + inline(" ".join(l.lstrip("> ").strip() for l in lines), refs) + "</p></blockquote>")
            continue
        if all(re.match(r"^[-*]\s+", l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(re.sub(r'^[-*]\s+', '', l), refs)}</li>" for l in lines) + "</ul>")
            continue
        if all(re.match(r"^\d+\.\s+", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\.\s+', '', l), refs)}</li>" for l in lines) + "</ol>")
            continue
        out.append("<p>" + inline(" ".join(lines), refs) + "</p>")
    body = "\n".join(out)
    if notas:
        items = "\n".join(f'<li id="fn-{n}">{inline(t, set())} <a href="#ref-{n}" class="fn-back" aria-label="Volver al texto">↩</a></li>'
                          for n, t in sorted(notas.items(), key=lambda x: int(x[0])))
        body += f'\n<section class="fns" aria-label="Notas"><h2 id="notas">Notas</h2><ol>\n{items}\n</ol></section>'
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return body, toc, max(1, round(words / 200))

# ------------------------------------------------------------------ piezas
def card(a, p):
    return f'''      <article class="art-card reveal" data-area="{slugify(a["area"])}">
        <a href="{p}articulos/{a["slug"]}.html">
          <p class="ac-meta"><span>{esc(a["area"])}</span><time datetime="{a["fecha"]}">{fecha_corta(a["date"])}</time></p>
          <h3>{esc(a["titulo"])}</h3>
          <p>{esc(a["resumen"])}</p>
          <span class="ac-more">Leer artículo · {a["min"]} min <i class="ti ti-arrow-right"></i></span>
        </a>
      </article>'''

def pagina_articulo(a, todos):
    p = "../"
    nombre, cargo, ini = AUTORES[a["autor"]]
    toc = ""
    if len(a["toc"]) >= 3:
        toc = '<nav class="side-box toc" aria-label="En este artículo"><p class="side-t">En este artículo</p><ol>' + "".join(
            f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in a["toc"]) + "</ol></nav>"
    rel = [x for x in todos if x is not a and x["area"] == a["area"]] + [x for x in todos if x is not a and x["area"] != a["area"]]
    rel_html = "\n".join(card(x, p) for x in rel[:3])
    fuente = f'<p class="art-fuente">Publicado originalmente en {esc(a["fuente"])}.</p>' if a.get("fuente") else ""
    msg = f"Hola, leí el artículo «{a['titulo']}» y quisiera hacer una consulta."
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["titulo"][:110], "description": a["resumen"],
           "datePublished": a["fecha"], "inLanguage": "es-AR", "articleSection": a["area"],
           "author": {"@type": "Person" if a["autor"] != "estudio" else "Organization", "name": html.unescape(nombre)},
           "publisher": {"@type": "Organization", "name": SITE_NAME}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "../index.html"},
              {"@type": "ListItem", "position": 2, "name": "Artículos", "item": "../articulos.html"},
              {"@type": "ListItem", "position": 3, "name": a["titulo"]}]}]
    hero_cls, hero_bg, og = "art-hero", "", None
    if a.get("img"):   # foto provista por el cliente para este artículo
        hero_cls = "art-hero art-hero-img"
        hero_bg = f'''\n    <div class="ph-bg" aria-hidden="true" style="background-image:url('{p}img/articulos/{a["img"]}')"></div>'''
        og = f"{p}img/articulos/{a['img']}"
    return head(p, f'{a["titulo"]} | Casanegra & Asociados', a["resumen"], ld, og_type="article", og_img=og) + header(p, "articulos.html") + f'''
<main>
<article class="art">
  <header class="{hero_cls}">{hero_bg}
    <div class="wrap art-hero-in">
      <nav aria-label="Ruta"><ol class="crumbs"><li><a href="{p}index.html">Inicio</a></li><li><i class="ti ti-chevron-right" aria-hidden="true"></i><a href="{p}articulos.html">Artículos</a></li><li><i class="ti ti-chevron-right" aria-hidden="true"></i><span aria-current="page">{esc(a["area"])}</span></li></ol></nav>
      <h1 class="art-h1">{esc(a["titulo"])}</h1>
      <p class="art-lead">{esc(a["resumen"])}</p>
      <div class="art-meta">
        <span class="avatar" aria-hidden="true">{ini}</span>
        <div class="art-author"><b>{nombre}</b><small>{cargo}</small></div>
        <span class="art-dot" aria-hidden="true"></span>
        <time datetime="{a["fecha"]}">{fecha_larga(a["date"])}</time>
        <span class="art-dot" aria-hidden="true"></span>
        <span>{a["min"]} min de lectura</span>
      </div>
    </div>
  </header>
  <div class="wrap art-layout">
    <div class="prose">
{a["html"]}
      {fuente}
      <p class="art-aviso">El presente artículo tiene carácter informativo y no constituye asesoramiento jurídico para un caso concreto.</p>
    </div>
    <aside class="art-side">
      {toc}
      <div class="side-box">
        <p class="side-t">Compartir</p>
        <div class="share">
          <button type="button" data-share="whatsapp" aria-label="Compartir por WhatsApp"><i class="ti ti-brand-whatsapp"></i></button>
          <button type="button" data-share="linkedin" aria-label="Compartir en LinkedIn"><i class="ti ti-brand-linkedin"></i></button>
          <button type="button" data-share="copiar" aria-label="Copiar el enlace"><i class="ti ti-link"></i></button>
        </div>
      </div>
      <div class="side-box side-cta">
        <p class="side-t">¿Su caso se relaciona con este tema?</p>
        <p>Cuéntenos su situación y la analizamos.</p>
        <a class="btn btn-gold js-wa" href="#" data-msg="{esc(msg)}">Consultar por WhatsApp</a>
      </div>
    </aside>
  </div>
</article>

<section class="art-sec art-rel">
  <div class="wrap">
    <div class="sec-top">
      <div><p class="eyebrow">Seguir leyendo</p><h2 class="h2">Otros <em>artículos.</em></h2></div>
      <a href="{p}articulos.html" class="link-arrow">Ver todos <i class="ti ti-arrow-right"></i></a>
    </div>
    <div class="art-grid">
{rel_html}
    </div>
  </div>
</section>
</main>
''' + footer(p)

def pagina_listado(todos):
    p = "./"
    areas = []
    for a in todos:
        if a["area"] not in areas:
            areas.append(a["area"])
    chips = '<button type="button" class="chip on" data-filter="todas">Todas</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{slugify(x)}">{esc(x)}</button>' for x in areas)
    cards = "\n".join(card(a, p) for a in todos)
    u = todos[0] if todos else None
    destacado = "" if not u else f"""  <a class="ph-feat rise d3" href="./articulos/{u["slug"]}.html">
    <span class="pf-tag">Último artículo</span>
    <span class="pf-area">{esc(u["area"])} · {fecha_corta(u["date"])}</span>
    <span class="pf-t">{esc(u["titulo"])}</span>
    <span class="ac-more">Leer · {u["min"]} min <i class="ti ti-arrow-right"></i></span>
  </a>"""
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Artículos y novedades — Casanegra & Asociados",
          "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"][:110], "datePublished": a["fecha"],
                        "url": f"articulos/{a['slug']}.html"} for a in todos]}
    return head(p, "Artículos y publicaciones jurídicas | Casanegra & Asociados",
                "Análisis normativo, jurisprudencia y novedades en derecho aduanero, administrativo, del consumidor, migratorio e inversiones.", ld) + header(p, "articulos.html") + f'''
<main>
<!-- foto de fondo: https://images.pexels.com/photos/4124053/pexels-photo-4124053.jpeg -->
<section class="ph ph-img">
  <div class="ph-bg" aria-hidden="true" style="background-image:url('./img/articulos.jpg');background-position:center 55%"></div>
  <div class="wrap ph-in">
    <nav aria-label="Ruta"><ol class="crumbs"><li><a href="./index.html">Inicio</a></li><li><i class="ti ti-chevron-right" aria-hidden="true"></i><span aria-current="page">Artículos</span></li></ol></nav>
    <h1 class="ph-h1 split-words">Artículos <em>y novedades.</em></h1>
    <p class="lead">Análisis normativo, jurisprudencia y tendencias en nuestras áreas de práctica.</p>
  </div>
{destacado}
</section>
<section class="art-sec art-list">
  <div class="wrap">
    <div class="chips" role="group" aria-label="Filtrar por área">{chips}</div>
    <div class="art-grid" id="artGrid">
{cards}
    </div>
    <p class="art-empty" id="artEmpty" hidden>No hay artículos en esta área todavía.</p>
  </div>
</section>
</main>
''' + footer(p)

# ------------------------------------------------------------------ main
def main():
    todos = []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".md") or f.upper() == f or f.startswith("_"):
            continue
        a = leer(os.path.join(SRC, f))
        if not a or a.get("borrador", "").lower() in ("si", "sí", "true"):
            continue
        a["html"], a["toc"], a["min"] = md_to_html(a["md"])
        todos.append(a)
    todos.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    os.makedirs(OUT, exist_ok=True)
    vivos = set()
    for a in todos:
        name = a["slug"] + ".html"; vivos.add(name)
        open(os.path.join(OUT, name), "w", encoding="utf8", newline="\n").write(pagina_articulo(a, todos))
        print(f"  articulos/{name}  ({a['min']} min, {len(a['toc'])} secciones)")
    for f in os.listdir(OUT):                       # artículos borrados o pasados a borrador
        if f.endswith(".html") and f not in vivos:
            os.remove(os.path.join(OUT, f)); print("  eliminado articulos/" + f)
    open(os.path.join(D, "articulos.html"), "w", encoding="utf8", newline="\n").write(pagina_listado(todos))
    print("  articulos.html")
    idx = os.path.join(D, "index.html")
    s = open(idx, encoding="utf8").read()
    bloque = "<!-- ARTICULOS:INICIO -->\n    <div class=\"art-grid\">\n" + "\n".join(card(a, "./") for a in todos[:3]) + "\n    </div>\n    <!-- ARTICULOS:FIN -->"
    s2, n = re.subn(r"<!-- ARTICULOS:INICIO -->.*?<!-- ARTICULOS:FIN -->", lambda m: bloque, s, flags=re.S)
    if n:
        open(idx, "w", encoding="utf8", newline="\n").write(s2); print("  index.html (últimos 3)")
    print(f"Listo: {len(todos)} artículos publicados.")

if __name__ == "__main__":
    main()
