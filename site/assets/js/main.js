/* Topography Consulting LLC: site interactions.
   No dependencies. Everything here is progressive: the pages are complete
   and readable without JavaScript, and motion is skipped for visitors who
   prefer reduced motion. */
(function () {
  "use strict";

  var doc = document.documentElement;
  var reduceMQ = window.matchMedia("(prefers-reduced-motion: reduce)");
  var reduce = reduceMQ.matches;
  var raf = window.requestAnimationFrame.bind(window);
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /* ------------------------------------------------------------------
     Header: transparent over the dark hero, solid once the page scrolls
     ------------------------------------------------------------------ */
  var header = document.querySelector("[data-header]");
  function updateHeader() {
    if (header) header.classList.toggle("is-solid", window.scrollY > 24);
  }

  /* ------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  function setNav(open, returnFocus) {
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    ["main", "footer"].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) el.inert = open;
    });
    if (open) {
      var first = nav.querySelector("a");
      if (first) first.focus();
    } else if (returnFocus) {
      toggle.focus();
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!document.body.classList.contains("nav-open"), true);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false, false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) setNav(false, true);
    });
    window.matchMedia("(min-width: 821px)").addEventListener("change", function (e) {
      if (e.matches && document.body.classList.contains("nav-open")) setNav(false, false);
    });
  }

  /* ------------------------------------------------------------------
     Scroll reveals
     ------------------------------------------------------------------ */
  var revealEls = document.querySelectorAll(".reveal, .reveal-img, .intro__trace");
  revealEls.forEach(function (el) {
    // gentle stagger among sibling reveals
    if (!el.classList.contains("reveal") || el.style.getPropertyValue("--d")) return;
    var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.classList.contains("reveal"); });
    var i = sibs.indexOf(el);
    if (i > 0) el.style.setProperty("--d", Math.min(i, 3) * 80 + "ms");
  });
  if ("IntersectionObserver" in window && !reduce) {
    // Elements revealed with clip-path start fully clipped, which the observer
    // treats as invisible, so their parent is observed instead.
    var watched = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        (watched.get(en.target) || []).forEach(function (el) { el.classList.add("is-in"); });
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) {
      var target = el.classList.contains("reveal") ? el : el.parentElement;
      if (!watched.has(target)) watched.set(target, []);
      watched.get(target).push(el);
      io.observe(target);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ------------------------------------------------------------------
     Signature animation: the approved logo draws itself, opens a route
     through its contours, then closes into the exact approved mark.
     The animated copies are temporary; the original vector is restored
     untouched when the sequence ends.
     ------------------------------------------------------------------ */
  var NS = "http://www.w3.org/2000/svg";
  var mark = document.querySelector("[data-mark]");
  var hero = document.querySelector("[data-hero]");
  var rings = document.querySelector("[data-rings]");
  // Emblem centre and outer radius in the logo's own coordinates.
  var EMBLEM = { x: 510, y: 426, r: 232 };
  var CUT = 512.5;            // vertical line through the north point
  var T = 1900;               // total sequence length (ms)
  var ringState = { plateau: 0, start: 0, end: 0, intro: 0, ready: false };

  function layoutRings() {
    if (!mark || !hero || !rings) return;
    var vb = mark.viewBox.baseVal;
    var m = mark.getBoundingClientRect(), h = hero.getBoundingClientRect();
    if (!m.width) return;
    var k = m.width / vb.width;
    var size = EMBLEM.r * k * (1600 / 150);       // field plateau is r=150 of 1600
    rings.style.setProperty("--cx", (m.left - h.left + (EMBLEM.x - vb.x) * k).toFixed(1) + "px");
    rings.style.setProperty("--cy", (m.top - h.top + (EMBLEM.y - vb.y) * k).toFixed(1) + "px");
    rings.style.setProperty("--size", size.toFixed(0) + "px");
    var step = size * 28 / 1600;
    ringState.plateau = size * 150 / 1600 - 2;
    ringState.start = ringState.plateau + step * 3.2;
    ringState.end = size * 0.72;
    ringState.ready = true;
  }

  function updateRings() {
    if (!ringState.ready || !rings) return;
    if (reduce) { rings.style.setProperty("--r", ringState.end + "px"); return; }
    var p = clamp(window.scrollY / Math.max(1, hero.offsetHeight * 0.85), 0, 1);
    var eased = 1 - Math.pow(1 - p, 2);
    var base = ringState.plateau + (ringState.start - ringState.plateau) * ringState.intro;
    var r = base + (ringState.end - ringState.start) * eased;
    rings.style.setProperty("--r", r.toFixed(1) + "px");
  }

  function tween(ms, fn, done) {
    var t0 = performance.now();
    (function step(now) {
      var t = clamp((now - t0) / ms, 0, 1);
      fn(1 - Math.pow(1 - t, 3));
      if (t < 1) raf(step); else if (done) done();
    })(t0);
  }

  function animateMark() {
    var art = mark.querySelector(".mark__art");
    var word = mark.querySelector(".mark__word");
    var route = mark.querySelector(".mark__route");
    var vb = mark.viewBox.baseVal;
    var k = mark.getBoundingClientRect().width / vb.width || 1;

    var defs = document.createElementNS(NS, "defs");
    defs.innerHTML =
      '<clipPath id="mk-l"><rect x="' + (vb.x - 60) + '" y="' + (vb.y - 60) + '" width="' + (CUT - vb.x + 60) + '" height="' + (vb.height + 120) + '"/></clipPath>' +
      '<clipPath id="mk-r"><rect x="' + CUT + '" y="' + (vb.y - 60) + '" width="' + (vb.x + vb.width - CUT + 60) + '" height="' + (vb.height + 120) + '"/></clipPath>';
    mark.appendChild(defs);

    var anims = [];
    var stroke = (1.15 / k).toFixed(2);
    var ease = "cubic-bezier(.65,0,.35,1)";
    var order = { waves: 0, mountains: 110, summit: 220, compass: 300, ring: 380 };

    var halves = ["l", "r"].map(function (side) {
      var wrap = document.createElementNS(NS, "g");
      wrap.setAttribute("clip-path", "url(#mk-" + side + ")");
      var copy = art.cloneNode(true);
      copy.removeAttribute("class");
      wrap.appendChild(copy);
      mark.insertBefore(wrap, route);
      // Stage 2: the halves part to open a route, then close again.
      var dx = side === "l" ? -16 : 16;
      anims.push(copy.animate({
        transform: ["translateX(0px)", "translateX(0px)", "translateX(" + dx + "px)", "translateX(" + dx + "px)", "translateX(0px)"],
        offset: [0, .2, .4, .6, .84],
        easing: ease
      }, { duration: T, fill: "both" }));
      // Stage 1: each contour draws on as an outline; Stage 3: it fills in.
      copy.querySelectorAll(".mark__g").forEach(function (g) {
        var base = order[g.getAttribute("data-g")] || 0;
        g.querySelectorAll("path").forEach(function (p, i) {
          var d0 = (base + i * 40) / T, d1 = Math.min(.62, d0 + 720 / T);
          p.setAttribute("pathLength", "1");
          p.setAttribute("stroke", "#FFFFFF");
          p.setAttribute("stroke-width", stroke);
          p.setAttribute("stroke-dasharray", "1 1");
          anims.push(p.animate({ strokeDashoffset: [1, 1, 0, 0], offset: [0, d0, d1, 1], easing: ease }, { duration: T, fill: "both" }));
          anims.push(p.animate({ fillOpacity: [0, 0, 1], offset: [0, .62, .86] }, { duration: T, fill: "both" }));
          anims.push(p.animate({ strokeOpacity: [1, 1, 0], offset: [0, .66, .88] }, { duration: T, fill: "both" }));
        });
      });
      return wrap;
    });
    art.style.visibility = "hidden";

    // The copper route traces the opening, then fades as the halves close.
    anims.push(route.animate({
      opacity: [0, 0, 1, 1, 0],
      strokeDashoffset: [1, 1, 1, 0, 0],
      offset: [0, .34, .35, .64, .9],
      easing: ease
    }, { duration: T, fill: "both" }));
    // Wordmark settles in last.
    anims.push(word.animate({
      opacity: [0, 0, 1],
      transform: ["translateY(14px)", "translateY(14px)", "translateY(0px)"],
      offset: [0, .66, 1],
      easing: "cubic-bezier(.16,1,.3,1)"
    }, { duration: T, fill: "both" }));

    mark.setAttribute("data-anim", "running");

    // Stage 4 begins as the mark completes: the first rings open out.
    setTimeout(function () {
      tween(900, function (t) { ringState.intro = t; updateRings(); });
    }, T * 0.7);

    Promise.all(anims.map(function (a) { return a.finished; })).then(function () {
      // Restore the untouched approved vector.
      halves.forEach(function (h) { h.remove(); });
      defs.remove();
      art.style.visibility = "";
      anims.forEach(function (a) { a.cancel(); });
      mark.setAttribute("data-anim", "done");
    }).catch(function () {});
  }

  if (mark) {
    // On narrow screens the header already shows the full lockup, so the hero
    // uses the approved emblem-only crop (same vectors, icon viewBox).
    var FULL_VB = mark.getAttribute("viewBox"), ICON_VB = "270.9 189.4 474.6 474.6";
    var small = window.matchMedia("(max-width: 899px)");
    var applyViewBox = function () { mark.setAttribute("viewBox", small.matches ? ICON_VB : FULL_VB); };
    applyViewBox();
    small.addEventListener("change", function () { applyViewBox(); layoutRings(); updateRings(); });
    var canAnimate = !reduce && typeof mark.animate === "function" && window.Animation && "finished" in window.Animation.prototype;
    layoutRings();
    if (canAnimate) {
      ringState.intro = 0;
      try { animateMark(); } catch (e) { mark.setAttribute("data-anim", "done"); ringState.intro = 1; }
    } else {
      mark.setAttribute("data-anim", "done");
      ringState.intro = 1;
    }
    updateRings();
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { layoutRings(); updateRings(); }, 120);
    });
  }

  /* ------------------------------------------------------------------
     Scroll loop (header + hero rings)
     ------------------------------------------------------------------ */
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    raf(function () { ticking = false; updateHeader(); updateRings(); });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  updateHeader();

  /* ------------------------------------------------------------------
     Home: service rows drive the image beside them (desktop)
     ------------------------------------------------------------------ */
  var svcRoot = document.querySelector("[data-svc-root]");
  if (svcRoot) {
    var items = svcRoot.querySelectorAll("[data-svc]");
    var imgs = svcRoot.querySelectorAll("[data-svc-img]");
    var setActive = function (idx) {
      items.forEach(function (it) { it.classList.toggle("is-active", it.getAttribute("data-svc") === idx); });
      imgs.forEach(function (im) { im.classList.toggle("is-active", im.getAttribute("data-svc-img") === idx); });
    };
    items.forEach(function (it) {
      var idx = it.getAttribute("data-svc");
      it.addEventListener("mouseenter", function () { setActive(idx); });
      it.addEventListener("focusin", function () { setActive(idx); });
    });
    setActive("0");
  }

  /* ------------------------------------------------------------------
     Services: accordion (content is in the HTML and open without JS)
     ------------------------------------------------------------------ */
  var accRoot = document.querySelector("[data-acc]");
  if (accRoot) {
    var setItem = function (btn, open) {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", String(open));
      if (open) panel.removeAttribute("data-closed"); else panel.setAttribute("data-closed", "");
    };
    var buttons = accRoot.querySelectorAll("[data-acc-btn]");
    var openFromHash = function () {
      var id = decodeURIComponent(location.hash.slice(1));
      var target = id && document.getElementById(id);
      if (target && target.classList.contains("acc__item")) {
        setItem(target.querySelector("[data-acc-btn]"), true);
        return true;
      }
      return false;
    };
    buttons.forEach(function (b) { setItem(b, false); });
    openFromHash();
    buttons.forEach(function (b) {
      b.addEventListener("click", function () { setItem(b, b.getAttribute("aria-expanded") !== "true"); });
    });
    window.addEventListener("hashchange", openFromHash);
  }

  /* ------------------------------------------------------------------
     Contact form
     mode "email":    no form service configured yet; composes an email
                      in the visitor's mail app and says so plainly.
     mode "endpoint": posts to the configured form service with loading,
                      success and error states.
     ------------------------------------------------------------------ */
  var form = document.querySelector("[data-form]");
  if (form) {
    var status = form.querySelector("[data-form-status]");
    var submit = form.querySelector("[type=submit]");
    var submitHTML = submit.innerHTML;
    var email = form.getAttribute("data-email");
    var rules = {
      name: function (v) { return v.trim() ? "" : "Please enter your name."; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Please enter a valid email address."; },
      message: function (v) { return v.trim().length >= 10 ? "" : "Please add a short message (at least 10 characters)."; }
    };
    var showError = function (name, msg) {
      var input = form.elements[name];
      var err = document.getElementById(input.id + "-error");
      input.setAttribute("aria-invalid", msg ? "true" : "false");
      err.textContent = msg;
      err.hidden = !msg;
    };
    var setStatus = function (msg, kind) {
      status.textContent = msg;
      status.className = "form__status" + (kind ? " is-" + kind : "");
    };
    Object.keys(rules).forEach(function (name) {
      form.elements[name].addEventListener("input", function () {
        if (this.getAttribute("aria-invalid") === "true") showError(name, rules[name](this.value));
      });
      form.elements[name].addEventListener("blur", function () {
        if (this.value) showError(name, rules[name](this.value));
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      Object.keys(rules).forEach(function (name) {
        var msg = rules[name](form.elements[name].value);
        showError(name, msg);
        if (msg && !firstBad) firstBad = form.elements[name];
      });
      if (firstBad) { setStatus("Please check the highlighted fields.", "error"); firstBad.focus(); return; }
      if (form.elements._gotcha && form.elements._gotcha.value) return; // likely a bot

      var f = new FormData(form);
      if (form.getAttribute("data-mode") !== "endpoint") {
        var subject = "Website inquiry: " + (f.get("interest") || "General");
        var body = "Name: " + f.get("name") + "\nCompany: " + (f.get("company") || "") +
          "\nEmail: " + f.get("email") + "\nArea of interest: " + f.get("interest") + "\n\n" + f.get("message");
        window.location.href = "mailto:" + email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        setStatus("Your email app should open with this message ready to send. If it does not, please write to " + email + ".", "");
        return;
      }

      submit.disabled = true;
      form.setAttribute("aria-busy", "true");
      submit.textContent = "Sending…";
      setStatus("", "");
      fetch(form.action, { method: "POST", body: f, headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          form.reset();
          setStatus("Thank you. Your message has been sent and Marcie will reply by email.", "success");
        })
        .catch(function () {
          setStatus("Sorry, the message could not be sent. Please email " + email + " directly.", "error");
        })
        .then(function () {
          submit.disabled = false;
          form.removeAttribute("aria-busy");
          submit.innerHTML = submitHTML;
        });
    });
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
