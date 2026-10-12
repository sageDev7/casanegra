(function () {
  "use strict";
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- WhatsApp: un solo número para todos los botones ---------- */
  var WA_NUMBER = "543516506222";
  document.querySelectorAll(".js-wa").forEach(function (a) {
    var msg = a.getAttribute("data-msg") || "Hola, quisiera hacer una consulta al estudio.";
    a.href = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg);
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* ---------- páginas internas todavía no construidas ---------- */
  document.querySelectorAll("[data-soon]").forEach(function (el) {
    el.addEventListener("click", function (e) { e.preventDefault(); });
  });

  /* ---------- header ---------- */
  var hdr = document.getElementById("hdr");
  function onScroll() { hdr.classList.toggle("sc", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- menú mobile (la hamburguesa se transforma en cruz) ---------- */
  var burger = document.getElementById("burger");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }
  burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  document.getElementById("mnavOv").addEventListener("click", function () { setNav(false); });
  document.querySelectorAll(".mnav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });

  /* ---------- título: entra palabra por palabra (el &nbsp; mantiene palabras juntas) ---------- */
  var wordIdx = 0;
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/([ \t\n\r]+)/).forEach(function (part) {
          if (!part) return;
          if (/^[ \t\n\r]+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span");
          w.className = "w";
          w.textContent = part;
          w.style.animationDelay = (0.2 + wordIdx++ * 0.08) + "s";
          frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== "BR") {
        splitWords(n);
      }
    });
  }
  if (!reduce) document.querySelectorAll(".split-words").forEach(splitWords);

  /* ---------- contadores ---------- */
  function runCount(el) {
    var to = parseFloat(el.getAttribute("data-to")), pre = el.getAttribute("data-prefix") || "";
    var dur = 1800, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 4);
      el.textContent = pre + Math.round(to * e);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = pre + "0";
    requestAnimationFrame(step);
  }
  if (!reduce && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    document.querySelectorAll(".count").forEach(function (el) { cio.observe(el); });
  }

  /* ---------- áreas: pestañas (accesibles con teclado) ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));
  function selectTab(t, focus) {
    tabs.forEach(function (o) {
      var on = o === t, panel = document.getElementById(o.getAttribute("aria-controls"));
      o.setAttribute("aria-selected", on ? "true" : "false");
      o.tabIndex = on ? 0 : -1;
      panel.hidden = !on;
    });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        e.preventDefault();
        selectTab(tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length], true);
      }
    });
  });

  /* ---------- listado de artículos: filtro por área ---------- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.getAttribute("data-filter"), visibles = 0;
      chips.forEach(function (o) { o.classList.toggle("on", o === c); });
      document.querySelectorAll("#artGrid .art-card").forEach(function (card) {
        var show = f === "todas" || card.getAttribute("data-area") === f;
        card.classList.toggle("off", !show);
        if (show) { visibles++; card.classList.add("in"); }
      });
      var empty = document.getElementById("artEmpty");
      if (empty) empty.hidden = visibles > 0;
    });
  });

  /* ---------- artículo: compartir ---------- */
  document.querySelectorAll("[data-share]").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = location.href.split("#")[0], title = document.title, kind = b.getAttribute("data-share");
      if (kind === "whatsapp") window.open("https://wa.me/?text=" + encodeURIComponent(title + " " + url), "_blank", "noopener");
      if (kind === "linkedin") window.open("https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url), "_blank", "noopener");
      if (kind === "copiar" && navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () {
          b.classList.add("ok"); b.setAttribute("aria-label", "Enlace copiado");
          setTimeout(function () { b.classList.remove("ok"); b.setAttribute("aria-label", "Copiar el enlace"); }, 1800);
        });
      }
    });
  });

  /* ---------- artículo: índice que marca la sección que se está leyendo ---------- */
  var tocLinks = document.querySelectorAll(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.toggle("act", a.getAttribute("href") === "#" + en.target.id); });
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll(".prose h2[id]").forEach(function (h) { tio.observe(h); });
  }

  /* ---------- reveals ---------- */
  var items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- parallax del hero ---------- */
  var heroBg = document.querySelector(".hero-bg, .ph-bg"), ticking = false;
  if (heroBg && !reduce) {
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        if (window.scrollY < window.innerHeight * 1.2) heroBg.style.transform = "translate3d(0," + (window.scrollY * 0.25) + "px,0)";
      });
    }, { passive: true });
  }

  /* ---------- WhatsApp flotante: se oculta en el hero, el contacto y el footer ---------- */
  var fab = document.getElementById("waFloat");
  if (fab && "IntersectionObserver" in window) {
    var hidden = new Set();
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) hidden.add(en.target); else hidden.delete(en.target); });
      fab.classList.toggle("hide", hidden.size > 0);
    });
    document.querySelectorAll(".hero, .ph, #contacto, #ftr").forEach(function (el) { fio.observe(el); });
  }

  /* ---------- formulario (FormSubmit + modal) ---------- */
  var form = document.getElementById("contactForm"), btn = document.getElementById("formSubmitBtn");
  var iframe = document.getElementById("formsubmit-iframe"), modal = document.getElementById("okModal"), sending = false;
  if (form) {
    var valid = function (input) {
      var v = input.value.trim();
      var ok = v !== "" && (input.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
      input.closest(".field").classList.toggle("err", !ok);
      return ok;
    };
    form.addEventListener("submit", function (e) {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (i) { if (!valid(i)) ok = false; });
      if (!ok) { e.preventDefault(); var f = form.querySelector(".field.err input,.field.err select,.field.err textarea"); if (f) f.focus(); return; }
      sending = true; btn.disabled = true; btn.textContent = "Enviando...";
    });
    form.querySelectorAll("[required]").forEach(function (i) {
      i.addEventListener("input", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
      i.addEventListener("change", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
    });
    iframe.addEventListener("load", function () {
      if (!sending) return;
      sending = false; form.reset(); btn.disabled = false; btn.textContent = "Enviar consulta";
      modal.classList.add("show");
    });
    modal.addEventListener("click", function (e) { if (e.target === modal || e.target.hasAttribute("data-close")) modal.classList.remove("show"); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setNav(false); if (modal) modal.classList.remove("show"); }
  });

  document.getElementById("yr").textContent = new Date().getFullYear();
})();
