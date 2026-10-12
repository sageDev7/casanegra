"""Genera index.html con el header/footer compartidos. El bloque de últimos artículos lo completa
publicar.py entre las marcas <!-- ARTICULOS:INICIO --> y <!-- ARTICULOS:FIN -->."""
import os
from comun import head, header, footer, WA_DEF
import re as _re, unicodedata as _ud

def _slug(t):
    t = _ud.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return _re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LD = {"@context": "https://schema.org", "@type": "LegalService", "name": "Estudio Jurídico Casanegra & Asociados",
      "slogan": "Asesoramos, negociamos y litigamos", "telephone": "+54 351 650-6222", "email": "secretaria@estudiocasanegra.com",
      "address": {"@type": "PostalAddress", "streetAddress": "José Gigena 2058", "addressLocality": "Córdoba",
                  "addressRegion": "Córdoba", "addressCountry": "AR"},
      "areaServed": "Argentina",
      "knowsAbout": ["Derecho administrativo", "Derecho ambiental", "Derecho minero", "Derecho urbanístico", "Derecho societario",
                     "Derecho del inversor", "Derecho tributario", "Derecho concursal", "Derecho penal económico", "Derecho aduanero",
                     "Defensa del consumidor", "Lealtad comercial", "Ciudadanías", "Derecho migratorio"],
      "employee": [{"@type": "Person", "name": "Francisco Casanegra", "jobTitle": "Managing Partner"},
                   {"@type": "Person", "name": "Paula Casanegra", "jobTitle": "Socia"}],
      "sameAs": ["https://www.instagram.com/estudio_casanegra", "https://www.facebook.com/estcasanegra",
                 "https://www.linkedin.com/in/francisco-casanegra-610413191/"]}

GRUPOS = [
 ("publico", "Público y regulatorio", [
   ("Derecho Administrativo", "Relación con la Administración Pública en todos sus niveles: licitaciones, contratos públicos y recursos administrativos."),
   ("Derecho Ambiental", "Proyectos compatibles con la protección del ambiente: evaluaciones de impacto y cumplimiento regulatorio."),
   ("Derecho Minero", "Asistencia a la industria extractiva, desde la prospección y la exploración hasta la explotación y el cierre."),
   ("Derecho Urbanístico", "Uso estratégico del suelo y conflictos territoriales: zonificación, loteos y convenios urbanísticos.")]),
 ("empresa", "Empresa e inversión", [
   ("Derecho Societario", "Constitución de sociedades, fusiones, adquisiciones, conflictos societarios y protocolos de empresa familiar."),
   ("Derecho del Inversor", "Protección de capitales, fideicomisos y radicación de inversiones extranjeras con seguridad jurídica."),
   ("Derecho Tributario", "Planificación fiscal, defensa ante determinaciones de oficio y litigio en los niveles nacional, provincial y municipal."),
   ("Derecho Concursal", "Reestructuración de pasivos, concursos preventivos, acuerdos preventivos extrajudiciales y quiebras."),
   ("Penal Económico", "Defensa y querella en fraudes corporativos, evasión tributaria, lavado de activos y compliance penal."),
   ("Gestión de Cobranzas", "Recupero de carteras en mora con gestión extrajudicial y ejecución judicial.")]),
 ("comercio", "Comercio y consumo", [
   ("Derecho Aduanero", "Comercio exterior: importaciones, exportaciones, clasificación arancelaria, valoración e infracciones aduaneras."),
   ("Defensa del Consumidor", "Reclamos individuales y colectivos, denuncias ante organismos y adecuación de prácticas comerciales."),
   ("Lealtad Comercial", "Competencia desleal, publicidad, etiquetado y promociones: defensa y compliance preventivo.")]),
]

def tabs():
    btns, panels = [], []
    for i, (gid, gname, areas) in enumerate(GRUPOS):
        sel = "true" if i == 0 else "false"
        btns.append(f'        <button class="tab" role="tab" id="t-{gid}" aria-controls="p-{gid}" aria-selected="{sel}"{"" if i == 0 else " tabindex=\"-1\""}><span>0{i+1}</span>{gname}</button>')
        items = "\n".join(f'          <li><a href="./areas.html#{_slug(t)}"><h3>{t}</h3><p>{d}</p></a></li>' for t, d in areas)
        panels.append(f'''      <div class="tab-panel{' on' if i == 0 else ''}" role="tabpanel" id="p-{gid}" aria-labelledby="t-{gid}"{'' if i == 0 else ' hidden'}>
        <ul class="area-list">
{items}
        </ul>
      </div>''')
    return "\n".join(btns), "\n".join(panels)

BTNS, PANELS = tabs()

BODY = f'''
<main>

<!-- ============ HERO ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/5720170/pexels-photo-5720170.jpeg -->
<section class="hero" id="inicio">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <p class="eyebrow rise">Estudio jurídico · Córdoba</p>
    <h1 class="hero-h1 split-words"><span class="hv"><i aria-hidden="true">I</i>Asesoramos,</span> <span class="hv"><i aria-hidden="true">II</i>negociamos</span> <em class="hv"><i aria-hidden="true">III</i>y&nbsp;litigamos.</em></h1>
    <p class="hero-sub rise d2">Soluciones jurídicas para empresas, inversores y personas en áreas de alta complejidad normativa: derecho público, societario, tributario, aduanero, ciudadanías e inversiones.</p>
    <div class="hero-ctas rise d3">
      <a class="btn btn-gold js-wa" href="#" data-msg="{WA_DEF}">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="#contacto">Completar el formulario</a>
    </div>
  </div>
  <!-- sello: retoma el badge circular del logo original -->
  <div class="hero-seal rise d3" aria-hidden="true">
    <svg viewBox="0 0 300 300">
      <defs><path id="sealPath" d="M150,150 m-121,0 a121,121 0 1,1 242,0 a121,121 0 1,1 -242,0"/></defs>
      <circle class="seal-ring" cx="150" cy="150" r="146"/>
      <circle class="seal-ring seal-ring-in" cx="150" cy="150" r="98"/>
      <g class="seal-rot"><text><textPath href="#sealPath" textLength="752" lengthAdjust="spacing">ASESORAMOS · NEGOCIAMOS · LITIGAMOS · CÓRDOBA · </textPath></text></g>
    </svg>
    <span class="seal-c">&amp;</span>
  </div>
  <ul class="hero-social rise d4" aria-label="Redes del estudio">
    <li><a href="https://www.instagram.com/estudio_casanegra" target="_blank" rel="noopener" aria-label="Instagram"><i class="ti ti-brand-instagram"></i></a></li>
    <li><a href="https://www.facebook.com/estcasanegra" target="_blank" rel="noopener" aria-label="Facebook"><i class="ti ti-brand-facebook"></i></a></li>
    <li><a href="https://www.linkedin.com/in/francisco-casanegra-610413191/" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="ti ti-brand-linkedin"></i></a></li>
  </ul>
  <ul class="hero-marks rise d4" aria-label="Ejes del estudio">
    <li><b>Derecho público</b><span>y regulatorio</span></li>
    <li><b>Empresa e inversión</b><span>societario, tributario, concursal</span></li>
    <li><b>Ciudadanías</b><span>y migraciones</span></li>
  </ul>
</section>

<!-- ============ TRES VERBOS ============ -->
<section class="verbos" id="servicios">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Cómo intervenimos</p>
      <h2 class="h2">De la prevención <em>a la representación judicial.</em></h2>
      <p class="lead">Un abordaje integral para cada necesidad legal, en tres momentos.</p>
    </div>
    <ol class="verbos-grid">
      <li class="reveal">
        <span class="v-n">I</span>
        <h3>Asesoramos</h3>
        <p>Evaluamos escenarios, identificamos riesgos y diseñamos estrategias viables.</p>
        <ul><li>Consultas preventivas y resolutivas</li><li>Dictámenes jurídicos fundados</li></ul>
      </li>
      <li class="reveal">
        <span class="v-n">II</span>
        <h3>Negociamos</h3>
        <p>Buscamos acuerdos favorables que eviten el desgaste, los costos y los tiempos de un litigio.</p>
        <ul><li>Mediaciones</li><li>Reclamos ante organismos y empresas</li></ul>
      </li>
      <li class="reveal">
        <span class="v-n">III</span>
        <h3>Litigamos</h3>
        <p>Representación ante tribunales provinciales y federales, y en instancias superiores.</p>
        <ul><li>Recursos administrativos</li><li>Demandas, amparos y medidas cautelares</li><li>Apelaciones, casación e inconstitucionalidad</li></ul>
      </li>
    </ol>
  </div>
</section>

<!-- ============ ÁREAS ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/13721768/pexels-photo-13721768.jpeg -->
<section class="areas" id="areas">
  <div class="wrap">
    <div class="sec-top reveal">
      <div>
        <p class="eyebrow">Áreas de práctica</p>
        <h2 class="h2">Derecho de alta <em>complejidad normativa.</em></h2>
      </div>
      <a href="./areas.html" class="link-arrow">Ver todas las áreas <i class="ti ti-arrow-right"></i></a>
    </div>
    <div class="tabs reveal">
      <div class="tab-list" role="tablist" aria-label="Grupos de áreas">
{BTNS}
      </div>
{PANELS}
    </div>
  </div>
</section>

<!-- ============ CIUDADANÍAS E INVERSIÓN ============ -->
<section class="destacado" id="ciudadanias">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Movilidad global</p>
      <h2 class="h2">Ciudadanías, <em>migraciones e inversión.</em></h2>
    </div>
    <div class="dest-grid">
      <article class="dest-card dest-main reveal">
        <p class="dest-tag">Programa de ciudadanía por inversión</p>
        <h3>Ciudadanía argentina por inversión</h3>
        <p>Argentina anunció un programa con dos vías de inversión. Está previsto que reciba solicitudes durante el cuarto trimestre de 2026, sujeto a la reglamentación vigente.</p>
        <ul class="dest-cifras">
          <li><b>u$s <span class="count" data-to="350" data-sep="1">350</span>.000</b><small>aporte al Tesoro Nacional</small></li>
          <li><b>u$s <span class="count" data-to="800" data-sep="1">800</span>.000</b><small>adquisición de un título público</small></li>
        </ul>
        <a href="./articulos/ciudadania-argentina-por-inversion.html" class="link-arrow">Modalidades y requisitos <i class="ti ti-arrow-right"></i></a>
      </article>
      <article class="dest-card reveal">
        <p class="dest-tag">Ciudadanías europeas</p>
        <h3>Italiana y española</h3>
        <p>Trámite completo de reconocimiento, inscripción en el AIRE, juicios por falta de turno, Ley de Memoria Democrática y apostillado.</p>
        <a href="./ciudadanias.html" class="link-arrow">Ver el servicio <i class="ti ti-arrow-right"></i></a>
      </article>
      <article class="dest-card reveal">
        <p class="dest-tag">Migraciones y visas</p>
        <h3>Residencias y viajes</h3>
        <p>Radicaciones en Argentina, visas para Estados Unidos y el Reino Unido, ETIAS, ESTA y visas de inversor.</p>
        <a href="./ciudadanias.html" class="link-arrow">Ver el servicio <i class="ti ti-arrow-right"></i></a>
      </article>
    </div>
  </div>
</section>

<!-- ============ EQUIPO ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/36207471/pexels-photo-36207471.jpeg -->
<section class="equipo" id="equipo">
  <div class="wrap">
    <div class="sec-top reveal">
      <div>
        <p class="eyebrow">Nuestra firma</p>
        <h2 class="h2">Quiénes <em>lo asesoran.</em></h2>
      </div>
      <a href="./nosotros.html" class="link-arrow">Conocer al equipo <i class="ti ti-arrow-right"></i></a>
    </div>
    <div class="team">
      <article class="member reveal">
        <figure><img src="./img/francisco.jpg" alt="Francisco Casanegra" width="1280" height="1280" loading="lazy"></figure>
        <div>
          <p class="m-role">Managing Partner</p>
          <h3>Francisco Casanegra</h3>
          <p class="m-cred">Abogado (UNC) · Magíster en Derecho Administrativo (Universidad Austral)</p>
          <p>Lidera la estrategia del estudio en derecho administrativo, ambiental y urbanístico, con trayectoria en contrataciones públicas, fideicomisos, proyectos de inversión y litigios complejos.</p>
        </div>
      </article>
      <article class="member reveal">
        <figure><img src="./img/paula.jpg" alt="Paula Casanegra" width="1000" height="1339" loading="lazy"></figure>
        <div>
          <p class="m-role">Socia</p>
          <h3>Paula Casanegra</h3>
          <p class="m-cred">Abogada (Universidad Siglo 21) · Certificación en idioma italiano (Dante Alighieri)</p>
          <p>Conduce el área de ciudadanía italiana y española, migraciones y derecho internacional, con trayectoria en instituciones consulares y organismos italianos.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ============ ARTÍCULOS ============ -->
<section class="art-sec" id="articulos">
  <div class="wrap">
    <div class="sec-top reveal">
      <div>
        <p class="eyebrow">Artículos y novedades</p>
        <h2 class="h2">Análisis normativo <em>y jurisprudencia.</em></h2>
      </div>
      <a href="./articulos.html" class="link-arrow">Ver todos los artículos <i class="ti ti-arrow-right"></i></a>
    </div>
<!-- ARTICULOS:INICIO -->
<!-- ARTICULOS:FIN -->
  </div>
</section>

<!-- ============ CONTACTO ============ -->
<!-- foto de fondo: https://images.pexels.com/photos/9227831/pexels-photo-9227831.jpeg -->
<section class="contacto" id="contacto">
  <div class="contacto-bg" aria-hidden="true"></div>
  <div class="wrap contacto-grid">
    <div class="contacto-info reveal">
      <p class="eyebrow">Contacto</p>
      <h2 class="h2">Analicemos <em>su caso.</em></h2>
      <p class="lead">Estamos a su disposición para estudiar su situación y ofrecerle el asesoramiento que necesita.</p>
      <ul class="datos">
        <li><span class="ic"><i class="ti ti-brand-whatsapp"></i></span><div><small>WhatsApp</small><a class="js-wa" href="#" data-msg="{WA_DEF}">+54 351 650-6222</a></div></li>
        <li><span class="ic"><i class="ti ti-phone"></i></span><div><small>Teléfono</small><a href="tel:+543512016540">+54 351 201-6540</a></div></li>
        <li><span class="ic"><i class="ti ti-mail"></i></span><div><small>Email</small><a href="mailto:secretaria@estudiocasanegra.com">secretaria@estudiocasanegra.com</a></div></li>
        <li><span class="ic"><i class="ti ti-map-pin"></i></span><div><small>Estudio</small><span>José Gigena 2058, Cerro de las Rosas, Córdoba</span></div></li>
      </ul>
    </div>
    <div class="form-card reveal">
      <h3>Envíenos su consulta</h3>
      <p>Le respondemos a la brevedad.</p>
      <iframe name="formsubmit-iframe" id="formsubmit-iframe" title="Envío del formulario" style="display:none"></iframe>
      <form id="contactForm" action="https://formsubmit.co/secretaria@estudiocasanegra.com" method="POST" target="formsubmit-iframe" novalidate>
        <input type="hidden" name="_subject" value="Nueva consulta desde estudiocasanegra.com">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="about:blank">
        <input type="hidden" name="_template" value="table">
        <div class="hp" aria-hidden="true"><input type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
        <div class="f-row">
          <div class="field"><label for="fNombre">Nombre completo</label><input id="fNombre" name="nombre" type="text" autocomplete="name" required><span class="msg">Ingrese su nombre.</span></div>
          <div class="field"><label for="fEmpresa">Empresa <small>(opcional)</small></label><input id="fEmpresa" name="empresa" type="text" autocomplete="organization"></div>
        </div>
        <div class="f-row">
          <div class="field"><label for="fEmail">Email</label><input id="fEmail" name="email" type="email" autocomplete="email" required><span class="msg">Ingrese un email válido.</span></div>
          <div class="field"><label for="fTel">Teléfono</label><input id="fTel" name="telefono" type="tel" autocomplete="tel" required><span class="msg">Ingrese un teléfono.</span></div>
        </div>
        <div class="field"><label for="fArea">Área de práctica</label>
          <select id="fArea" name="area" required>
            <option value="">Seleccione el área de su interés</option>
            <optgroup label="Público y regulatorio"><option>Derecho Administrativo</option><option>Derecho Ambiental</option><option>Derecho Minero</option><option>Derecho Urbanístico</option></optgroup>
            <optgroup label="Empresa e inversión"><option>Derecho Societario</option><option>Derecho del Inversor</option><option>Derecho Tributario</option><option>Derecho Concursal</option><option>Penal Económico</option><option>Gestión de Cobranzas</option></optgroup>
            <optgroup label="Comercio y consumo"><option>Derecho Aduanero</option><option>Defensa del Consumidor</option><option>Lealtad Comercial</option></optgroup>
            <optgroup label="Movilidad global"><option>Ciudadanías europeas</option><option>Ciudadanía argentina por inversión</option><option>Migraciones y visas</option></optgroup>
            <option>Otra consulta</option>
          </select>
          <span class="msg">Seleccione un área.</span>
        </div>
        <div class="field"><label for="fMsg">Consulta</label><textarea id="fMsg" name="consulta" required></textarea><span class="msg">Detalle brevemente su consulta.</span></div>
        <button type="submit" class="btn btn-gold" id="formSubmitBtn">Enviar consulta</button>
      </form>
    </div>
  </div>
</section>

</main>

<div class="modal" id="okModal" role="dialog" aria-modal="true" aria-labelledby="okTitle">
  <div class="modal-card">
    <i class="ti ti-circle-check"></i>
    <h3 id="okTitle">Consulta enviada</h3>
    <p>Gracias por escribirnos. Le respondemos a la brevedad.</p>
    <button type="button" class="btn btn-gold" data-close>Cerrar</button>
  </div>
</div>
'''

if __name__ == "__main__":
    html = head("./", "Estudio Jurídico Casanegra & Asociados | Abogados en Córdoba",
                "Estudio jurídico en Córdoba: derecho administrativo, ambiental, societario, tributario, aduanero, del inversor, ciudadanías y migraciones. Asesoramos, negociamos y litigamos.",
                LD) + header("./") + BODY + footer("./")
    open(os.path.join(D, "index.html"), "w", encoding="utf8", newline="\n").write(html)
    print("ok index.html")

    # el bloque de últimos artículos lo completa publicar.py: se corre siempre a continuación
    import publicar
    publicar.main()
