/* Spiel Ventures — privacy-friendly CTA attribution. No cookies, no third-party requests, no data leaves your browser.
   When someone clicks an email (mailto:) button, the page name is added to the draft email body so Tommy can see which page it came from.
   Payhip links get utm_source/utm_medium/utm_campaign. Optional: set GOATCOUNTER_CODE after a free signup at goatcounter.com (cookie-free). */
(function () {
  var GOATCOUNTER_CODE = ""; // e.g. "spielventures" -> loads https://spielventures.goatcounter.com/count
  var page = (location.pathname.replace(/^\/+/, "").replace(/\.html$/, "").replace(/\/index$/, "").replace(/\/$/, "")) || "home";
  var utm = "utm_source=site&utm_medium=cta&utm_campaign=" + encodeURIComponent(page);
  function decorate() {
    var links = document.querySelectorAll('a[href*="payhip.com"]');
    for (var i = 0; i < links.length; i++) {
      var h = links[i].getAttribute("href");
      if (h.indexOf("utm_source=") === -1) links[i].setAttribute("href", h + (h.indexOf("?") === -1 ? "?" : "&") + utm);
    }
  }
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href^="mailto:"]') : null;
    if (!a || a.getAttribute("data-trk")) return;
    var h = a.getAttribute("href"), q = h.indexOf("?");
    var base = q < 0 ? h : h.slice(0, q), parts = q < 0 ? [] : h.slice(q + 1).split("&"), tag = encodeURIComponent("\n\n---\nsource: " + page + " (" + utm + ")");
    var found = false;
    for (var i = 0; i < parts.length; i++) if (parts[i].indexOf("body=") === 0) { parts[i] += tag; found = true; }
    if (!found) parts.push("body=" + encodeURIComponent("Hi Tommy,\n") + tag);
    a.setAttribute("href", base + "?" + parts.join("&")); a.setAttribute("data-trk", "1");
  }, true);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", decorate); else decorate();
  if (GOATCOUNTER_CODE) { var s = document.createElement("script"); s.async = true; s.src = "//gc.zgo.at/count.js"; s.setAttribute("data-goatcounter", "https://" + GOATCOUNTER_CODE + ".goatcounter.com/count"); document.head.appendChild(s); }
})();
