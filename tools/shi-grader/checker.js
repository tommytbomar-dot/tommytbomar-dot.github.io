/* Static site-health checker (SHI-style). Analyses PASTED HTML in the browser; fetches nothing. MIT. */
(function (root, f) { if (typeof module === 'object' && module.exports) module.exports = f(); else root.ShiChecker = f(); })(typeof self !== 'undefined' ? self : this, function () {
  function has(re, h) { return re.test(h); }
  function check(html) {
    html = String(html || '');
    var items = [], text = html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi, ' ');
    function add(id, label, pass, weight, fix) { items.push({ id: id, label: label, pass: !!pass, weight: weight, fix: fix }); }
    var title = (html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1];
    add('title', 'Has a <title> of 15-65 characters', title && title.trim().length >= 15 && title.trim().length <= 65, 10, 'Write a title with your service + city, about 50-60 characters.');
    var md = html.match(/<meta[^>]+name=["']description["'][^>]*>/i);
    var mdc = md && (md[0].match(/content=["']([^"']*)["']/i) || [])[1];
    add('desc', 'Has a meta description of 70-170 characters', mdc && mdc.length >= 70 && mdc.length <= 170, 8, 'Add a meta description that says what you do, where, and how to reach you.');
    add('viewport', 'Has a mobile viewport meta tag', has(/<meta[^>]+name=["']viewport["']/i, html), 15, 'Add <meta name="viewport" content="width=device-width, initial-scale=1">. Without it phones show a tiny desktop page.');
    var h1s = (html.match(/<h1[\s>]/gi) || []).length;
    add('h1', 'Exactly one <h1>', h1s === 1, 8, h1s === 0 ? 'Add one H1 stating what you do and where.' : 'Use only one H1 per page.');
    add('tel', 'Has a tap-to-call tel: link', has(/href=["']\s*tel:\s*\+?[\d\s().\-]{7,}/i, html), 15, 'Make your phone number a tel: link so mobile visitors can tap to call.');
    add('cta', 'Has a visible call/book/quote action', has(/(call|book|schedule|get (a )?(free )?(quote|estimate)|request|contact)/i, text) && has(/<(a|button)[\s>]/i, html), 8, 'Put one clear call, book, or quote button near the top.');
    add('form', 'Has a contact form or mailto link', has(/<form[\s>]/i, html) || has(/href=["']mailto:/i, html), 6, 'Offer a short form or email link as an alternative to calling.');
    add('schema', 'Has JSON-LD structured data', has(/application\/ld\+json/i, html), 8, 'Add LocalBusiness JSON-LD (see the Local Schema Generator).');
    add('localbiz', 'Structured data mentions a LocalBusiness-type', has(/"@type"\s*:\s*"?\[?\s*"?(LocalBusiness|Plumber|HVACBusiness|Electrician|RoofingContractor|Dentist|Restaurant|ProfessionalService|AutoRepair|HomeAndConstructionBusiness|GeneralContractor|LegalService|Physician|HairSalon|BeautySalon)/i, html), 4, 'Use a specific LocalBusiness type in your JSON-LD.');
    var imgs = html.match(/<img\b[^>]*>/gi) || [], noAlt = imgs.filter(function (i) { return !/\balt=["'][^"']+["']/i.test(i); }).length;
    add('alt', 'Images have alt text' + (imgs.length ? ' (' + noAlt + ' of ' + imgs.length + ' missing)' : ''), noAlt === 0, 5, 'Add short descriptive alt text to every image.');
    add('lang', 'Has <html lang>', has(/<html[^>]+lang=/i, html), 3, 'Add lang="en" to the <html> tag.');
    add('hours', 'Mentions business hours', has(/(hours|open (mon|tue|wed|thu|fri|sat|sun|daily|24)|mon(day)?\s*[-–]\s*fri)/i, text), 4, 'Show your hours on the page and keep them identical to your Google profile.');
    add('addr', 'Shows a street address or service area', has(/\b\d{2,5}\s+[A-Za-z0-9 .]+\b(st|street|ave|avenue|rd|road|blvd|dr|drive|ln|lane|hwy|highway|way|ct|court)\b/i, text) || has(/(serving|service area|areas? served)/i, text), 4, 'List your address or the cities you serve in plain text.');
    add('https', 'Page links do not hardcode http:// resources', !has(/(src|href)=["']http:\/\/(?!localhost)/i, html), 2, 'Switch http:// links and images to https://.');
    var total = 0, got = 0; items.forEach(function (i) { total += i.weight; if (i.pass) got += i.weight; });
    var score = total ? Math.round(100 * got / total) : 0;
    return { score: score, grade: score >= 90 ? 'A' : score >= 75 ? 'B' : score >= 60 ? 'C' : score >= 40 ? 'D' : 'F', items: items };
  }
  return { check: check };
});
