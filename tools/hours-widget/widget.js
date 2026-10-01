/* Hours widget: <div data-hours-widget data-tz="America/Chicago" data-hours='{"mon":["09:00-17:00"],"sat":[],"sun":[]}'></div>. MIT. */
(function (root, f) { var api = f(); if (typeof module === 'object' && module.exports) module.exports = api; else { root.HoursWidget = api; if (typeof document !== 'undefined') api.autoInit(document); } })(typeof self !== 'undefined' ? self : this, function () {
  var D = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
  function toMin(s) { var m = /^(\d{1,2}):(\d{2})$/.exec(s); return m ? +m[1] * 60 + +m[2] : NaN; }
  function fmt(min) { min = min % 1440; var h = Math.floor(min / 60), m = min % 60; return (h % 12 || 12) + (m ? ':' + (m < 10 ? '0' : '') + m : '') + (h < 12 ? ' AM' : ' PM'); }
  function nowIn(tz, date) {
    var p = new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(date || new Date()), o = {};
    p.forEach(function (x) { o[x.type] = x.value; });
    return { day: o.weekday.toLowerCase().slice(0, 3), min: (+o.hour % 24) * 60 + +o.minute };
  }
  function status(hours, now) { // now: {day, min}
    var i = D.indexOf(now.day), prev = D[(i + 6) % 7], r, k;
    // overnight spill from previous day
    var pr = hours[prev] || []; for (k = 0; k < pr.length; k++) { r = pr[k].split('-'); var a = toMin(r[0]), b = toMin(r[1]); if (b <= a && now.min < b) return { open: true, until: b }; }
    var td = hours[now.day] || [];
    for (k = 0; k < td.length; k++) { r = td[k].split('-'); a = toMin(r[0]); b = toMin(r[1]); if (isNaN(a) || isNaN(b)) continue; if (b <= a) b += 1440; if (now.min >= a && now.min < b) return { open: true, until: b }; }
    var best = null;
    for (var d = 0; d < 7; d++) { var day = D[(i + d) % 7], rs = hours[day] || [];
      for (k = 0; k < rs.length; k++) { a = toMin(rs[k].split('-')[0]); if (isNaN(a)) continue; if (d === 0 && a <= now.min) continue; best = { day: day, d: d, at: a }; break; }
      if (best) break; }
    return { open: false, next: best };
  }
  function label(st) { if (st.open) return 'Open now · until ' + fmt(st.until); if (!st.next) return 'Closed'; return 'Closed · opens ' + (st.next.d === 0 ? 'today' : st.next.d === 1 ? 'tomorrow' : st.next.day.charAt(0).toUpperCase() + st.next.day.slice(1)) + ' at ' + fmt(st.next.at); }
  function render(el) {
    var hours; try { hours = JSON.parse(el.getAttribute('data-hours')); } catch (e) { el.textContent = 'Hours widget: invalid data-hours JSON'; return; }
    var tz = el.getAttribute('data-tz') || 'America/Chicago', st;
    try { st = status(hours, nowIn(tz)); } catch (e) { el.textContent = 'Hours widget: invalid data-tz'; return; }
    el.textContent = label(st); el.setAttribute('data-open', st.open ? 'true' : 'false'); el.setAttribute('role', 'status');
    if (!el.getAttribute('data-unstyled')) { el.style.cssText = 'display:inline-block;padding:.35em .8em;border-radius:999px;font:600 14px system-ui,sans-serif;color:#fff;background:' + (st.open ? '#1a7f37' : '#8a8f98'); }
  }
  function autoInit(doc) { [].forEach.call(doc.querySelectorAll('[data-hours-widget]'), render); }
  return { status: status, label: label, nowIn: nowIn, render: render, autoInit: autoInit };
});
