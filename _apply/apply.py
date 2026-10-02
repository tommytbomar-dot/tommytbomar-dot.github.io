#!/usr/bin/env python3
"""One-shot, idempotent site-findability edit (Spiel Ventures). Adds /start.html, /links.html, services menu PDF+PNG,
home 'Services & prices' block, richer JSON-LD, 'Hire Tommy' link on every indexable page, sitemap + llms.txt entries.
Never changes price text. Prices below mirror pricing.html (live, 2026-10-01)."""
import os, re, sys, json
BASE = "https://tommytbomar-dot.github.io/"
root = sys.argv[1] if len(sys.argv) > 1 else "."
MARK = "<!--hire-->"
def rd(p): return open(os.path.join(root, p), encoding="utf-8").read()
def wr(p, s):
    full = os.path.join(root, p); os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

# ---- price data (mirrors pricing.html) ----
SERVICES = [
 ("Deep Mobile Audit (PDF of one live URL)", "$147", "audit.html"),
 ("Audit + 10-minute screen-recorded video", "$197", "audit.html"),
 ("One-Day Homepage CTA Rescue", "$297", "svc-cta-rescue.html"),
 ("Map-Pack Rescue (Google Business Profile, 1 location)", "$597", "svc-map-pack-rescue.html"),
 ("Map-Pack + CTA Rescue", "$797", "svc-map-pack-cta-rescue.html"),
 ("Citation Cleanup (research + fix sheet)", "$197", "svc-citation-cleanup-dfy.html"),
 ("Quote page (done for you)", "$497", "svc-booking-page-dfy.html"),
 ("Booking page (done for you)", "$997", "svc-booking-page-dfy.html"),
 ("Review Reply Setup", "$197 + $79/mo", "svc-review-reply-setup.html"),
 ("Site Watch / Site Care (monthly)", "$97 / $179 per mo", "svc-site-health-care.html"),
 ("Office hours, 30 minutes (written recap)", "$125", "office-hours.html"),
 ("Photo restore: light / repair", "$29 / $59", "photo-restore-order.html"),
 ("Photo restore: 3-photo pack / 10-photo album", "$99 / $299", "photo-restore-order.html"),
 ("Mobile Lead Fix Kit (4 checklists, instant Payhip checkout)", "$47", "https://payhip.com/b/ByJMd"),
]
SUBJ = [("Audit","WANT AUDIT"),("Audit + video","WANT AUDIT VIDEO"),("CTA Rescue","WANT CTA RESCUE"),("Map-Pack Rescue","WANT MAP-PACK RESCUE"),
        ("Citation Cleanup","WANT CITATION CLEANUP"),("Quote / Booking page","WANT BOOKING PAGE"),("Photo restore","PHOTO RESTORE"),("Office hours","OFFICE HOURS"),("Kit (or use Payhip)","WANT KIT")]
def href(h): return h if h.startswith("http") else h
def mailto(sub): return "mailto:tommytbomar@gmail.com?subject=" + sub.replace(" ", "%20")

HEAD = lambda title, desc, url, extra="": f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{url}"/>
<link rel="stylesheet" href="/assets/site.css"/>
{extra}<script src="/assets/track.js" defer></script>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Spiel Ventures"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:image" content="{BASE}assets/og-card.png"/>
<meta property="og:image:alt" content="Spiel Ventures - Tommy Bomar, Texas"/>
<meta name="twitter:card" content="summary_large_image"/>
</head>
<body>
<main>
'''
NAV = '<p class="nav"><a href="/index.html">Home</a> · <a href="/pricing.html">Pricing</a> · <a href="/start.html">Hire Tommy</a> · <a href="/links.html">Links</a> · <a href="/faq.html">FAQ</a></p>\n'
FOOT = '''<footer>
<p>Identity: Tommy Bomar / Spiel Ventures · <a href="mailto:tommytbomar@gmail.com">tommytbomar@gmail.com</a> · Texas, USA</p>
<p>No fake reviews. No invented portfolio. No ranking or results guarantees. Prices as of 2026-10-01: <a href="/pricing.html">pricing.html</a> is authoritative.</p>
</footer>
</main>
</body>
</html>
'''
def trows():
    return "\n".join(f'<tr><td><a href="{h}">{n}</a></td><td>{p}</td></tr>' for n, p, h in SERVICES)

# ---- JSON-LD ----
offers = []
for n, p, h in [("Mobile Lead Fix Kit","47",0),("Deep Mobile Audit","147",0),("Audit + 10-minute video","197",0),("One-Day Homepage CTA Rescue","297",0),
                ("Map-Pack Rescue","597",0),("Citation Cleanup","197",0),("Quote page","497",0),("Booking page","997",0),
                ("Photo restore - light (1 photo)","29",0),("Photo restore - repair (1 photo)","59",0),("Photo restore - 3-photo pack","99",0),("Photo restore - 10-photo album","299",0)]:
    offers.append({"@type":"Offer","priceCurrency":"USD","price":p,"itemOffered":{"@type":"Service","name":n}})
LD = {"@context":"https://schema.org","@graph":[
 {"@type":"WebSite","@id":BASE+"#website","url":BASE,"name":"Spiel Ventures","publisher":{"@id":BASE+"#business"}},
 {"@type":["ProfessionalService","Organization"],"@id":BASE+"#business","name":"Spiel Ventures","url":BASE,"email":"tommytbomar@gmail.com",
  "image":BASE+"assets/og-card.png","founder":{"@id":BASE+"#tommy"},
  "description":"Solo Texas developer. Fixed-price mobile website audits, local-lead fixes, quote and booking pages, and digital photo restoration. Prices posted; async by email.",
  "areaServed":["Tyler TX","Longview TX","Kilgore TX","Marshall TX","Galveston TX","East Texas","Gulf Coast","Remote (United States)"],
  "knowsAbout":["JavaScript","Kotlin","Mobile website audits","Google Business Profile","Local business websites","Photo restoration"],
  "priceRange":"$29-$997","sameAs":["https://github.com/tommytbomar-dot"],
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services and prices (USD)","itemListElement":offers}},
 {"@type":"Person","@id":BASE+"#tommy","name":"Tommy Bomar","email":"tommytbomar@gmail.com","url":BASE+"start.html","sameAs":["https://github.com/tommytbomar-dot"],"worksFor":{"@id":BASE+"#business"}}]}
LDTAG = '<script type="application/ld+json">\n' + json.dumps(LD, ensure_ascii=False, separators=(",", ":")) + '\n</script>\n'

# ---- start.html ----
subj = " · ".join(f'<a href="{mailto(s)}">{s}</a>' for _, s in SUBJ[:0]) or ""
order_rows = "\n".join(f'<tr><td>{n}</td><td><a href="{mailto(s)}">{s}</a></td></tr>' for n, s in SUBJ)
start = HEAD("Hire Tommy - services, prices and how to order | Spiel Ventures",
  "Hire Tommy Bomar (Spiel Ventures), a solo JavaScript and Kotlin developer in Texas: mobile website audit $147, CTA rescue $297, photo restore from $29. Prices posted, order by email.",
  BASE+"start.html", LDTAG) + NAV + f'''<h1>Hire Tommy</h1>
<p class="lead">Solo JavaScript &amp; Kotlin developer in Texas · fixed prices · written scope before you pay · async by email, no calls needed</p>
<div class="card">
<h2>What I do</h2>
<ul>
<li><strong>Local business websites:</strong> a plain-English mobile audit of your live site, fixes to the call/quote button path, quote and booking pages, Google Business Profile and citation cleanup.</li>
<li><strong>Family photos:</strong> digital restoration with natural-looking faces, printable ~4K, from $29.</li>
<li><strong>Developer work (JavaScript, Node, Chrome extensions, Kotlin/Android):</strong> email what you need and I'll quote it in writing. No published rates yet.</li>
</ul>
<div class="btn-row"><a class="btn-buy" href="{mailto("WANT AUDIT")}">Email · WANT AUDIT + your URL</a><a class="btn-secondary" href="mailto:tommytbomar@gmail.com">tommytbomar@gmail.com</a></div>
</div>
<div class="card" id="prices">
<h2>Services &amp; prices (USD, one price per item)</h2>
<table class="pt">
{trows()}
</table>
<p class="buy-note">Full list incl. vertical packs and wholesale: <a href="/pricing.html">pricing.html</a> (authoritative). No ranking or results guarantees on anything.</p>
</div>
<div class="card">
<h2>How to order</h2>
<ol>
<li>Email <a href="mailto:tommytbomar@gmail.com">tommytbomar@gmail.com</a> with the subject for the item (below) and, for an audit, your website URL; for photos, attach the scans.</li>
<li>I reply with the scope in writing. You approve it.</li>
<li>You pay by Venmo, PayPal or Zelle, then work starts. (The $47 kit also has instant checkout on <a href="https://payhip.com/b/ByJMd">Payhip</a>.)</li>
<li>I send the finished deliverable by email.</li>
</ol>
<table class="pt">
{order_rows}
</table>
</div>
<div class="card">
<h2>What you can check before you pay</h2>
<ul>
<li>Free tools I wrote: <a href="https://github.com/tommytbomar-dot/broken-cta-detector">Broken CTA Detector</a>, <a href="https://github.com/tommytbomar-dot/gbp-hours-validator">GBP Hours Validator</a>, <a href="https://github.com/tommytbomar-dot/local-schema-generator">Local Schema Generator</a>, <a href="https://github.com/tommytbomar-dot/form-field-counter">Form Field Counter</a> (all open source on <a href="https://github.com/tommytbomar-dot">GitHub</a>).</li>
<li>A <a href="/sample-audit.html">sample audit</a> (labeled SAMPLE) so you can see the format.</li>
<li><strong>Honest status:</strong> I'm new to selling this. There are no customer reviews or client logos yet, and I won't invent any.</li>
</ul>
</div>
<div class="card">
<h2>Share or print</h2>
<p><a href="/assets/services-menu.pdf">One-page services menu (PDF)</a> · <a href="/assets/services-menu.png">PNG for sharing</a> · <a href="/links.html">All links</a></p>
</div>
''' + FOOT
wr("start.html", start)

# ---- links.html ----
def L(h, t, d=""): return f'<li><a href="{h}"><strong>{t}</strong></a>' + (f' <span class="muted">- {d}</span>' if d else "") + "</li>"
links = HEAD("Links - Tommy Bomar / Spiel Ventures", "Every real link for Tommy Bomar (Spiel Ventures): services and prices, order by email, free tools, GitHub, photo restore.",
  BASE+"links.html") + NAV + '''<h1>Tommy Bomar · Spiel Ventures</h1>
<p class="lead">Solo JavaScript &amp; Kotlin developer in Texas. Prices posted. Order by email.</p>
<div class="card"><h2>Hire / order</h2><ul>
''' + "\n".join([
 L("/start.html","Hire Tommy: services &amp; prices","what I do, how to order"),
 L("/pricing.html","Full price sheet","every price in one place"),
 L("/audit.html","Deep Mobile Audit - $147","PDF of your live site on phones"),
 L("/photo-restore-order.html","Photo restoration - from $29","how to order"),
 L("https://payhip.com/b/ByJMd","Mobile Lead Fix Kit - $47","instant Payhip checkout"),
 L("mailto:tommytbomar@gmail.com","Email: tommytbomar@gmail.com")]) + '''
</ul></div>
<div class="card"><h2>Free tools and guides</h2><ul>
''' + "\n".join([
 L("/tools/","Free local-business tools","site checker, schema, hours widget and more"),
 L("/tools/broken-cta/","Broken CTA Detector","bookmarklet"),
 L("/lead-magnet-7-day.html","Free 7-day lead checklist"),
 L("/photo-scanner-guide.html","Photo scanner guide","for restoring family photos"),
 L("/blog/index.html","Tips blog")]) + '''
</ul></div>
<div class="card"><h2>Open source (GitHub)</h2><ul>
''' + "\n".join([
 L("https://github.com/tommytbomar-dot","GitHub profile"),
 L("https://github.com/tommytbomar-dot/broken-cta-detector","broken-cta-detector"),
 L("https://github.com/tommytbomar-dot/gbp-hours-validator","gbp-hours-validator"),
 L("https://github.com/tommytbomar-dot/local-schema-generator","local-schema-generator"),
 L("https://github.com/tommytbomar-dot/form-field-counter","form-field-counter"),
 L("https://github.com/tommytbomar-dot/review-sentiment-phrase-bank","review-sentiment-phrase-bank"),
 L("https://github.com/tommytbomar-dot/n8n-lead-workflow-templates","n8n-lead-workflow-templates"),
 L("https://github.com/tommytbomar-dot/mobile-lead-fix-kit","mobile-lead-fix-kit")]) + '''
</ul></div>
<div class="card"><h2>Print / share</h2><ul>
''' + L("/assets/services-menu.pdf","Services menu (PDF, 1 page)") + L("/assets/services-menu.png","Services menu (PNG)") + '''
</ul></div>
''' + FOOT
wr("links.html", links)

# ---- site.css: table style (append once) ----
css = rd("assets/site.css")
if ".pt{" not in css:
    css += "\n.pt{width:100%;border-collapse:collapse;font-size:.95rem;margin:.4rem 0}.pt td{padding:.4rem .25rem;border-bottom:1px solid var(--line);vertical-align:top}.pt td:last-child{text-align:right;color:var(--ok);font-weight:700;white-space:nowrap}\n.hire-cta{font-size:.9rem}\n"
    wr("assets/site.css", css)

# ---- index.html: services block + JSON-LD ----
ix = rd("index.html")
if 'id="services-prices"' not in ix:
    block = f'''<div class="card" id="services-prices">
<h2>Services &amp; prices</h2>
<table class="pt">
{trows()}
</table>
<div class="btn-row"><a class="btn-buy" href="/start.html">Hire Tommy · how to order</a><a class="btn-secondary" href="/pricing.html">Full price sheet</a></div>
</div>
'''
    ix2 = re.sub(r'(<p class="lead">.*?</p>\n)', lambda m: m.group(1) + block, ix, count=1, flags=re.S)
    assert ix2 != ix, "index lead not found"
    ix = ix2
ix = re.sub(r'<script type="application/ld\+json">.*?</script>\n', lambda m: LDTAG, ix, count=1, flags=re.S) if '"@graph"' not in ix else ix
wr("index.html", ix)

# ---- 'Hire Tommy' link on every indexable page ----
LINE = f'<p class="hire-cta">{MARK}<a href="/start.html">Hire Tommy: services &amp; prices</a> · <a href="/links.html">All links</a></p>\n'
changed = 0
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in (".git", ".github", "_apply", "node_modules")]
    for f in fn:
        if not f.endswith(".html"): continue
        rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
        if rel in ("start.html", "links.html"): continue
        s = rd(rel)
        if MARK in s: continue
        if re.search(r'name=["\']robots["\'][^>]*noindex', s, re.I) and rel != "404.html": continue
        if "</body>" not in s: continue
        t = s
        if '<p class="nav">' in t and "/start.html" not in t.split("</p>", 1)[0] :
            t = re.sub(r'(<p class="nav">.*?)(</p>)', lambda m: m.group(1) + ' · <a href="/start.html">Hire Tommy</a>' + m.group(2), t, count=1, flags=re.S)
        if "</footer>" in t:
            i = t.rindex("</footer>"); t = t[:i] + LINE + t[i:]
        elif "</main>" in t:
            i = t.rindex("</main>"); t = t[:i] + LINE + t[i:]
        else:
            i = t.rindex("</body>"); t = t[:i] + LINE + t[i:]
        wr(rel, t); changed += 1
print("hire-link added to", changed, "pages")

# ---- sitemap + llms.txt ----
sm = rd("sitemap.xml")
for u in ("start.html", "links.html"):
    if BASE + u not in sm:
        sm = sm.replace("</urlset>", f"<url><loc>{BASE}{u}</loc><changefreq>weekly</changefreq></url>\n</urlset>")
wr("sitemap.xml", sm)
ll = rd("llms.txt")
if "start.html" not in ll:
    ll = ll.replace("## Key pages\n", "## Key pages\n- [Hire Tommy](" + BASE + "start.html): what he does, every price, how to order\n- [Links](" + BASE + "links.html): all real links\n- [Services menu PDF](" + BASE + "assets/services-menu.pdf): one-page printable menu\n", 1)
    wr("llms.txt", ll)

# ---- services menu PDF + PNG ----
try:
    from PIL import Image, ImageDraw, ImageFont
    import qrcode
    def F(sz, bold=False):
        for fp in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""), "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular")):
            if os.path.exists(fp): return ImageFont.truetype(fp, sz)
        return ImageFont.load_default()
    def menu(W, H, s):
        im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
        INK, MUT, ACC = (17, 24, 39), (90, 100, 115), (14, 116, 144)
        d.rectangle([0, 0, W, int(170*s)], fill=INK)
        d.text((int(60*s), int(28*s)), "Spiel Ventures", font=F(int(70*s), True), fill=(255, 255, 255))
        d.text((int(60*s), int(112*s)), "Tommy Bomar  |  solo JavaScript & Kotlin developer  |  Texas", font=F(int(30*s)), fill=(203, 213, 225))
        y = int(220*s)
        groups = [("Websites for local businesses", [("Deep Mobile Audit (PDF, one live URL)", "$147"), ("Audit + 10-minute video", "$197"), ("One-Day Homepage CTA Rescue", "$297"), ("Map-Pack Rescue (Google Business Profile)", "$597"), ("Citation Cleanup (research + fix sheet)", "$197"), ("Quote page / Booking page", "$497 / $997")]),
                  ("Family photo restoration", [("Light restore / Repair (per photo)", "$29 / $59"), ("3-photo pack / 10-photo album", "$99 / $299")]),
                  ("Ongoing and extras", [("Site Watch / Site Care (monthly)", "$97 / $179"), ("Office hours, 30 min + written recap", "$125"), ("Mobile Lead Fix Kit (4 checklists)", "$47")])]
        for title, rows in groups:
            d.text((int(60*s), y), title, font=F(int(42*s), True), fill=ACC); y += int(68*s)
            for n, p in rows:
                d.text((int(60*s), y), n, font=F(int(34*s)), fill=INK)
                pw = d.textlength(p, font=F(int(34*s), True)); d.text((W-int(60*s)-pw, y), p, font=F(int(34*s), True), fill=INK)
                d.line([int(60*s), y+int(50*s), W-int(60*s), y+int(50*s)], fill=(226, 232, 240), width=max(1, int(s)))
                y += int(66*s)
            y += int(44*s)
        d.text((int(60*s), y), "How to order", font=F(int(42*s), True), fill=ACC); y += int(68*s)
        for line in ("1. Email the item name (and your website URL or photo scans).", "2. I reply with the scope in writing. You approve it.", "3. Pay by Venmo, PayPal or Zelle. Then work starts.", "4. Finished work arrives by email. No calls needed."):
            d.text((int(60*s), y), line, font=F(int(32*s)), fill=INK); y += int(54*s)
        y += int(14*s)
        d.text((int(60*s), y), "tommytbomar@gmail.com", font=F(int(44*s), True), fill=INK); y += int(66*s)
        d.text((int(60*s), y), "tommytbomar-dot.github.io/start.html", font=F(int(36*s), True), fill=ACC)
        q = qrcode.make(BASE + "start.html").convert("RGB").resize((int(260*s), int(260*s)))
        im.paste(q, (W-int(60*s)-int(260*s), y-int(190*s)))
        d.text((int(60*s), H-int(130*s)), "Prices as of 2026-10-01, USD. Full list: tommytbomar-dot.github.io/pricing.html", font=F(int(26*s)), fill=MUT)
        d.text((int(60*s), H-int(88*s)), "New to selling this: no customer reviews or client logos yet, and none are claimed.", font=F(int(26*s)), fill=MUT)
        d.text((int(60*s), H-int(46*s)), "No ranking or results guarantees.", font=F(int(26*s)), fill=MUT)
        return im
    os.makedirs(os.path.join(root, "assets"), exist_ok=True)
    pdfim = menu(1700, 2200, 1.0)  # letter @ 200 dpi
    pdfim.save(os.path.join(root, "assets", "services-menu.pdf"), "PDF", resolution=200.0)
    menu(1080, 1400, 0.64).save(os.path.join(root, "assets", "services-menu.png"), optimize=True)
    print("menu written")
except Exception as e:
    print("MENU FAILED:", e); sys.exit(1)
