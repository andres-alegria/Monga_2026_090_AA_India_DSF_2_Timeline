/* Mongabay 2026_090: interactive timeline, compact version.
   Draws content.js into index.html: a list of periods on a shared time axis (tabs) and one reading card.
   Choosing a period (click, tap, arrow keys or the previous / next buttons) swaps the card. The height never
   changes with the choice, only with the width, and the page reports that height to the host page so a
   WordPress post can size the iframe. */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js"); // the static fallback is for browsers without JavaScript
  // ?fill=1: the WordPress shortcode sets the frame's height with a CSS formula; the timeline stretches to fill it
  if (/[?&]fill=1(&|$)/.test(location.search)) document.documentElement.classList.add("is-fill");

  var C = window.DSF_TIMELINE;
  var ICONS = window.DSF_ICONS;
  var AX = C.axis;

  var CFG = {
    start: 0,          // entry shown first (0 = the first period)
    minTickGap: 40,    // px between decade labels below which only every other label shows
    maxHeight: 1000,   // WordPress's iframe resizer caps heights here; the page warns if it grows past it
  };

  // ---------------------------------------------------------------- helpers
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  // **phrase** -> <mark>phrase</mark>: the phrases the reporter set in bold
  function rich(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, "<mark>$1</mark>");
  }
  // position on the time axis, as a percentage of its width
  function pct(year) {
    return ((year - AX.start) / (AX.end - AX.start)) * 100;
  }
  function svg(d) {
    return '<svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>';
  }
  // Phosphor caret-left / caret-right
  var CARET_L = "M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z";
  var CARET_R = "M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z";

  // the mark for one event: a dot for a single year, a bar for a period, a bar with an arrowhead if still running
  function mark(e) {
    var m;
    if (e.ongoing) {
      m = el("span", "tl-bar is-ongoing");
      m.style.left = pct(e.start) + "%";
      m.style.width = pct(AX.end) - pct(e.start) + "%";
    } else if (e.end > e.start) {
      m = el("span", "tl-bar");
      m.style.left = pct(e.start) + "%";
      m.style.width = pct(e.end + 1) - pct(e.start) + "%"; // from the start of the first year to the end of the last
    } else {
      m = el("span", "tl-dot");
      m.style.left = pct(e.start + 0.5) + "%"; // the middle of the year
    }
    return m;
  }
  function guides(scale) {
    AX.ticks.forEach(function (t) {
      var g = el("span", "tl-guide");
      g.style.left = pct(t) + "%";
      scale.appendChild(g);
    });
  }

  // ---------------------------------------------------------------- title block, source, axis labels
  var fig = document.getElementById("tl");
  document.getElementById("tl-title").textContent = C.title;
  document.getElementById("tl-deck").textContent = C.deck;
  document.getElementById("tl-source").textContent = C.source;

  var ticks = document.getElementById("tl-ticks");
  AX.ticks.forEach(function (t, i) {
    var lab = el("span", "tl-tick" + (i % 2 ? " is-minor" : ""), String(t));
    lab.style.left = pct(t) + "%";
    ticks.appendChild(lab);
  });
  var axisRow = ticks.closest(".tl-axis");
  function thinTicks() {
    var gap = (ticks.getBoundingClientRect().width * 10) / (AX.end - AX.start);
    axisRow.classList.toggle("is-sparse", gap < CFG.minTickGap);
  }

  // ---------------------------------------------------------------- tabs (the list of periods) and cards
  var nav = document.getElementById("tl-nav");
  var cards = document.getElementById("tl-cards");
  nav.setAttribute("aria-label", C.ui.navLabel);

  var tabs = [];
  var panels = [];
  C.events.forEach(function (e, i) {
    var tab = el("button", "tl-tab tl-navgrid");
    tab.type = "button";
    tab.id = "tl-tab-" + i;
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-controls", "tl-card-" + i);
    tab.appendChild(el("span", "tl-date", e.date));
    tab.appendChild(el("span", "tl-name", e.title));
    var track = tab.appendChild(el("span", "tl-track"));
    track.setAttribute("aria-hidden", "true");
    var scale = track.appendChild(el("span", "tl-scale"));
    guides(scale);
    scale.appendChild(mark(e));
    tab.addEventListener("click", function () { select(i); });
    nav.appendChild(tab);
    tabs.push(tab);

    var card = el("article", "tl-card");
    card.id = "tl-card-" + i;
    card.setAttribute("role", "tabpanel");
    card.setAttribute("aria-labelledby", tab.id);
    card.innerHTML =
      '<div class="tl-meta">' + svg(ICONS[e.icon]) + "<span>" + esc(e.date) + "</span></div>" +
      '<h2 class="tl-card-title">' + esc(e.title) + "</h2>" +
      '<p class="tl-card-sub">' + esc(e.subhead) + "</p>" +
      '<p class="tl-card-body">' + rich(e.body) + "</p>";
    cards.appendChild(card);
    panels.push(card);
  });

  var prev = document.getElementById("tl-prev");
  var next = document.getElementById("tl-next");
  var count = document.getElementById("tl-count");
  prev.innerHTML = svg(CARET_L);
  next.innerHTML = svg(CARET_R);
  prev.setAttribute("aria-label", C.ui.prev);
  next.setAttribute("aria-label", C.ui.next);

  var current = -1;
  function select(i, focus) {
    i = Math.max(0, Math.min(C.events.length - 1, i));
    current = i;
    tabs.forEach(function (t, j) {
      t.setAttribute("aria-selected", String(j === i));
      t.tabIndex = j === i ? 0 : -1;
    });
    panels.forEach(function (p, j) { p.classList.toggle("is-active", j === i); });
    count.textContent = i + 1 + " " + C.ui.of + " " + C.events.length;
    prev.disabled = i === 0;
    next.disabled = i === C.events.length - 1;
    if (focus) tabs[i].focus();
  }

  prev.addEventListener("click", function () { select(current - 1); });
  next.addEventListener("click", function () { select(current + 1); });

  // arrow keys, Home and End move between periods, as in any tab list
  nav.addEventListener("keydown", function (ev) {
    var k = ev.key, to = null;
    if (k === "ArrowDown" || k === "ArrowRight") to = current + 1;
    else if (k === "ArrowUp" || k === "ArrowLeft") to = current - 1;
    else if (k === "Home") to = 0;
    else if (k === "End") to = C.events.length - 1;
    if (to === null) return;
    ev.preventDefault();
    select(to, true);
  });

  select(CFG.start);

  // ---------------------------------------------------------------- height for the host page
  // WordPress's own iframe resizer (wp-embed.js) sizes an iframe whose data-secret matches the secret in its
  // messages. The secret comes from the iframe URL (#?secret=…), or from WordPress's "ready" message.
  // The small listener in embed.html reads the same message, for pages where wp-embed.js is not loaded.
  var secret = (location.hash.match(/secret=([A-Za-z0-9]+)/) || [])[1] || null;
  var lastHeight = 0;

  function report(force) {
    var h = Math.ceil(fig.getBoundingClientRect().height);
    if (h > CFG.maxHeight && window.console) {
      console.warn("Timeline is " + h + " px tall; WordPress will cut it at " + CFG.maxHeight + " px.");
    }
    if (!secret || window.parent === window || (!force && h === lastHeight)) return;
    lastHeight = h;
    window.parent.postMessage({ message: "height", value: h, secret: secret }, "*");
  }

  window.addEventListener("message", function (ev) {
    var d = ev.data;
    if (ev.source === window.parent && d && d.message === "ready" && /^[A-Za-z0-9]+$/.test(d.secret || "")) {
      secret = d.secret;
      report(true);
    }
  });

  function relayout() {
    thinTicks();
    report();
  }
  relayout();
  if (window.ResizeObserver) new ResizeObserver(relayout).observe(fig);
  else window.addEventListener("resize", relayout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
  window.addEventListener("load", relayout);
})();
