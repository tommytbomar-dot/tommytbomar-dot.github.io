#!/usr/bin/env python3
"""Apply the approved 2026-10-01 price sheet to the Spiel Ventures static site (run from repo root)."""
import re, os, glob

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8', newline='').write(s)

def sub(p, old, new, count=1, regex=False, flags=0):
    s = rd(p)
    n = len(re.findall(old, s, flags)) if regex else s.count(old)
    if n < 1 or (count and n != count):
        raise AssertionError('%s: %r matched %d (want %s)' % (p, old[:70], n, count))
    s = re.sub(old, new, s, flags=flags) if regex else s.replace(old, new)
    wr(p, s)

M = 'mailto:tommytbomar@gmail.com?subject='
BASE = 'https://tommytbomar-dot.github.io/'
KITREPO = 'https://github.com/tommytbomar-dot/mobile-lead-fix-kit'
FOOT = '<footer><p>© Spiel Ventures · Tommy Bomar · <a href="mailto:tommytbomar@gmail.com">tommytbomar@gmail.com</a></p><p>No fake reviews. No invented portfolio. Inbound only. $0 ads.</p></footer>'
NAV = '<p class="nav"><a href="index.html">Home</a> · <a href="offers.html">Offers</a> · <a href="pricing.html">Pricing</a> · <a href="order.html">Order</a> · <a href="services.html">Services</a> · <a href="products.html">Products</a> · <a href="book.html">Book</a> · <a href="faq.html">FAQ</a></p>'

def stub(path, title, target, msg, prefix=''):
    t = prefix + target
    wr(path, ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
      '<title>%s | Spiel Ventures</title><meta name="robots" content="noindex,follow"/>'
      '<link rel="canonical" href="%s%s"/><meta http-equiv="refresh" content="3;url=%s"/>'
      '<link rel="stylesheet" href="%sassets/site.css"/></head><body><main>'
      '<p class="nav"><a href="%sindex.html">Home</a> · <a href="%sproducts.html">Products</a> · <a href="%spricing.html">Pricing</a></p>'
      '<h1>%s</h1><div class="card"><p>%s</p><p>Taking you to <a href="%s">%s</a> in a few seconds.</p></div>'
      '<footer><p>© Spiel Ventures · Tommy Bomar · <a href="mailto:tommytbomar@gmail.com">tommytbomar@gmail.com</a></p></footer></main></body></html>\n')
      % (title, BASE, target, t, prefix, prefix, prefix, prefix, title, msg, t, target))

# ---------------------------------------------------------------- 1. global $97 audit -> $147 (files where $97 is the audit price)
EXCL_97 = {'order.html','pricing.html','services.html','white-label.html','white-label-onepager.html','office-hours.html','community.html',
           'svc-site-health-care.html','svc-agency-audit-wholesale.html'}
allhtml = sorted(glob.glob('**/*.html', recursive=True))
for p in allhtml + ['README.md','tools/broken-cta/scan.js']:
    if p in EXCL_97 or p.startswith('products/') or p.startswith('svc-'): continue
    s = rd(p)
    s2 = s.replace('$97', '$147').replace('"price":"97"', '"price":"147"')
    if s2 != s: wr(p, s2)

# ---------------------------------------------------------------- 2. voicemail etc: product pages
VERT = {'01':39,'05':39,'07':39,'09':29,'11':39,'12':29,'13':49,'14':29,'15':49,'16':39,'17':29,'18':49,'19':39,'20':29,'21':39,'22':29,'23':29,'99':97,'100':97}
INBUNDLE = ['02','03','04','06','08','10','24','25']
for p in sorted(glob.glob('products/*.html')):
    n = os.path.basename(p)[:2] if not os.path.basename(p).startswith('100') else '100'
    if n in ('38','86','87'): continue
    s = rd(p)
    s = s.replace('Local Lead OS bundle $197', 'Local Lead OS bundle $97')
    m = re.search(r'class="price">\$(\d+)</span>', s)
    old = int(m.group(1))
    if n in INBUNDLE:
        s = re.sub(r'\$\d+ \| Spiel Ventures</title>', '(in Local Lead OS bundle) | Spiel Ventures</title>', s)
        s = re.sub(r'\$\d+\. Email WANT [A-Z0-9 ]+\.', 'Included in the Local Lead OS bundle ($97); not sold separately.', s)
        s = s.replace('<span class="price">$%d</span>' % old, '<span class="price">In Local Lead OS · $97</span>')
        s = re.sub(r'<a class="btn-buy" href="mailto:tommytbomar@gmail.com\?subject=WANT%20[^"]+">Email · WANT [^<]+</a>',
                   '<a class="btn-buy" href="mailto:tommytbomar@gmail.com?subject=WANT%20LOCAL%20LEAD%20OS">Email · WANT LOCAL LEAD OS ($97)</a>', s)
        s = re.sub(r'Email <b>WANT [A-Z0-9 ]+</b> to tommytbomar@gmail.com', 'Email <b>WANT LOCAL LEAD OS</b> to tommytbomar@gmail.com', s)
        s = re.sub(r'<div class="card"><p><b>Which price\?</b>.*?</p></div>', '', s)
        card = ('<div class="card"><p><b>Not sold separately.</b> This pack is a module of the <a href="100-local-lead-os-bundle.html">Local Lead OS bundle ($97)</a>, '
                'which also includes the Mobile Lead Fix Kit and the other bundle modules.</p></div>')
        assert '<footer>' in s
        s = s.replace('<footer>', card + '<footer>', 1)
    elif n in VERT:
        new = VERT[n]
        if new != old:
            s = s.replace('$%d | Spiel Ventures</title>' % old, '$%d | Spiel Ventures</title>' % new)
            s, c = re.subn(r'\$%d\. Email WANT' % old, '$%d. Email WANT' % new, s); assert c == 1, p
            s = s.replace('<span class="price">$%d</span>' % old, '<span class="price">$%d</span>' % new)
    # n == 85 unchanged ($79)
    wr(p, s)

# bundle page extras
sub('products/100-local-lead-os-bundle.html', '<div class="card"><p><b>Is the Payhip Mobile Lead Fix Kit different?',
    '<div class="card"><h2>Licenses</h2><p><b>Owner license — $97</b> (this page): use everything in your own business.</p>'
    '<p><b>Agency License — $197:</b> use it across your agency team and client work, white-label the worksheets under your brand. Not for resale as a competing product. <a href="../white-label.html">Agency License details</a> · email <b>WANT AGENCY LICENSE</b>.</p>'
    '<p><b>Sold only inside this bundle:</b> Hours-of-Operation Fix Pack, Missed-Call SMS Scripts, Google Review Request Kit, After-Hours Voicemail Scripts, Schema Markup Snippet Pack, Speed Budget One-Pager, GBP Post Calendar (52 weeks) and Review Response Bank (100 replies).</p></div>'
    '<div class="card"><p><b>Is the Payhip Mobile Lead Fix Kit different?')

# retired product pages
stub('products/38-email-signature-lead-cta-pack.html', 'Email Signature Lead CTA Pack — retired', 'products.html',
     'This pack was retired on 2026-10-01 and is no longer sold. The current product list is on the products page.', '../')
stub('products/86-family-reunion-album-sprint.html', 'Family Reunion Album Sprint — retired', 'photo-restore-order.html',
     'This product was retired on 2026-10-01. Use the 10-photo album ($299, up to 10 photos; captioned layout +$50) on the photo restore page.', '../')
stub('products/87-wedding-heirloom-restore-pack.html', 'Wedding Heirloom Restore Pack — retired', 'photo-restore-order.html',
     'This product was retired on 2026-10-01. Use the 3-photo pack ($99) or the 10-photo album ($299) on the photo restore page.', '../')
# retired creator packs + hub
for f, ttl in (('packs-podcast-show-notes.html','Podcast Show Notes Template Pack'),('packs-linkedin-30-day.html','LinkedIn Local-Biz Post Pack'),
               ('packs-intake-forms.html','Fillable Intake Forms Pack'),('packs-ad-briefs.html','Canva-Free Static Ad Creative Briefs')):
    stub(f, ttl + ' — retired', 'products.html', 'This pack was retired on 2026-10-01 and is no longer sold. See the current products and the Local Lead OS bundle.')
stub('creator-packs.html', 'Creator packs — retired', 'products.html',
     'The podcast, LinkedIn, intake-form and ad-brief packs were retired on 2026-10-01. Current digital products are on the products page.')

# nav / hub links to the retired hub
for p in allhtml:
    if p == 'creator-packs.html' or p.startswith('packs-'): continue
    s = rd(p)
    s2 = re.sub(r'href="((?:\.\./)?)creator-packs\.html">Digital packs</a>', r'href="\1products.html">Digital packs</a>', s)
    if s2 != s: wr(p, s2)
sub('index.html', '<li><a href="creator-packs.html">Podcast, LinkedIn, intake-form &amp; ad-brief packs</a></li>',
    '<li><a href="products.html">Digital packs and the Local Lead OS bundle</a></li>')
sub('sample-intake-form.html', '<a href="packs-intake-forms.html">← Intake Forms Pack</a> · <a href="creator-packs.html">All packs</a>', '<a href="products.html">← All products</a>')
sub('sample-intake-form.html', ' The full pack has 6 forms.', ' This is a free sample.')
sub('roadmap.html', '<li><strong>Digital packs</strong> — Podcast notes, LinkedIn 30, intake forms, ad briefs.</li>', '<li><strong>Digital packs</strong> — vertical packs and the Local Lead OS bundle.</li>')
sub('roadmap.html', '<li><strong>Bundle</strong> — several packs at one price.</li>', '<li><strong>Bundle</strong> — shipped as Local Lead OS ($97).</li>')

# products.html table
s = rd('products.html')
def fixrow(m):
    row = m.group(0); n = m.group(1).zfill(2) if int(m.group(1)) < 100 else m.group(1)
    if n in ('38','86','87'): return ''
    if n in INBUNDLE: return re.sub(r'<td class="price">\$\d+</td>', '<td class="price">In bundle</td>', row)
    if n in VERT: return re.sub(r'<td class="price">\$\d+</td>', '<td class="price">$%d</td>' % VERT[n], row)
    return row
s = re.sub(r'<tr><td>(\d+)</td>.*?</tr>\n?', lambda m: (fixrow(m) + ('\n' if fixrow(m) else '')), s)
cnt = len(re.findall(r'<tr><td>\d+</td>', s))
s = re.sub(r'<p class="lead">\d+ products', '<p class="lead">%d products' % cnt, s)
s = s.replace('<table class="t">', '<p class="note" style="margin-top:.5rem">Rows marked <b>In bundle</b> are included in the Local Lead OS bundle ($97) and are not sold separately. Mobile Lead Fix Kit: $47 on Payhip.</p>\n<table class="t">', 1)
wr('products.html', s)

# ---------------------------------------------------------------- 3. kit / source ZIP links, mobile-lead-form-kit -> mobile-lead-fix-kit
ZIP = 'https://codeload.github.com/tommytbomar-dot/mobile-lead-form-kit/zip/refs/heads/main'
sub('kit.html', 'Public source archive (same pack files): <a href="%s">Download ZIP</a>' % ZIP, 'Public source on GitHub (same pack files): <a href="%s">mobile-lead-fix-kit repo</a>' % KITREPO)
sub('offers.html', '<a href="%s">Public source ZIP</a>' % ZIP, '<a href="%s">Public source (GitHub)</a>' % KITREPO)
sub('index.html', '<a href="%s">Public source ZIP</a>' % ZIP, '<a href="%s">Public source (GitHub)</a>' % KITREPO)
for p in allhtml:
    s = rd(p)
    if 'mobile-lead-form-kit' in s and p != 'white-label.html':
        wr(p, s.replace('mobile-lead-form-kit', 'mobile-lead-fix-kit'))

# ---------------------------------------------------------------- 4. photo ladder + offers/index/order
LADDER_OFFERS = ('<li><span class="price">$29</span> — single light restore</li>\n<li><span class="price">$59</span> — single repair (scratches / fade)</li>\n'
                 '<li><span class="price">$99</span> — 3-photo pack (up to 3 photos, repair level)</li>\n<li><span class="price">$299</span> — family album (up to 10 photos; captioned layout +$50)</li>')
sub('offers.html', '<li><span class="price">$29</span> — single light restore</li>\n<li><span class="price">$79</span> — single plus (scratches / fade)</li>\n<li><span class="price">$149</span> — 3-photo pack</li>\n<li><span class="price">$497</span> — family album (10 photos)</li>', LADDER_OFFERS)
sub('offers.html', '<h2>Deep Mobile Audit PDF <span class="price">$147</span></h2>\n<p>We run the audit on your live URL and send a PDF. Include the URL in your email.</p>',
    '<h2>Deep Mobile Audit PDF <span class="price">$147</span></h2>\n<p>We run the audit on your live URL and send a PDF. Include the URL in your email. Want the 10-minute video walkthrough too? <b>$197</b> total — email <b>WANT AUDIT VIDEO</b>.</p>')
sub('offers.html', '<div class="card">\n<h2>4K Photo Restore packs</h2>',
    '<div class="card">\n<h2>Local Lead OS bundle <span class="price">$97</span></h2>\n<p>The Mobile Lead Fix Kit plus eight working modules, a self-audit and a 30-day plan. Agency License $197 for client work. <a href="products/100-local-lead-os-bundle.html">Details</a> · <a href="pricing.html">Full price list</a></p>\n<a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20LOCAL%20LEAD%20OS">Email · WANT LOCAL LEAD OS</a>\n</div>\n\n<div class="card">\n<h2>4K Photo Restore packs</h2>')
sub('index.html', '<h2>4K Photo Restore <span class="price">$29–$497</span></h2>\n<p>Natural faces, printable ~4K. Packs: $29 · $79 · $149 · $497. Not waxy AI redraw.</p>',
    '<h2>4K Photo Restore <span class="price">$29–$299</span></h2>\n<p>Natural faces, printable ~4K. $29 light · $59 repair · $99 3-photo pack · $299 10-photo album. Not waxy AI redraw.</p>')
sub('index.html', '<div class="card">\n<h2>How payment works</h2>',
    '<div class="card">\n<h2>Local Lead OS bundle <span class="price">$97</span></h2>\n<p>Kit + eight modules + 30-day plan in one ZIP. <a href="pricing.html">See every price</a>.</p>\n<a class="btn" href="products/100-local-lead-os-bundle.html">Details</a>\n</div>\n<div class="card">\n<h2>How payment works</h2>')
sub('index.html', 'booking page, Loom audit)', 'booking page, audit + video)')
sub('index.html', '<meta name="description" content="Mobile Lead Fix Kit $47 on Payhip, Deep Mobile Audit $147, photo restore packs.', '<meta name="description" content="Mobile Lead Fix Kit $47 on Payhip, Deep Mobile Audit $147, Local Lead OS $97, photo restore from $29.')

# order.html
sub('order.html', '<h2>Deep Mobile Audit PDF <span class="price">$97</span></h2>\n<p>Written audit of your live URL. Include the URL in your email.</p>',
    '<h2>Deep Mobile Audit PDF <span class="price">$147</span></h2>\n<p>Written audit of your live URL. Include the URL in your email. Add a 10-minute video walkthrough: <b>$197</b> total (subject WANT AUDIT VIDEO).</p>')
sub('order.html', '<li><span class="price">$29</span> single · <span class="price">$79</span> plus · <span class="price">$149</span> 3-pack · <span class="price">$497</span> album</li>',
    '<li><span class="price">$29</span> light · <span class="price">$59</span> repair · <span class="price">$99</span> 3-pack · <span class="price">$299</span> 10-photo album</li>')
sub('order.html', '<h2>White-label kit license <span class="price">$97 / $197</span></h2>\n<p>Freelancers &amp; agencies: use the kit with clients. Personal $97 · Commercial $197.</p>\n<div class="btn-row">\n  <a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20WHITE%20LABEL">Email · WANT WHITE LABEL</a>\n  <a class="btn-secondary" href="white-label.html">License terms</a>',
    '<h2>Local Lead OS <span class="price">$97</span> · Agency License <span class="price">$197</span></h2>\n<p>Owner bundle $97 for your own business. Agency License $197 for client work and white-label use.</p>\n<div class="btn-row">\n  <a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20LOCAL%20LEAD%20OS">Email · WANT LOCAL LEAD OS</a>\n  <a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20AGENCY%20LICENSE">Email · WANT AGENCY LICENSE</a>\n  <a class="btn-secondary" href="white-label.html">License terms</a>')
sub('order.html', '<p class="muted"><a href="index.html">Home</a> · <a href="offers.html">Offers</a> · <a href="kit.html">Kit</a></p>', '<p class="muted"><a href="index.html">Home</a> · <a href="offers.html">Offers</a> · <a href="pricing.html">Pricing</a> · <a href="kit.html">Kit</a></p>')

# photo pages
sub('photo-restore-order.html', 'Packs $29–$497. Email PHOTO RESTORE.', 'From $29 (light) to $299 (10-photo album). Email PHOTO RESTORE.')
sub('photo-restore-order.html', '"price":"79","priceCurrency":"USD","name":"Plus"', '"price":"59","priceCurrency":"USD","name":"Repair"')
sub('photo-restore-order.html', '"price":"149","priceCurrency":"USD","name":"3-pack"', '"price":"99","priceCurrency":"USD","name":"3-pack"')
sub('photo-restore-order.html', '"price":"497","priceCurrency":"USD","name":"Album"', '"price":"299","priceCurrency":"USD","name":"Album"')
sub('photo-restore-order.html', '<li><span class="price">$29</span> single photo</li><li><span class="price">$79</span> plus (harder damage)</li><li><span class="price">$149</span> 3-pack</li><li><span class="price">$497</span> 10-photo album</li>',
    '<li><span class="price">$29</span> single light restore (dust, contrast, color)</li><li><span class="price">$59</span> single repair (scratches, tears, fade, harder damage)</li><li><span class="price">$99</span> 3-photo pack (up to 3 photos, repair level)</li><li><span class="price">$299</span> 10-photo album (up to 10 photos; captioned layout +$50)</li><li><span class="price">$79</span> memorial / obituary rush (1 photo, 24–48 h)</li>')
sub('restore-faded-family-photos.html', '$29 single light · $79 single plus · $149 three-photo · $497 ten-photo album.', '$29 light · $59 repair · $99 three-photo pack · $299 ten-photo album.')
sub('sops/photo-fulfill.html', '($29 / $79 / $149 / $497)', '($29 light / $59 repair / $99 3-photo / $299 10-photo album)')
sub('README.md', 'WANT AUDIT ($147 + URL) · PHOTO RESTORE ($29/$79/$149/$497)', 'WANT AUDIT ($147 + URL) · WANT AUDIT VIDEO ($197) · PHOTO RESTORE ($29/$59/$99/$299)')
sub('sops/order-watch.html', 'WANT WHITE LABEL · BOOK SLOT', 'WANT AGENCY LICENSE · BOOK SLOT')
sub('faq.html', 'White-label: <strong>WANT WHITE LABEL</strong>', 'Agency License: <strong>WANT AGENCY LICENSE</strong>')

# ---------------------------------------------------------------- 5. audit page (+ video merge)
sub('audit.html', '<meta name="description" content="What you get in the $147 Deep Mobile Lead Audit PDF from Tommy Bomar / Spiel Ventures.', '<meta name="description" content="What you get in the $147 Deep Mobile Lead Audit PDF (or $197 with a 10-minute video) from Tommy Bomar / Spiel Ventures.')
sub('audit.html', '<div class="card">\n<h2>Not included</h2>',
    '<div class="card">\n<h2>Add the 10-minute video — <span class="price">$197</span> total</h2>\n<p>The same PDF plus a recorded walkthrough (about 10 minutes) of your site on a phone-size screen, with the highest-impact fixes shown on screen. The link stays up so you can share it with your web person. Delivered in about 2-3 business days.</p>\n<a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20AUDIT%20VIDEO">Email · WANT AUDIT VIDEO + your URL</a>\n<p class="buy-note">This replaces the old separate screenshot/video audit page.</p>\n</div>\n\n<div class="card">\n<h2>Not included</h2>')
sub('audit.html', 'Payhip Audit listing may go live next — until then mailto + Venmo/PayPal/Zelle.', 'There is no Payhip audit listing yet — order by email and pay by Venmo/PayPal/Zelle.')

# ---------------------------------------------------------------- 6. services + svc pages
stub('svc-loom-audit.html', 'Mobile Screenshot Audit — now part of the Audit page', 'audit.html',
     'The separate video audit was merged into the Deep Mobile Audit: PDF $147, or PDF plus a 10-minute video walkthrough $197.')
sub('svc-map-pack-rescue.html', 'Map-Pack Rescue $497 | Spiel Ventures', 'Map-Pack Rescue $597 | Spiel Ventures')
sub('svc-map-pack-rescue.html', '<span class="price">$497</span>', '<span class="price">$597</span>')
sub('svc-map-pack-rescue.html', '<div class="card"><h2>What I need from you</h2>', '<div class="card"><h2>Add-ons and bundles</h2><ul><li><b>Map-Pack + CTA Rescue — $797:</b> this plus the One-Day Homepage CTA Rescue (<a href="svc-map-pack-cta-rescue.html">details</a>)</li><li><b>Citation Cleanup research — +$150</b> when added to this rescue (<a href="svc-citation-cleanup-dfy.html">details</a>)</li></ul></div>\n<div class="card"><h2>What I need from you</h2>')
mp = rd('svc-map-pack-rescue.html')
newpage = mp.replace('Map-Pack Rescue $597 | Spiel Ventures', 'Map-Pack + CTA Rescue $797 | Spiel Ventures')
newpage = newpage.replace('<h1>Map-Pack Rescue</h1>', '<h1>Map-Pack + CTA Rescue</h1>')
newpage = re.sub(r'<meta name="description" content="[^"]*"/>', '<meta name="description" content="Map-Pack Rescue plus the One-Day Homepage CTA Rescue in one package: fix your Google Business Profile and the call-to-action path on your homepage. $797."/>', newpage, count=1)
newpage = re.sub(r'<p class="lead">.*?</p>', '<p class="lead">Both fixes in one order: your Google Business Profile and local signals, plus the call-to-action path on your homepage. One location, one primary city, one page.</p>', newpage, count=1)
newpage = newpage.replace('<span class="price">$597</span>', '<span class="price">$797</span>').replace('WANT%20MAP-PACK%20RESCUE', 'WANT%20MAP-PACK%20CTA%20RESCUE').replace('Email: WANT MAP-PACK RESCUE', 'Email: WANT MAP-PACK CTA RESCUE')
newpage = re.sub(r'<div class="card"><h2>Add-ons and bundles</h2>.*?</div>\n', '', newpage, flags=re.S)
newpage = newpage.replace('<div class="card"><h2>What you get</h2><ul>', '<div class="card"><h2>What you get</h2><p>Everything in <a href="svc-map-pack-rescue.html">Map-Pack Rescue</a> ($597) plus the <a href="svc-cta-rescue.html">One-Day Homepage CTA Rescue</a> ($297) — $97 less than buying both separately.</p><ul><li><b>Homepage CTA fix:</b> tap-to-call button and sticky mobile bar, above-the-fold headline with one clear action, form cut to the minimum fields, fixes for broken or buried buttons and links, before/after list of what changed (screenshots of your own site)</li>', 1)
newpage = newpage.replace('<li>About 20 minutes on a call or email thread to confirm facts</li>', '<li>About 20 minutes on a call or email thread to confirm facts</li><li>Edit access to the homepage (WordPress, Wix, Squarespace, Webflow, HTML/GitHub), or I send copy-paste changes at a reduced scope</li>')
newpage = newpage.replace('Delivered in about 7 business days after access is granted.', 'Map-Pack work in about 7 business days after access is granted; homepage CTA fix within about 1 business day of receiving edit access (longer for locked-down builders). One page only; no conversion or ranking guarantee.')
assert 'CTA RESCUE' in newpage and '$797' in newpage
wr('svc-map-pack-cta-rescue.html', newpage)

sub('svc-citation-cleanup-dfy.html', 'Cleanup (Done-For-You Research) $297 | Spiel', 'Cleanup (Done-For-You Research) $197 | Spiel')
sub('svc-citation-cleanup-dfy.html', '<span class="price">$297</span> <span class="muted">one-time</span>', '<span class="price">$197</span> <span class="muted">one-time · or +$150 added to a Map-Pack Rescue</span>')

sub('svc-booking-page-dfy.html', '(Done-For-You) $397-$897 | Spiel', '(Done-For-You) Quote $497 / Booking $997 | Spiel')
sub('svc-booking-page-dfy.html', '<span class="price">$397-$897</span> <span class="muted">one-time</span>', '<span class="price">Quote Page $497</span> · <span class="price">Booking Page $997</span> <span class="muted">one-time</span>')
sub('svc-booking-page-dfy.html', '<li><b>$397:</b> one-page', '<li><b>Quote Page $497:</b> one-page')
sub('svc-booking-page-dfy.html', '<li><b>$897:</b> multi-service', '<li><b>Booking Page $997:</b> multi-service')

sub('svc-review-reply-setup.html', '$197 + $47/mo | Spiel', '$197 + $79/mo | Spiel')
sub('svc-review-reply-setup.html', '<span class="price">$197 + $47/mo</span>', '<span class="price">$197 + $79/mo</span>')
sub('svc-review-reply-setup.html', '<b>Optional $47/mo:</b>', '<b>Optional $79/mo:</b>')

sub('svc-site-health-care.html', 'Site Health Care Plan $97-$149 | Spiel', 'Site Health Care Plan: Watch $97/mo, Care $179/mo | Spiel')
sub('svc-site-health-care.html', '<span class="price">$97-$149</span> <span class="muted">per month</span>', '<span class="price">Watch $97</span> · <span class="price">Care $179</span> <span class="muted">per month</span>')
sub('svc-site-health-care.html', '<b>$97/mo:</b> monthly re-grade', '<b>Watch — $97/mo:</b> monthly re-grade')
sub('svc-site-health-care.html', '<b>$149/mo:</b> everything above', '<b>Care — $179/mo:</b> everything above')
sub('svc-site-health-care.html', '(for the $149 plan)', '(for the Care plan)')
sub('svc-site-health-care.html', '(Loom audit, CTA Rescue or Map-Pack Rescue)', '(audit + video, CTA Rescue or Map-Pack Rescue)')

sub('svc-agency-audit-wholesale.html', 'for Agencies $67 | Spiel', 'for Agencies $97 | Spiel')
sub('svc-agency-audit-wholesale.html', '<span class="price">$67</span> <span class="muted">per audit, wholesale</span>', '<span class="price">$97</span> <span class="muted">per audit, wholesale · $79 each at 10+ audits a month</span>')
sub('svc-agency-audit-wholesale.html', "<a href='white-label.html'>white-label kit</a>", "<a href='white-label.html'>Agency License</a>")
sub('svc-agency-audit-wholesale.html', 'Start with one URL. Volume terms are by email.', 'Start with one URL. 10+ audits a month: $79 each. (Retail price of the same audit on this site: $147.)')

# photo wholesale: one rate card + partner rule
pw = 'svc-photo-wholesale.html'
sub(pw, 'Wholesale (Batch) $2-$5 | Spiel', 'Wholesale (Batch) $9-$25 per photo | Spiel')
sub(pw, '<p class="lead">Batch restoration for genealogists, archivists and local historical societies.', '<p class="lead">Batch restoration for photographers, genealogists, archivists and local historical societies.')
sub(pw, '<span class="price">$2-$5</span> <span class="muted">per photo, batch</span>', '<span class="price">$9-$25</span> <span class="muted">per photo, by volume</span>')
sub(pw, '<li><b>$2/photo:</b> dust, contrast and color cleanup (minimum 25 photos)</li><li><b>$5/photo:</b> scratch, tear and fade repair (minimum 10 photos)</li>',
    '<li><b>Rate card (per photo, by photos in the order):</b></li>'
    '<li><b>Light restore</b> (dust, contrast, color cleanup): <b>$15</b> for 1-9 · <b>$13</b> for 10-24 · <b>$9</b> for 25+</li>'
    '<li><b>Repair</b> (scratch, tear and fade repair): <b>$25</b> for 1-9 · <b>$22</b> for 10-24 · <b>$18</b> for 25+</li>'
    '<li>You invoice your own client at your own retail price; this one rate card is the same for every wholesale buyer</li>')
sub(pw, '<div class="card"><h2>What I need from you</h2>', '<div class="card"><h2>Partner discount (referral partners)</h2><ul><li>Realtors, funeral homes and other referral partners who order from the <a href="photo-restore-order.html">retail photo ladder</a> get <b>15% off</b>, or <b>20% off</b> on 3+ orders.</li><li>One rule for every partner; it does not stack with the wholesale rate card.</li></ul></div>\n<div class="card"><h2>What I need from you</h2>')

# services hub cards
s = rd('services.html')
s = s.replace('Map-Pack Rescue $497,', 'Map-Pack Rescue $597,')
lines = s.split('\n'); out = []
for ln in lines:
    if 'svc-map-pack-rescue.html">Map-Pack Rescue</a>' in ln:
        ln = ln.replace('<span class="price">$497</span>', '<span class="price">$597</span>')
        out.append(ln)
        out.append('<div class="card"><h2><a href="svc-map-pack-cta-rescue.html">Map-Pack + CTA Rescue</a> <span class="price">$797</span> <span class="muted">one-time</span></h2><p>Map-Pack Rescue plus the One-Day Homepage CTA Rescue in one order: your Google profile and your homepage call path, fixed together.</p><a class="btn-secondary" href="svc-map-pack-cta-rescue.html">Details</a></div>')
        continue
    if 'svc-site-health-care.html">Site Health Care Plan</a>' in ln:
        ln = ln.replace('<span class="price">$97-$149</span>', '<span class="price">Watch $97 · Care $179</span>')
    if 'svc-booking-page-dfy.html">Booking / Quote Page' in ln:
        ln = ln.replace('<span class="price">$397-$897</span>', '<span class="price">Quote $497 · Booking $997</span>')
    if 'svc-review-reply-setup.html">Review Reply Setup' in ln:
        ln = ln.replace('$197 + $47/mo', '$197 + $79/mo')
    if 'svc-citation-cleanup-dfy.html">Citation Cleanup' in ln:
        ln = ln.replace('<span class="price">$297</span> <span class="muted">one-time</span>', '<span class="price">$197</span> <span class="muted">one-time (+$150 as a Map-Pack add-on)</span>')
    if 'svc-loom-audit.html">Mobile Screenshot Audit' in ln:
        out.append('<div class="card"><h2><a href="audit.html">Deep Mobile Audit</a> <span class="price">PDF $147 · PDF + 10-min video $197</span> <span class="muted">one-time</span></h2><p>A plain-English audit of your live URL on phones. Add a recorded 10-minute walkthrough with the top fixes for $197 total.</p><a class="btn-secondary" href="audit.html">Details</a></div>')
        continue
    if 'svc-agency-audit-wholesale.html">White-Label' in ln:
        ln = ln.replace('<span class="price">$67</span> <span class="muted">per audit, wholesale</span>', '<span class="price">$97</span> <span class="muted">per audit, wholesale ($79 at 10+/mo)</span>').replace("white-label kit</a>", "Agency License</a>")
    if 'svc-photo-wholesale.html">Photo Restore Wholesale' in ln:
        ln = ln.replace('<span class="price">$2-$5</span> <span class="muted">per photo, batch</span>', '<span class="price">$9-$25</span> <span class="muted">per photo, by volume</span>').replace('for genealogists, archivists and local historical societies', 'for photographers, genealogists, archivists and local historical societies')
    out.append(ln)
s = '\n'.join(out)
s = s.replace('Office hours ($97 / 30 min)', 'Office hours ($125 / 30 min)')
s = s.replace('video audit and wholesale options', 'audit + video and wholesale options')
s = s.replace('<li><a href="offers.html">Kit, audit and photo packs</a></li>', '<li><a href="pricing.html">Full price list</a></li><li><a href="offers.html">Kit, audit and photo packs</a></li>')
wr('services.html', s)
for chk in ('$297</span> <span class="muted">one-time</span></h2><p>I find', '$67', '$2-$5', '$147</span> <span class="muted">one-time</span></h2><p>A recorded', 'Office hours ($97'):
    assert chk not in s, chk

# office hours / community / OSS
s = rd('office-hours.html'); assert '$97' in s; wr('office-hours.html', s.replace('$97', '$125'))
sub('community.html', '- $97 per 30 minutes', '- $125 per 30 minutes')

# ---------------------------------------------------------------- 7. Agency License pages (replace kit-only white-label license)
LIC = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
 '<title>Local Lead OS Agency License — $197 | Spiel Ventures</title>\n'
 '<meta name="description" content="Local Lead OS Agency License $197: use the bundle across your agency team and client work, with white-label worksheets. Owner license is $97. Tommy Bomar / Spiel Ventures."/>\n'
 '<link rel="canonical" href="https://tommytbomar-dot.github.io/white-label.html"/>\n<link rel="stylesheet" href="assets/site.css"/>\n</head>\n<body>\n<main>\n'
 + NAV + '\n<h1>Local Lead OS — Agency License <span class="price">$197</span></h1>\n'
 '<p class="lead">For freelancers and agencies who use the system on client work. Tommy Bomar / Spiel Ventures.</p>\n'
 '<div class="card"><h2>What you get</h2><p>The full <a href="products/100-local-lead-os-bundle.html">Local Lead OS bundle</a> (the four Mobile Lead Fix Kit checklists plus eight modules, a self-audit worksheet, a 30-day plan and a tracker) with agency rights.</p>'
 '<p>Source for the free kit checklists is public: <a href="https://github.com/tommytbomar-dot/mobile-lead-fix-kit">mobile-lead-fix-kit on GitHub</a>.</p></div>\n'
 '<div class="card"><h2>Agency License — <span class="price">$197</span></h2><ul>'
 '<li>Use across your agency team and client work</li><li>White-label the worksheets and checklists with your own brand</li>'
 '<li>Do not republish or resell the files as a competing digital product</li><li>No invented Spiel Ventures case studies</li><li>One license per agency entity</li></ul></div>\n'
 '<div class="card"><h2>Owner license — <span class="price">$97</span></h2><p>Same bundle for use in your own business. Not for client work or white-labeling.</p>'
 '<div class="btn-row"><a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20LOCAL%20LEAD%20OS">Email · WANT LOCAL LEAD OS ($97)</a></div></div>\n'
 '<div class="card"><h2>Replaces the old kit-only licenses</h2><p>The earlier kit-only personal ($97) and commercial ($197) licenses are retired; the Agency License covers that use and the whole bundle.</p></div>\n'
 '<div class="card"><h2>Not included</h2><p>Custom implementation, ads setup, ranking guarantees, or support SLAs.</p><div class="btn-row">'
 '<a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20AGENCY%20LICENSE">Email · WANT AGENCY LICENSE</a>'
 '<a class="btn-secondary" href="https://payhip.com/b/ByJMd">Buy consumer Kit $47</a></div>'
 '<p class="buy-note">Pay via PayPal / Venmo / Zelle as agreed. Identity: Tommy Bomar / Spiel Ventures.</p></div>\n'
 '<footer>\n<p>© Spiel Ventures · Tommy Bomar · tommytbomar@gmail.com</p>\n</footer>\n</main>\n</body>\n</html>\n')
wr('white-label.html', LIC)
wr('white-label-onepager.html', ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Agency License One-Pager | Spiel Ventures</title>'
 '<meta name="description" content="One-pager for freelancers and agencies: Local Lead OS Agency License $197 (owner license $97). Spiel Ventures."/><meta name="robots" content="index,follow"/>'
 '<link rel="canonical" href="https://tommytbomar-dot.github.io/white-label-onepager.html"/><link rel="stylesheet" href="assets/site.css"/></head><body><main>' + NAV +
 '<h1>Agency License — one-pager</h1><p class="lead">For freelancers &amp; tiny agencies · use Local Lead OS on client work under your own brand</p>'
 '<div class="card"><h2>What you get</h2><ul><li>The full Local Lead OS bundle with agency rights: team and client use, white-label worksheets</li>'
 '<li>Agency License <span class="price">$197</span> · Owner license (own business only) <span class="price">$97</span></li><li>No invented client logos — you bring your own delivery</li></ul>'
 '<a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20AGENCY%20LICENSE">WANT AGENCY LICENSE</a><a class="btn-secondary" href="white-label.html" style="margin-left:.5rem">Full terms</a></div>'
 + FOOT + '</main></body></html>\n'))

# ---------------------------------------------------------------- 8. pricing.html (authoritative)
def row(name, price, notes, subject=None, link=None):
    nm = '<a href="%s">%s</a>' % (link, name) if link else name
    od = '<a href="%s%s">%s</a>' % (M, subject.replace(' ', '%20'), subject) if subject else '—'
    return '<tr><td>%s</td><td class="price">%s</td><td>%s</td><td>%s</td></tr>' % (nm, price, notes, od)
def table(rows):
    return '<table class="t"><tr><th>Item</th><th>Price</th><th>What it is</th><th>Order (email subject)</th></tr>' + ''.join(rows) + '</table>'
def pl(n, name): return '<a href="products/%s">%s</a>' % (n, name)
P29 = [pl('09-accessibility-quick-pass-checklist-wcag-lite.html','Accessibility Quick-Pass #09'), pl('12-airbnb-listing-headline-formula-pack.html','Airbnb Headline Formula #12'), pl('14-church-nonprofit-donation-page-checklist.html','Church/Nonprofit Donation Checklist #14'), pl('17-hvac-emergency-banner-snippet-pack.html','HVAC Emergency Banner #17'), pl('20-salon-booking-link-fix-checklist.html','Salon Booking-Link Checklist #20'), pl('22-multi-location-nap-spreadsheet-template.html','Multi-Location NAP Spreadsheet #22'), pl('23-citation-cleanup-tracker-sheets.html','Citation Cleanup Tracker #23'), '<a href="tools/n8n-templates/">n8n Lead Workflow Pack</a>']
P39 = [pl('01-nap-consistency-checker-trades.html','NAP Consistency Checker #01'), pl('05-qr-code-menu-call-cta-pack-food.html','QR Menu → Call CTA #05'), pl('07-competitor-screenshot-diff-report-kit.html','Competitor Screenshot Diff #07'), pl('11-vacation-rental-welcome-book-template-galveston.html','STR Welcome Book #11'), pl('16-dentist-new-patient-form-kit.html','Dentist New-Patient Form Kit #16'), pl('19-auto-shop-online-quote-form-pack.html','Auto Shop Quote Form #19'), pl('21-restaurant-online-order-path-map.html','Restaurant Online-Order Path Map #21')]
P49 = [pl('13-property-manager-lead-site-wireframe-pack.html','Property-Manager Wireframes #13'), pl('15-attorney-intake-form-ux-pack.html','Attorney Intake Form UX #15'), pl('18-roofing-storm-season-landing-wireframe.html','Roofing Storm Landing Wireframe #18')]
PRICING = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
 '<title>Pricing — every price in one place | Spiel Ventures | Tommy Bomar</title>'
 '<meta name="description" content="Every Spiel Ventures price: audit $147, audit + video $197, Map-Pack Rescue $597, quote page $497, Site Care $179/mo, office hours $125, Local Lead OS $97, photo restore from $29, kit $47."/>'
 '<meta name="robots" content="index,follow"/><link rel="canonical" href="https://tommytbomar-dot.github.io/pricing.html"/><link rel="stylesheet" href="assets/site.css"/><link rel="stylesheet" href="assets/products.css"/>'
 '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"OfferCatalog","name":"Spiel Ventures offers","itemListElement":['
 '{"@type":"Offer","price":"47","priceCurrency":"USD","name":"Mobile Lead Fix Kit"},{"@type":"Offer","price":"97","priceCurrency":"USD","name":"Local Lead OS bundle (owner license)"},'
 '{"@type":"Offer","price":"197","priceCurrency":"USD","name":"Local Lead OS Agency License"},{"@type":"Offer","price":"147","priceCurrency":"USD","name":"Deep Mobile Audit PDF"},'
 '{"@type":"Offer","price":"197","priceCurrency":"USD","name":"Deep Mobile Audit PDF + 10-minute video"},{"@type":"Offer","price":"297","priceCurrency":"USD","name":"One-Day Homepage CTA Rescue"},'
 '{"@type":"Offer","price":"597","priceCurrency":"USD","name":"Map-Pack Rescue"},{"@type":"Offer","price":"797","priceCurrency":"USD","name":"Map-Pack + CTA Rescue"},'
 '{"@type":"Offer","price":"497","priceCurrency":"USD","name":"Quote Page"},{"@type":"Offer","price":"997","priceCurrency":"USD","name":"Booking Page"},'
 '{"@type":"Offer","price":"125","priceCurrency":"USD","name":"Office hours (30 minutes)"},{"@type":"Offer","price":"29","priceCurrency":"USD","name":"Photo restore, light"},'
 '{"@type":"Offer","price":"59","priceCurrency":"USD","name":"Photo restore, repair"},{"@type":"Offer","price":"99","priceCurrency":"USD","name":"Photo restore, 3-photo pack"},'
 '{"@type":"Offer","price":"299","priceCurrency":"USD","name":"Photo restore, 10-photo album"}]}\n</script></head><body><main>' + NAV +
 '<h1>Pricing</h1><p class="lead">USD · one price per item · no ranges · no hidden fees · email order (the kit also has instant Payhip checkout)</p>'
 '<p class="note">How to pay: email the subject shown, we agree scope in writing, you pay by Venmo / PayPal / Zelle, then work starts. The Mobile Lead Fix Kit is the one item with instant checkout (Payhip). No ranking or results guarantees on anything here.</p>'
 '<div class="card"><h2>Audits</h2>' + table([
   row('Deep Mobile Audit PDF', '$147', 'Plain-English PDF on one live URL: CTA path, form friction, NAP + hours, map-pack basics, this-week vs later fixes', 'WANT AUDIT', 'audit.html'),
   row('Audit + 10-minute video', '$197', 'The same PDF plus a recorded phone-screen walkthrough (replaces the old separate video audit)', 'WANT AUDIT VIDEO', 'audit.html'),
   row('White-label audit (agencies)', '$97 per audit', '$79 each at 10+ audits a month; branded PDF you resell', 'WANT AGENCY AUDIT', 'svc-agency-audit-wholesale.html')]) + '</div>'
 '<div class="card"><h2>Fix services (one-time)</h2>' + table([
   row('One-Day Homepage CTA Rescue', '$297', 'One page, one problem: the call-to-action path on phones', 'WANT CTA RESCUE', 'svc-cta-rescue.html'),
   row('Map-Pack Rescue', '$597', 'Google Business Profile and local signals; one location, one city', 'WANT MAP-PACK RESCUE', 'svc-map-pack-rescue.html'),
   row('Map-Pack + CTA Rescue', '$797', 'Map-Pack Rescue plus the homepage CTA Rescue ($97 less than both separately)', 'WANT MAP-PACK CTA RESCUE', 'svc-map-pack-cta-rescue.html'),
   row('Citation Cleanup (research)', '$197', '+$150 when added to a Map-Pack Rescue; submission-ready fix sheet', 'WANT CITATION CLEANUP', 'svc-citation-cleanup-dfy.html'),
   row('Quote Page', '$497', 'One-page quote/contact request, click-to-call, short form, thank-you page', 'WANT BOOKING PAGE', 'svc-booking-page-dfy.html'),
   row('Booking Page', '$997', 'Multi-service booking page, service-specific forms, calendar embed, confirmation wording, schema', 'WANT BOOKING PAGE', 'svc-booking-page-dfy.html'),
   row('Review Reply Setup', '$197 setup', 'Optional $79/mo: up to 15 drafted replies a month', 'WANT REVIEW REPLY SETUP', 'svc-review-reply-setup.html')]) + '</div>'
 '<div class="card"><h2>Monthly and time-based</h2>' + table([
   row('Site Watch', '$97/mo', 'Monthly mobile re-grade with a one-page fix list; alert email if phone, hours or form break', 'WANT SITE HEALTH CARE', 'svc-site-health-care.html'),
   row('Site Care', '$179/mo', 'Everything in Watch plus up to 2 hours/month of small fixes', 'WANT SITE HEALTH CARE', 'svc-site-health-care.html'),
   row('Office hours (30 min)', '$125', 'Prep by email first, 30-minute call, written recap the same day', 'OFFICE HOURS', 'office-hours.html'),
   row('Open-source support session', '$125', 'Up to 60 minutes of email support on one of the free open-source repos, with a written follow-up (see SUPPORT.md in each repo)', 'WANT SUPPORT')]) + '</div>'
 '<div class="card"><h2>Digital products</h2>' + table([
   row('Mobile Lead Fix Kit', '$47', 'Four plain-English checklists; instant Payhip checkout', 'WANT KIT', 'kit.html'),
   row('Local Lead OS bundle (owner license)', '$97', 'The kit plus eight modules, self-audit, 30-day plan and tracker; for your own business', 'WANT LOCAL LEAD OS', 'products/100-local-lead-os-bundle.html'),
   row('Local Lead OS Agency License', '$197', 'Same bundle with agency team, client-work and white-label rights (replaces the old kit-only licenses)', 'WANT AGENCY LICENSE', 'white-label.html'),
   row('Photo Restore SOP — commercial license', '$97', 'The photo-restoration operations SOP with a white-label license for one entity', 'WANT SOP LICENSE', 'products/99-photo-restore-sop-commercial-license.html')]) + '</div>'
 '<div class="card"><h2>Vertical packs</h2><p>Three price points. Email the subject on the pack page.</p>'
 '<p><span class="price">$29</span> — ' + ' · '.join(P29) + '</p><p><span class="price">$39</span> — ' + ' · '.join(P39) + '</p><p><span class="price">$49</span> — ' + ' · '.join(P49) + '</p>'
 '<p><b>Included in the Local Lead OS bundle only (not sold separately):</b> Hours-of-Operation Fix Pack, Missed-Call SMS Scripts, Google Review Request Kit, After-Hours Voicemail Scripts, Schema Markup Snippet Pack, Speed Budget One-Pager, GBP Post Calendar (52 weeks), Review Response Bank (100 replies).</p></div>'
 '<div class="card"><h2>Photo restore</h2>' + table([
   row('Light restore (1 photo)', '$29', 'Dust, contrast, color; natural faces, printable ~4K', 'PHOTO RESTORE', 'photo-restore-order.html'),
   row('Repair (1 photo)', '$59', 'Scratches, tears, fade, harder damage', 'PHOTO RESTORE', 'photo-restore-order.html'),
   row('3-photo pack', '$99', 'Up to 3 photos, repair level', 'PHOTO RESTORE', 'photo-restore-order.html'),
   row('10-photo album', '$299', 'Up to 10 photos; captioned album layout +$50', 'PHOTO RESTORE', 'photo-restore-order.html'),
   row('Memorial / obituary rush', '$79', '1 photo, 24–48 hours, honest deadline check before you pay', 'WANT MEMORIAL RUSH', 'products/85-memorial-obituary-photo-rush.html')]) + '</div>'
 '<div class="card"><h2>Photo wholesale and partners</h2><p><b>One wholesale rate card</b> (per photo, by photos in the order) — <a href="svc-photo-wholesale.html">details</a>:</p>'
 '<table class="t"><tr><th></th><th>1–9 photos</th><th>10–24</th><th>25+</th></tr><tr><td>Light restore</td><td class="price">$15</td><td class="price">$13</td><td class="price">$9</td></tr><tr><td>Repair</td><td class="price">$25</td><td class="price">$22</td><td class="price">$18</td></tr></table>'
 '<p><b>One partner discount rule:</b> referral partners (realtors, funeral homes, others) ordering from the retail ladder get 15% off, 20% off on 3+ orders.</p>'
 '<p><a class="btn" href="mailto:tommytbomar@gmail.com?subject=WANT%20PHOTO%20WHOLESALE">Email · WANT PHOTO WHOLESALE</a></p></div>'
 '<div class="card"><h2>Retired or folded in (2026-10-01)</h2><ul><li>Separate video audit → now the $197 audit + video</li><li>Kit-only white-label licenses ($97/$197) → Local Lead OS Agency License $197</li><li>Podcast, LinkedIn, intake-form, ad-brief and email-signature packs → retired</li><li>Family Reunion Album and Wedding Heirloom packs → use the 3-photo pack or 10-photo album</li></ul></div>'
 + FOOT.replace('Inbound only. $0 ads.', 'Cold email paused — inbound only.') + '</main></body></html>\n')
wr('pricing.html', PRICING)

# ---------------------------------------------------------------- 9. changelog
s = rd('changelog.html')
s = re.sub(r'Four digital packs on the .*?ad briefs \(\$29\)\.', 'Four creator packs (podcast show notes, LinkedIn 30-day posts, fillable intake forms, Canva-free ad briefs) — since retired; the <a href="sample-intake-form.html">free sample intake form</a> stays up.', s, flags=re.S)
s = s.replace('<div class="card">\n<h2>2026-10-01 — Geo hub', '<div class="card">\n<h2>2026-10-01 — One price per item</h2>\n<ul>\n<li>New <a href="pricing.html">pricing page</a> listing every price.</li>\n<li>Audit $147; audit + 10-minute video $197 (the separate video audit page was merged into it).</li>\n<li>Map-Pack Rescue $597; new Map-Pack + CTA Rescue $797; quote page $497; booking page $997; Site Care $179/mo; office hours $125.</li>\n<li>Local Lead OS bundle $97 with a $197 Agency License; photo ladder $29 / $59 / $99 / $299; one photo wholesale rate card.</li>\n<li>Creator packs retired; eight packs now included only in the bundle.</li>\n</ul>\n</div>\n<div class="card">\n<h2>2026-10-01 — Geo hub', 1)
assert 'One price per item' in s
wr('changelog.html', s)

# ---------------------------------------------------------------- 10. privacy-friendly CTA tracking (no account) + optional GoatCounter slot
TRACK = r'''/* Spiel Ventures — privacy-friendly CTA attribution. No cookies, no third-party requests, no data leaves your browser.
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
'''
wr('assets/track.js', TRACK)
miss = []
for p in sorted(glob.glob('**/*.html', recursive=True)):
    s = rd(p)
    if 'assets/track.js' in s: continue
    if '</head>' not in s: miss.append(p); continue
    wr(p, s.replace('</head>', '<script src="/assets/track.js" defer></script></head>', 1))
print('no </head> in:', miss)

# ---------------------------------------------------------------- 11. sitemap
s = rd('sitemap.xml')
for u in ('svc-loom-audit.html','creator-packs.html','packs-ad-briefs.html','packs-intake-forms.html','packs-linkedin-30-day.html','packs-podcast-show-notes.html',
          'products/38-email-signature-lead-cta-pack.html','products/86-family-reunion-album-sprint.html','products/87-wedding-heirloom-restore-pack.html'):
    line = '<url><loc>%s%s</loc><changefreq>weekly</changefreq></url>\n' % (BASE, u)
    assert line in s, u
    s = s.replace(line, '')
anchor = '<url><loc>%ssvc-map-pack-rescue.html</loc><changefreq>weekly</changefreq></url>\n' % BASE
assert anchor in s
s = s.replace(anchor, anchor + '<url><loc>%ssvc-map-pack-cta-rescue.html</loc><changefreq>weekly</changefreq></url>\n' % BASE)
wr('sitemap.xml', s)
print('done')
