/* Browser-side collector: reads the live page, calls CtaDetector.analyze, shows a panel. */
(function () {
  var els = [].slice.call(document.querySelectorAll('a,button,input[type=submit],input[type=button],[role=button]')).map(function (n) {
    var r = n.getBoundingClientRect(), cs = getComputedStyle(n);
    return { tag: n.tagName.toLowerCase(), text: (n.innerText || n.value || '').slice(0, 80), ariaLabel: n.getAttribute('aria-label'),
      href: n.tagName === 'A' ? n.getAttribute('href') : null, onclick: !!(n.onclick || n.getAttribute('onclick')), disabled: n.disabled === true || n.getAttribute('aria-disabled') === 'true',
      visible: cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0, top: r.top + window.scrollY, width: r.width, height: r.height };
  });
  var forms = [].filter.call(document.forms, function (f) { return !f.getAttribute('action'); }).length;
  var res = CtaDetector.analyze(els, { viewportHeight: window.innerHeight, formsWithoutAction: forms });
  var p = document.getElementById('__cta_panel') || document.createElement('div'); p.id = '__cta_panel';
  p.style.cssText = 'position:fixed;z-index:2147483647;top:10px;right:10px;max-width:380px;max-height:80vh;overflow:auto;background:#111;color:#eee;font:13px/1.4 system-ui;padding:12px;border-radius:8px;box-shadow:0 4px 20px #0008';
  var h = '<b>Broken CTA check</b> <a href="#" id="__cta_x" style="float:right;color:#9cf">close</a><br>' + res.ctaCount + ' CTA(s) found, ' + res.issues.length + ' issue(s)<ul style="padding-left:18px">';
  res.issues.forEach(function (i) { h += '<li style="color:' + (i.sev === 'high' ? '#f88' : i.sev === 'med' ? '#fc6' : '#aaa') + '">[' + i.sev + '] ' + i.msg.replace(/</g, '&lt;') + '</li>'; });
  if (!res.issues.length) h += '<li style="color:#8f8">No issues detected by these basic checks.</li>';
  h += '</ul><a style="color:#9cf" href="mailto:tommytbomar@gmail.com?subject=WANT%20AUDIT&body=URL%3A%20' + encodeURIComponent(location.href) + '">Want a human audit? Email WANT AUDIT ($147)</a>';
  p.innerHTML = h; document.body.appendChild(p); document.getElementById('__cta_x').onclick = function (e) { e.preventDefault(); p.remove(); };
})();
