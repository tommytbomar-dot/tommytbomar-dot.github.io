/* NAP (Name, Address, Phone) formatter. US-focused. MIT. */
(function (root, f) { if (typeof module === 'object' && module.exports) module.exports = f(); else root.Nap = f(); })(typeof self !== 'undefined' ? self : this, function () {
  var ABBR = { street: 'St', avenue: 'Ave', road: 'Rd', boulevard: 'Blvd', drive: 'Dr', lane: 'Ln', highway: 'Hwy', court: 'Ct', suite: 'Ste', north: 'N', south: 'S', east: 'E', west: 'W', parkway: 'Pkwy' };
  function cap(w) { return /^(PO|NE|NW|SE|SW|N|S|E|W|LLC|LP|II|III)$/i.test(w) ? w.toUpperCase() : w.charAt(0).toUpperCase() + w.slice(1).toLowerCase(); }
  function phone(raw) {
    var d = String(raw || '').replace(/\D/g, '');
    if (d.length === 11 && d[0] === '1') d = d.slice(1);
    if (d.length !== 10) return { ok: false, error: 'Expected 10 US digits, found ' + d.length + '.' };
    return { ok: true, display: '(' + d.slice(0, 3) + ') ' + d.slice(3, 6) + '-' + d.slice(6), tel: '+1' + d, dashed: d.slice(0, 3) + '-' + d.slice(3, 6) + '-' + d.slice(6) };
  }
  function street(raw, abbreviate) {
    var s = String(raw || '').replace(/\s+/g, ' ').replace(/\./g, '').trim();
    return s.split(' ').map(function (w) { var l = w.toLowerCase().replace(/,$/, ''); if (abbreviate && ABBR[l]) return ABBR[l]; if (/^\d/.test(w)) return w.toUpperCase(); return cap(w); }).join(' ');
  }
  function format(o) {
    var errors = [], name = String(o.name || '').replace(/\s+/g, ' ').trim();
    if (!name) errors.push('Business name is required.');
    var p = phone(o.phone); if (!p.ok) errors.push('Phone: ' + p.error);
    var st = street(o.street, o.abbreviate !== false), city = cap0(o.city), state = String(o.state || '').trim().toUpperCase(), zip = String(o.zip || '').trim();
    if (!st) errors.push('Street is required.');
    if (!/^[A-Z]{2}$/.test(state)) errors.push('State must be a 2-letter code.');
    if (!/^\d{5}(-\d{4})?$/.test(zip)) errors.push('ZIP must be 5 digits (or ZIP+4).');
    var oneLine = name + ' · ' + st + ', ' + city + ', ' + state + ' ' + zip + ' · ' + (p.display || '');
    var html = '<div itemscope itemtype="https://schema.org/LocalBusiness">\n  <strong itemprop="name">' + esc(name) + '</strong><br>\n  <span itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">\n    <span itemprop="streetAddress">' + esc(st) + '</span>,\n    <span itemprop="addressLocality">' + esc(city) + '</span>,\n    <span itemprop="addressRegion">' + esc(state) + '</span>\n    <span itemprop="postalCode">' + esc(zip) + '</span>\n  </span><br>\n  <a href="tel:' + (p.tel || '') + '" itemprop="telephone">' + esc(p.display || '') + '</a>\n</div>';
    return { errors: errors, name: name, street: st, city: city, state: state, zip: zip, phone: p, oneLine: oneLine, html: html, citationBlock: [name, st, city + ', ' + state + ' ' + zip, p.display || ''].join('\n') };
  }
  function cap0(c) { return String(c || '').replace(/\s+/g, ' ').trim().split(' ').map(cap).join(' '); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  // Try to split "123 main street, tyler tx 75701, 903.555.0100" style paste
  function parseLoose(text) {
    var t = String(text || '').trim(), out = {};
    var ph = t.match(/(\+?1?[\s.\-]?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})/); if (ph) { out.phone = ph[1]; t = t.replace(ph[1], ' '); }
    var z = t.match(/\b([A-Za-z]{2})\.?[ ,]+(\d{5}(?:-\d{4})?)\b/); if (z) { out.state = z[1]; out.zip = z[2]; t = t.replace(z[0], ' '); }
    var parts = t.split(/[\n,|;·]+/).map(function (x) { return x.trim(); }).filter(Boolean);
    if (parts.length >= 3) { out.name = parts[0]; out.street = parts[1]; out.city = parts[2]; }
    else if (parts.length === 2) { out.street = parts[0]; out.city = parts[1]; }
    return out;
  }
  return { format: format, phone: phone, parseLoose: parseLoose, street: street };
});
