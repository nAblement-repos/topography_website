/* Topography Consulting — interactions (kept deliberately quiet) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header: transparent over hero, solid after scrolling, tucks away on scroll down */
  var header = document.querySelector(".site-header");
  var lastY = window.scrollY;
  function onScrollHeader() {
    var y = window.scrollY;
    if (!header) return;
    header.classList.toggle("is-solid", y > 60);
    if (!document.body.classList.contains("nav-open")) {
      header.classList.toggle("is-hidden", y > 700 && y > lastY + 2);
      if (y < lastY - 2) header.classList.remove("is-hidden");
    }
    lastY = y;
  }

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    document.querySelectorAll(".nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) toggle.click();
    });
  }

  /* Prepare line-drawing SVGs */
  document.querySelectorAll(".draw path").forEach(function (p) {
    try { p.style.setProperty("--len", Math.ceil(p.getTotalLength())); } catch (e) {}
  });

  /* Reveal on scroll */
  var targets = document.querySelectorAll(".reveal, .draw, .range");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          if (en.target.classList.contains("range")) {
            var line = en.target.querySelector(".range__line");
            if (line) line.style.setProperty("--p", "100%");
          }
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) {
      t.classList.add("is-in");
      var line = t.querySelector && t.querySelector(".range__line");
      if (line) line.style.setProperty("--p", "100%");
    });
  }

  /* Gentle parallax on hero + image bands */
  var para = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));

  /* Depth gauge: reads scroll as fathoms of descent — a quiet nod to charts */
  var gauge = document.querySelector(".gauge");
  var mark = gauge && gauge.querySelector(".gauge__mark");
  var val = gauge && gauge.querySelector(".gauge__val");

  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY, vh = window.innerHeight;
    onScrollHeader();
    para.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      var offset = (r.top + r.height / 2 - vh / 2) * -speed;
      var cap = r.height * 0.09; offset = Math.max(-cap, Math.min(cap, offset));
      el.style.transform = "translate3d(0," + offset.toFixed(1) + "px,0)";
    });
    if (gauge) {
      var max = Math.max(1, doc.scrollHeight - vh);
      var p = Math.min(1, Math.max(0, y / max));
      mark.style.top = (p * 140).toFixed(1) + "px";
      val.textContent = "DEPTH " + String(Math.round(p * 1200)).padStart(4, "0") + " M";
    }
  }
  function requestFrame() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", requestFrame);
  frame();

  /* Contact form → composes an email (static site, no backend required) */
  var form = document.querySelector("[data-mailto-form]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var f = new FormData(form);
      var subject = "Inquiry: " + (f.get("topic") || "General") + " — " + (f.get("name") || "");
      var body =
        "Name: " + (f.get("name") || "") + "\n" +
        "Organization: " + (f.get("org") || "") + "\n" +
        "Role / sector: " + (f.get("sector") || "") + "\n" +
        "Email: " + (f.get("email") || "") + "\n\n" +
        (f.get("message") || "");
      window.location.href = "mailto:marcie@topographyllc.com?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
