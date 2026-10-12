"""Páginas internas de Casanegra: nosotros, areas, ciudadanias, inversiones, privacidad y 404.
Comparten head/header/footer (comun.py) y las áreas con generar_index.py (GRUPOS).
Volver a correr tras cambios de estructura; el CSS va en styles.css."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import head, header, footer, esc, WA_DEF
from publicar import slugify

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)

def ph(img, pos, crumb, h1, lead, side="", px=None):
    c = f"<!-- foto de fondo: https://images.pexels.com/photos/{px}/pexels-photo-{px}.jpeg -->\n" if px else ""
    return f'''
<!-- ============ CABECERA ============ -->
{c}<section class="ph ph-img">
  <div class="ph-bg" aria-hidden="true" style="background-image:url('./img/{img}');background-position:{pos}"></div>
  <div class="wrap ph-in">
    <nav aria-label="Ruta"><ol class="crumbs"><li><a href="./index.html">Inicio</a></li><li><i class="ti ti-chevron-right" aria-hidden="true"></i><span aria-current="page">{crumb}</span></li></ol></nav>
    <h1 class="ph-h1 split-words">{h1[0]} <em>{h1[1]}</em></h1>
    <p class="lead rise d2">{lead}</p>
  </div>
{side}
</section>
'''

def cta(h2, lead, msg=WA_DEF, btn="Consultar por WhatsApp"):
    return f'''
<!-- ============ CIERRE ============ -->
<section class="cta-band">
  <div class="wrap reveal">
    <h2 class="h2">{h2[0]} <em>{h2[1]}</em></h2>
    <p class="lead">{lead}</p>
    <div class="cta-ctas">
      <a class="btn btn-gold js-wa" href="#" data-msg="{esc(msg)}">{btn}</a>
      <a class="btn btn-line" href="./index.html#contacto">Completar el formulario</a>
    </div>
  </div>
</section>
'''

def write(name, html):
    open(name, "w", encoding="utf8", newline="\n").write(html)
    print("ok", name)

def page(name, title, desc, active, body, ld=None, robots=None):
    write(name, head("./", title, desc, ld, robots=robots) + header("./", active) + "\n<main>\n" + body + "\n</main>\n" + footer("./"))

# ================================================================== NOSOTROS
EQUIPO = [
 dict(img="francisco.jpg", w=1280, h=1280, role="Managing Partner", name="Francisco Casanegra",
      bio="Con una sólida trayectoria en derecho administrativo, ambiental y urbanístico, lidera la estrategia del estudio y asesora a empresas, inversores y organismos públicos. Su experiencia en contrataciones, fideicomisos, proyectos de inversión y litigios complejos le permite ofrecer soluciones jurídicas innovadoras y de alto valor agregado.",
      form=["Abogado — Universidad Nacional de Córdoba", "Magíster en Derecho Administrativo — Universidad Austral",
            "Disertante y autor de publicaciones en Derecho Administrativo y Contrataciones Públicas"],
      chips=["Derecho de la Construcción", "Contrataciones Públicas", "Fideicomisos", "Litigios Estratégicos"],
      link=("https://www.linkedin.com/in/francisco-casanegra-610413191/", "Perfil de LinkedIn")),
 dict(img="paula.jpg", w=1000, h=1339, role="Socia", name="Paula Casanegra",
      bio="Conduce el área de ciudadanía italiana y española, migraciones y derecho internacional. Combina su experiencia profesional con una extensa trayectoria en instituciones consulares y organismos italianos, y brinda un acompañamiento cercano y eficiente en procesos migratorios y de obtención de ciudadanía.",
      form=["Abogada — Universidad Empresarial Siglo 21", "Certificación en idioma italiano — Dante Alighieri",
            "Formación complementaria en idioma inglés y gestión administrativa internacional"],
      chips=["Ciudadanía Italiana", "Ciudadanía Española", "Derecho Migratorio", "Residencias Argentinas", "Trámites Consulares",
             "Gestión Documental Internacional", "Asesoramiento para Extranjeros", "Derecho Internacional Privado"],
      link=None),
]
def perfil(m, i):
    form = "".join(f"<li>{x}</li>" for x in m["form"])
    chips = "".join(f"<li>{x}</li>" for x in m["chips"])
    link = f'<a href="{m["link"][0]}" target="_blank" rel="noopener" class="link-arrow">{m["link"][1]} <i class="ti ti-arrow-up-right"></i></a>' if m["link"] else ""
    return f'''    <article class="perfil{' perfil-rev' if i % 2 else ''} reveal" id="{slugify(m["name"])}">
      <figure><img src="./img/{m["img"]}" alt="{m["name"]}" width="{m["w"]}" height="{m["h"]}" loading="lazy"></figure>
      <div class="perfil-txt">
        <p class="m-role">{m["role"]}</p>
        <h2>{m["name"]}</h2>
        <p class="perfil-bio">{m["bio"]}</p>
        <div class="perfil-cols">
          <div><h3>Formación</h3><ul class="form-list">{form}</ul></div>
          <div><h3>Áreas de experiencia</h3><ul class="chip-list">{chips}</ul></div>
        </div>
        {link}
      </div>
    </article>'''

ld_people = [{"@context": "https://schema.org", "@type": "Person", "name": m["name"], "jobTitle": m["role"],
              "worksFor": {"@type": "LegalService", "name": "Estudio Jurídico Casanegra & Asociados"}} for m in EQUIPO]
nos_side = '''  <figure class="ph-quote rise d3">
    <blockquote>Soluciones que no solo resuelven los conflictos actuales, sino que anticipan los desafíos futuros.</blockquote>
    <figcaption>Asesoramos · Negociamos · Litigamos</figcaption>
  </figure>'''
page("nosotros.html", "Nosotros | Estudio Jurídico Casanegra & Asociados",
     "Conozca al equipo del estudio: Francisco Casanegra, Magíster en Derecho Administrativo, y Paula Casanegra, abogada a cargo de ciudadanías y migraciones. Córdoba.",
     "nosotros.html", ph("nosotros.jpg", "center 55%", "Nosotros", ("Nuestra", "firma."),
     "Un equipo comprometido con la excelencia y la defensa integral de sus intereses.", nos_side, 9419044) + f'''
<!-- ============ COMPROMISO ============ -->
<section class="pg-sec pg-navy">
  <div class="wrap sobre-grid">
    <div class="reveal">
      <p class="eyebrow">Nuestro compromiso</p>
      <h2 class="h2">Excelencia <em>y sustentabilidad.</em></h2>
    </div>
    <div class="sobre-txt reveal">
      <p>Entendemos que el derecho moderno requiere soluciones que no solo resuelvan conflictos actuales, sino que anticipen desafíos futuros, promoviendo el desarrollo equilibrado y la seguridad jurídica a largo plazo.</p>
      <p>Brindamos asesoramiento legal estratégico con una visión integral, para proteger sus intereses en un entorno normativo en constante evolución.</p>
    </div>
  </div>
</section>

<!-- ============ EQUIPO ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/36207471/pexels-photo-36207471.jpeg -->
<section class="pg-sec pg-photo pg-photo-recinto">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Equipo</p>
      <h2 class="h2">Quiénes <em>lo asesoran.</em></h2>
    </div>
    <div class="perfiles">
{chr(10).join(perfil(m, i) for i, m in enumerate(EQUIPO))}
    </div>
  </div>
</section>
''' + cta(("¿Quiere que analicemos", "su caso?"), "Estamos a su disposición para estudiar su situación y ofrecerle el asesoramiento que necesita."), ld_people)

# ================================================================== ÁREAS
from generar_index import GRUPOS
SERVICIOS = [
 ("ti-message-question", "Consultas", "Asesoramiento legal preventivo y resolutivo. Evaluamos escenarios, identificamos riesgos y diseñamos estrategias viables adaptadas a los objetivos de su organización."),
 ("ti-file-certificate", "Dictámenes", "Opiniones jurídicas fundadas sobre situaciones normativas complejas, para respaldar decisiones corporativas o institucionales."),
 ("ti-arrows-exchange", "Mediaciones", "Resolución alternativa de conflictos: acuerdos favorables que eviten el desgaste, los costos y los tiempos de un litigio prolongado."),
 ("ti-file-alert", "Reclamos", "Defensa activa de sus intereses ante organismos estatales o empresas privadas: reclamos administrativos, civiles y comerciales."),
 ("ti-building-bank", "Recursos administrativos", "Impugnación de actos de la Administración Pública y agotamiento de la vía administrativa: reconsideración, jerárquico y alzada."),
 ("ti-gavel", "Acciones judiciales", "Patrocinio y representación ante tribunales provinciales y federales: demandas, amparos y medidas cautelares."),
 ("ti-scale", "Recursos judiciales", "Protección de sus derechos en instancias superiores: apelaciones, casación, inconstitucionalidad y queja."),
]
grupos_html, idx = [], []
tonos = ["pg-navy", "pg-navy-d", "pg-navy"]
for k, (gid, gname, areas) in enumerate(GRUPOS):
    idx.append(f'<li><a href="#{gid}"><span>0{k+1}</span>{gname}</a></li>')
    cards = "\n".join(f'''      <article class="area-card reveal" id="{slugify(t)}">
        <h3>{t}</h3>
        <p>{d}</p>
        <a class="link-arrow js-wa" href="#" data-msg="{esc('Hola, quisiera hacer una consulta sobre ' + t + '.')}">Consultar <i class="ti ti-arrow-right"></i></a>
      </article>''' for t, d in areas)
    grupos_html.append(f'''
<!-- ============ {gname.upper()} ============ -->
<section class="pg-sec {tonos[k]}" id="{gid}">
  <div class="wrap">
    <div class="sec-top reveal">
      <div><p class="eyebrow">0{k+1} · Áreas de práctica</p><h2 class="h2">{gname}.</h2></div>
    </div>
    <div class="area-cards">
{cards}
    </div>
  </div>
</section>''')
idx.append('<li><a href="./ciudadanias.html"><span>04</span>Ciudadanías y migraciones</a></li>')
areas_side = '''  <nav class="ph-index rise d3" aria-label="Grupos de áreas">
    <p class="pf-tag">En esta página</p>
    <ol>''' + "".join(idx) + '''</ol>
  </nav>'''
serv = "\n".join(f'      <li class="reveal"><i class="ti {ic}"></i><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in SERVICIOS)
page("areas.html", "Áreas de práctica | Estudio Jurídico Casanegra & Asociados",
     "Derecho administrativo, ambiental, minero, urbanístico, societario, del inversor, tributario, concursal, penal económico, cobranzas, aduanero, consumidor y lealtad comercial en Córdoba.",
     "areas.html", ph("areas.jpg", "center 50%", "Áreas de práctica", ("Áreas", "de práctica."),
     "Estrategias jurídicas sólidas en sectores clave para el desarrollo empresarial y personal.", areas_side, 11576307)
     + "".join(grupos_html) + f'''

<!-- ============ SERVICIOS ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/13721768/pexels-photo-13721768.jpeg -->
<section class="pg-sec pg-photo pg-photo-columnas" id="servicios">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Servicios jurídicos</p>
      <h2 class="h2">De la prevención <em>a la representación judicial.</em></h2>
    </div>
    <ul class="serv-list">
{serv}
    </ul>
  </div>
</section>
''' + cta(("¿En qué área necesita", "asesoramiento?"), "Cuéntenos su situación y le indicamos cómo podemos intervenir."))

# ================================================================== CIUDADANÍAS
CIU = ["Trámite completo de reconocimiento", "Gestión en la plataforma Fast It", "Inscripción en el padrón AIRE",
       "Actualización de estado civil (matrimonio o divorcio)", "Ciudadanía directa para hijos menores", "Ciudadanía para nietos",
       "Procesos sumarios y juicios por falta de turno", "Inscripción de menores de edad", "Inscripción para mayores de 18 años",
       "Tramitación y renovación de pasaporte", "Ciudadanía para hijos mayores de edad (Ley de Memoria Democrática)",
       "Búsqueda de actas en España", "Legalización y apostillado de documentación"]
MIG = [("ti-home-check", "Residencias en Argentina", "Trámites de radicación precaria, temporaria y permanente para extranjeros."),
       ("ti-plane", "Visas para Estados Unidos", "Asesoramiento para visas de turismo (B1/B2), estudio y trabajo."),
       ("ti-world", "ETIAS (Europa)", "Gestión del nuevo permiso de viaje obligatorio para ingresar al espacio Schengen."),
       ("ti-building-castle", "Visa para el Reino Unido", "Preparación y presentación de expedientes de visado."),
       ("ti-plane-departure", "Autorización ESTA", "Sistema Electrónico para Autorización de Viaje a EE. UU., para países exentos de visa."),
       ("ti-chart-line", "Visas de inversor", "Estructuración legal para obtener visas de inversor extranjero en distintos países.")]
ciu_side = '''  <a class="ph-feat rise d3" href="./articulos/ciudadania-argentina-por-inversion.html">
    <span class="pf-tag">Nuevo programa</span>
    <span class="pf-area">Ciudadanía argentina por inversión</span>
    <span class="pf-t">Dos vías de inversión: u$s 350.000 o u$s 800.000. Modalidades, familiares y evaluación.</span>
    <span class="ac-more">Leer el artículo <i class="ti ti-arrow-right"></i></span>
  </a>'''
ciu_li = "\n".join(f'        <li><i class="ti ti-check"></i>{x}</li>' for x in CIU)
mig = "\n".join(f'      <li class="reveal"><i class="ti {ic}"></i><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in MIG)
page("ciudadanias.html", "Ciudadanía italiana, española y migraciones | Casanegra & Asociados",
     "Ciudadanía italiana y española, Ley de Memoria Democrática, juicios por falta de turno, residencias en Argentina, visas, ETIAS y ESTA. Estudio en Córdoba.",
     "ciudadanias.html", ph("ciudadanias.jpg", "center 50%", "Ciudadanías y migraciones", ("Ciudadanías", "y derecho migratorio."),
     "Soluciones integrales para la movilidad internacional de personas, familias y capitales, simplificando trámites burocráticos y consulares.", ciu_side, 20067918) + f'''
<!-- ============ CIUDADANÍAS EUROPEAS ============ -->
<section class="pg-sec pg-navy">
  <div class="wrap sobre-grid">
    <div class="reveal">
      <p class="eyebrow">Ciudadanías extranjeras</p>
      <h2 class="h2">Italiana <em>y española.</em></h2>
      <p class="lead">Acompañamos cada etapa del reconocimiento, desde la búsqueda de actas hasta el pasaporte.</p>
      <div class="lead-card">
        <img src="./img/paula.jpg" alt="Paula Casanegra" width="1000" height="1339" loading="lazy">
        <div><p class="m-role">Conduce el área</p><p class="lc-name">Paula Casanegra</p><a href="./nosotros.html#paula-casanegra" class="link-arrow">Ver perfil <i class="ti ti-arrow-right"></i></a></div>
      </div>
    </div>
    <ul class="check-list reveal">
{ciu_li}
    </ul>
  </div>
</section>

<!-- ============ MIGRACIONES Y VISAS ============ -->
<section class="pg-sec pg-navy-d">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Migraciones y viajes</p>
      <h2 class="h2">Residencias, <em>visas y permisos.</em></h2>
    </div>
    <ul class="serv-list">
{mig}
    </ul>
  </div>
</section>
''' + cta(("Comencemos", "su trámite."), "Cuéntenos su caso y le indicamos la documentación necesaria y los pasos a seguir.", "Hola, quisiera consultar por un trámite de ciudadanía o migratorio."))

# ================================================================== INVERSIONES
PIL = [("ti-search", "Asesoramiento previo", "Análisis de viabilidad legal y regulatoria (due diligence) para proyectos de inversión nacionales e internacionales."),
       ("ti-shield-lock", "Protección patrimonial", "Diseño de arquitecturas legales para aislar riesgos y proteger activos personales y corporativos."),
       ("ti-coin", "Protección del capital", "Mecanismos jurídicos para resguardar la rentabilidad y la seguridad de los fondos invertidos."),
       ("ti-file-description", "Fideicomisos", "Constitución y administración de fideicomisos de administración, garantía, inmobiliarios y financieros."),
       ("ti-world-dollar", "Inversión extranjera", "Acompañamiento a capitales foráneos: radicación, giro de divisas, beneficios fiscales y cumplimiento normativo.")]
inv_side = '''  <figure class="ph-quote rise d3">
    <blockquote>El diseño legal en la etapa de estructuración puede definir el éxito o el fracaso de un proyecto.</blockquote>
    <figcaption>Derecho del inversor</figcaption>
  </figure>'''
pil = "\n".join(f'      <li class="reveal"><i class="ti {ic}"></i><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in PIL)
page("inversiones.html", "Derecho del inversor e inversiones | Casanegra & Asociados",
     "Due diligence, protección patrimonial y del capital, fideicomisos e inversión extranjera para empresas, desarrolladores e inversores. Estudio en Córdoba.",
     "inversiones.html", ph("inversiones.jpg", "center 40%", "Inversiones", ("Derecho del inversor", "e inversiones."),
     "Para empresas, desarrolladores e inversores que buscan seguridad jurídica y una estructura óptima para sus negocios.", inv_side, 16895158) + f'''
<!-- ============ ENFOQUE ============ -->
<section class="pg-sec pg-navy">
  <div class="wrap sobre-grid">
    <div class="reveal">
      <p class="eyebrow">Creación de valor</p>
      <h2 class="h2">Estructuras flexibles <em>pero robustas.</em></h2>
    </div>
    <div class="sobre-txt reveal">
      <p>Un entorno económico dinámico exige estructuras jurídicas flexibles pero robustas.</p>
      <p>Trabajamos junto a inversores y grupos empresariales para resguardar el capital y asegurar el cumplimiento normativo en cada etapa de la inversión.</p>
    </div>
  </div>
</section>

<!-- ============ PILARES ============ -->
<section class="pg-sec pg-navy-d">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Qué hacemos</p>
      <h2 class="h2">Cinco frentes <em>de la inversión.</em></h2>
    </div>
    <ul class="serv-list">
{pil}
    </ul>
  </div>
</section>

<!-- ============ RELACIONADOS ============ -->
<section class="pg-sec pg-navy">
  <div class="wrap rel-grid">
    <a class="rel-card reveal" href="./articulos/ciudadania-argentina-por-inversion.html"><span class="pf-tag">Artículo</span><span class="pf-t">Ciudadanía argentina por inversión</span><span class="ac-more">Leer <i class="ti ti-arrow-right"></i></span></a>
    <a class="rel-card reveal" href="./areas.html#derecho-societario"><span class="pf-tag">Área</span><span class="pf-t">Derecho societario</span><span class="ac-more">Ver el área <i class="ti ti-arrow-right"></i></span></a>
    <a class="rel-card reveal" href="./areas.html#derecho-tributario"><span class="pf-tag">Área</span><span class="pf-t">Derecho tributario</span><span class="ac-more">Ver el área <i class="ti ti-arrow-right"></i></span></a>
  </div>
</section>
''' + cta(("¿Planificando", "una nueva inversión?"), "Contáctenos para un análisis preliminar de riesgos y oportunidades.", "Hola, quisiera agendar una reunión estratégica por una inversión.", "Agendar una reunión"))

# ================================================================== PRIVACIDAD
page("privacidad.html", "Política de privacidad | Casanegra & Asociados",
     "Cómo trata el Estudio Jurídico Casanegra & Asociados los datos personales recibidos a través de este sitio, conforme a la Ley 25.326.",
     None, ph("columnas-noche.jpg", "center 40%", "Política de privacidad", ("Política", "de privacidad."),
     "Cómo tratamos los datos que nos envía a través de este sitio.", "", 9227831).replace('class="ph ph-img"', 'class="ph ph-img ph-img-short"') + '''
<section class="pg-sec pg-navy legal">
  <div class="wrap legal-in">
    <p class="legal-date">Última actualización: octubre de 2026</p>
    <h2>1. Responsable</h2>
    <p>El responsable del tratamiento es el Estudio Jurídico Casanegra &amp; Asociados, con domicilio en José Gigena 2058, Cerro de las Rosas, Córdoba. Contacto: secretaria@estudiocasanegra.com · +54 351 650-6222.</p>
    <h2>2. Qué datos recopilamos</h2>
    <p>Solo los que usted envía voluntariamente: nombre, empresa (opcional), email, teléfono, el área de su consulta y el mensaje que escribe en el formulario, o los datos que comparte al escribirnos por WhatsApp. El sitio no utiliza cookies de seguimiento ni herramientas de publicidad.</p>
    <h2>3. Para qué los usamos</h2>
    <p>Para responder su consulta, coordinar una reunión y, si decide contratarnos, prestar el servicio. No los usamos para otros fines ni los cedemos a terceros con fines comerciales.</p>
    <h2>4. Secreto profesional</h2>
    <p>La información que nos confía está protegida por el secreto profesional que rige el ejercicio de la abogacía.</p>
    <h2>5. Servicios de terceros</h2>
    <p>Para funcionar, el sitio utiliza servicios externos que pueden procesar datos técnicos (como la dirección IP):</p>
    <ul>
      <li><b>FormSubmit</b>, que envía a nuestro correo los datos del formulario de contacto.</li>
      <li><b>WhatsApp</b> (Meta Platforms), si elige escribirnos por ese medio.</li>
      <li><b>Google Fonts</b> y <b>jsDelivr</b>, que sirven las tipografías y los íconos del sitio.</li>
    </ul>
    <p>Cada uno se rige por su propia política de privacidad.</p>
    <h2>6. Conservación y seguridad</h2>
    <p>Conservamos los datos el tiempo necesario para atender su consulta y cumplir obligaciones legales y profesionales, con medidas razonables de protección.</p>
    <h2>7. Sus derechos</h2>
    <p>Conforme a la Ley 25.326, puede solicitar en forma gratuita el acceso, la rectificación, la actualización o la supresión de sus datos, por los medios indicados en el punto 1. La Agencia de Acceso a la Información Pública, órgano de control de la Ley 25.326, atiende las denuncias y los reclamos por incumplimientos de las normas sobre protección de datos personales.</p>
    <h2>8. Cambios</h2>
    <p>Esta política puede actualizarse. La versión vigente es siempre la publicada en esta página.</p>
  </div>
</section>
''')

# ================================================================== 404
page("404.html", "Página no encontrada | Casanegra & Asociados", "La página que busca no existe o cambió de dirección.", None, '''
<section class="nf">
  <div class="nf-bg" aria-hidden="true"></div>
  <div class="wrap nf-in">
    <span class="nf-num" aria-hidden="true">404</span>
    <h1 class="ph-h1">Esta página <em>no existe.</em></h1>
    <p class="lead">Puede que haya cambiado de dirección. Vuelva al inicio o escríbanos y lo ayudamos.</p>
    <div class="ph-ctas">
      <a class="btn btn-gold" href="./index.html">Volver al inicio</a>
      <a class="btn btn-line js-wa" href="#" data-msg="Hola, quisiera hacer una consulta al estudio.">Consultar por WhatsApp</a>
    </div>
  </div>
</section>''', robots="noindex")
