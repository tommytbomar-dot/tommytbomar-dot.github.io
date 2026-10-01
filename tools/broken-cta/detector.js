/* Broken CTA Detector core — MIT. Pure function over a DOM-like document. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(); else root.CtaDetector = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  var CTA_WORDS = /(call|text|book|schedule|get (a )?(free )?(quote|estimate)|request|contact|order|buy|start|sign up|free|appointment|quote|estimate|directions)/i;
  // els: array of {tag, text, href, onclick, disabled, role, visible, top, width, height}
  function analyze(els, ctx) {
    ctx = ctx || {}; var issues = [], ctas = [];
    els.forEach(function (e) {
      var label = (e.text || e.ariaLabel || '').replace(/\s+/g, ' ').trim();
      var href = e.href == null ? null : String(e.href).trim();
      var isCta = CTA_WORDS.test(label) || /^(tel:|sms:|mailto:)/i.test(href || '');
      if (!isCta) return;
      ctas.push(label || href);
      var where = '"' + (label || href || e.tag) + '"';
      if (e.tag === 'a') {
        if (href === null || href === '' || href === '#' || /^javascript:\s*(void\(0\)|;)?$/i.test(href)) { if (!e.onclick) issues.push({ sev: 'high', msg: where + ' is a link with no real destination (href="' + (href || '') + '") and no click handler.' }); }
        if (/^tel:\s*$/i.test(href) || /^mailto:\s*$/i.test(href) || /^sms:\s*$/i.test(href)) issues.push({ sev: 'high', msg: where + ' has an empty ' + href + ' link.' });
        if (/^tel:/i.test(href) && !/^tel:\+?[\d\s().\-]{7,}$/i.test(href)) issues.push({ sev: 'high', msg: where + ' tel: link does not look like a valid phone number (' + href + ').' });
        if (/^mailto:/i.test(href) && !/^mailto:[^@\s?]+@[^@\s?]+\.[^@\s?]+/i.test(href)) issues.push({ sev: 'high', msg: where + ' mailto: link does not contain a valid email (' + href + ').' });
      }
      if (e.disabled) issues.push({ sev: 'high', msg: where + ' is disabled.' });
      if (e.visible === false) issues.push({ sev: 'low', msg: where + ' is hidden (display/visibility); fine if intentional.' });
      if (e.visible !== false && e.width != null && (e.width < 44 || e.height < 32)) issues.push({ sev: 'med', msg: where + ' is small (' + Math.round(e.width) + 'x' + Math.round(e.height) + 'px); tap targets should be about 44px.' });
    });
    var visibleCtas = els.filter(function (e) { return CTA_WORDS.test((e.text || '')) && e.visible !== false; });
    if (!ctas.length) issues.push({ sev: 'high', msg: 'No call-to-action-looking buttons or links found on this page.' });
    var hasTel = els.some(function (e) { return /^tel:/i.test(e.href || ''); });
    if (!hasTel && ctas.length) issues.push({ sev: 'med', msg: 'No tap-to-call (tel:) link found. Mobile visitors to local businesses often want one.' });
    var anyAbove = els.some(function (e) { return e.visible !== false && (CTA_WORDS.test(e.text || '') || /^tel:/i.test(e.href || '')) && e.top != null && e.top < (ctx.viewportHeight || 700); });
    if (ctas.length && els.some(function (e) { return e.top != null; }) && !anyAbove) issues.push({ sev: 'med', msg: 'No CTA is visible without scrolling on the first screen.' });
    if (ctx.formsWithoutAction) issues.push({ sev: 'med', msg: ctx.formsWithoutAction + ' form(s) have no action attribute and may rely on JavaScript; test that they submit.' });
    return { ctaCount: ctas.length, issues: issues, ok: !issues.some(function (i) { return i.sev === 'high'; }) };
  }
  return { analyze: analyze };
});
