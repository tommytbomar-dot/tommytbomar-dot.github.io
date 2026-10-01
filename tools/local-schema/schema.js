/* Local Schema Generator core — MIT. UMD: works in browser and node. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(); else root.LocalSchema = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  var DAY = { mon: 'Monday', tue: 'Tuesday', wed: 'Wednesday', thu: 'Thursday', fri: 'Friday', sat: 'Saturday', sun: 'Sunday' };
  function t24(s) { // "09:00" -> "09:00"; accepts "9:00", "9am"
    s = String(s || '').trim().toLowerCase();
    var m = s.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$/); if (!m) return null;
    var h = +m[1], mi = m[2] ? +m[2] : 0;
    if (m[3]) { if (h < 1 || h > 12) return null; h = h % 12 + (m[3] === 'pm' ? 12 : 0); }
    if (h > 24 || mi > 59) return null;
    return (h < 10 ? '0' : '') + h + ':' + (mi < 10 ? '0' : '') + mi;
  }
  function build(f) {
    var errors = [];
    if (!f.name || !f.name.trim()) errors.push('Business name is required.');
    var o = { '@context': 'https://schema.org', '@type': f.type || 'LocalBusiness' };
    if (f.name) o.name = f.name.trim();
    if (f.url) { if (!/^https?:\/\//i.test(f.url)) errors.push('URL must start with http:// or https://'); o.url = f.url.trim(); }
    if (f.image) o.image = f.image.trim();
    if (f.phone) o.telephone = f.phone.trim();
    if (f.email) o.email = f.email.trim();
    if (f.priceRange) o.priceRange = f.priceRange.trim();
    if (f.description) o.description = f.description.trim();
    var a = {};
    if (f.street) a.streetAddress = f.street.trim();
    if (f.city) a.addressLocality = f.city.trim();
    if (f.state) a.addressRegion = f.state.trim();
    if (f.zip) a.postalCode = f.zip.trim();
    if (Object.keys(a).length) { a['@type'] = 'PostalAddress'; a.addressCountry = (f.country || 'US').trim(); o.address = a; }
    else errors.push('Address is strongly recommended for local business schema.');
    if (f.lat !== undefined && f.lat !== '' && f.lng !== undefined && f.lng !== '') {
      var la = parseFloat(f.lat), ln = parseFloat(f.lng);
      if (isNaN(la) || isNaN(ln) || Math.abs(la) > 90 || Math.abs(ln) > 180) errors.push('Latitude/longitude out of range.');
      else o.geo = { '@type': 'GeoCoordinates', latitude: la, longitude: ln };
    }
    if (f.areaServed) { var as = f.areaServed.split(/\s*,\s*/).filter(Boolean); if (as.length) o.areaServed = as.length === 1 ? as[0] : as; }
    if (f.sameAs) { var s = f.sameAs.split(/\s*[\n,]\s*/).filter(Boolean); if (s.length) o.sameAs = s; }
    // hours: array of {days:[mon..], opens, closes}
    if (f.hours && f.hours.length) {
      var specs = [];
      f.hours.forEach(function (h, i) {
        if (!h.days || !h.days.length) return;
        var op = t24(h.opens), cl = t24(h.closes);
        if (!op || !cl) { errors.push('Hours row ' + (i + 1) + ': could not read times.'); return; }
        if (op === cl) { errors.push('Hours row ' + (i + 1) + ': opens and closes at the same time.'); return; }
        specs.push({ '@type': 'OpeningHoursSpecification', dayOfWeek: h.days.map(function (d) { return DAY[d]; }), opens: op, closes: cl });
      });
      if (specs.length) o.openingHoursSpecification = specs;
    }
    return { object: o, json: JSON.stringify(o, null, 2), errors: errors };
  }
  function toScriptTag(json) { return '<script type="application/ld+json">\n' + json + '\n</script>'; }
  return { build: build, toScriptTag: toScriptTag, t24: t24 };
});
