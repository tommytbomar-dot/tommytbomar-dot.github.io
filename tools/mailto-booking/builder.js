/* Mailto booking link builder core. MIT. */
(function (root, f) { if (typeof module === 'object' && module.exports) module.exports = f(); else root.MailtoBuilder = f(); })(typeof self !== 'undefined' ? self : this, function () {
  var EMAIL = /^[^@\s,;?&]+@[^@\s,;?&]+\.[^@\s,;?&]+$/;
  function enc(s) { return encodeURIComponent(String(s)).replace(/%20/g, '%20'); }
  function build(o) {
    var errors = [];
    if (!EMAIL.test((o.to || '').trim())) errors.push('Enter one valid email address.');
    var fields = (o.fields || []).map(function (s) { return String(s).trim(); }).filter(Boolean);
    var body = '';
    if (o.intro) body += o.intro.trim() + '\n\n';
    fields.forEach(function (f) { body += f + ': \n'; });
    var q = [];
    if (o.subject) q.push('subject=' + enc(o.subject.trim()));
    if (body) q.push('body=' + enc(body.replace(/\n/g, '\r\n')));
    var href = 'mailto:' + (o.to || '').trim() + (q.length ? '?' + q.join('&') : '');
    var label = (o.label || 'Book by email').replace(/</g, '&lt;');
    var html = '<a href="' + href.replace(/&/g, '&amp;') + '" style="display:inline-block;padding:.75em 1.25em;background:' + (o.color || '#1a73e8') + ';color:#fff;border-radius:8px;text-decoration:none;font:600 16px system-ui,sans-serif">' + label + '</a>';
    if (href.length > 1800) errors.push('Link is ' + href.length + ' characters; some mail apps cut off long links. Shorten the intro or fields.');
    return { href: href, html: html, errors: errors, length: href.length };
  }
  return { build: build };
});
