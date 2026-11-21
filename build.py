"""Build the LAPIS static website. Python standard library only."""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / 'site.json').read_text())
OUT = ROOT / 'dist'
PAGES = {
    'index': ('Immobilienverwaltung, die entlastet.', 'Persönliche Immobilienverwaltung für private Eigentümer von Mietliegenschaften in der Ostschweiz. Persönlich. Strukturiert. Verlässlich.'),
    'leistungen': ('Unsere Leistungen', 'Mietliegenschaften bewirtschaften: Administration, Vermietung, Finanzen und Unterhalt. Lernen Sie den vorgesehenen Leistungsumfang von LAPIS kennen.'),
    'eigentuemer': ('Für Eigentümer', 'Weniger Verwaltungsaufwand und mehr Überblick für private Eigentümer in St. Gallen, Thurgau und Appenzell. So beginnt die Zusammenarbeit mit LAPIS.'),
    'ueber-uns': ('Über uns', 'LAPIS entsteht als persönliche Immobilienverwaltung von zwei Gründern in der Ostschweiz. Unsere Werte: Verlässlichkeit, Transparenz, Verantwortung und Partnerschaftlichkeit.'),
    'kontakt': ('Kontakt', 'Bereiten Sie Ihr Erstgespräch mit LAPIS Immobilienverwaltung vor. Erzählen Sie uns von Ihrer Mietliegenschaft und Ihrem Anliegen.'),
    'impressum': ('Impressum', 'Angaben zur Website von LAPIS Immobilienverwaltung und Bildnachweise.'),
    'datenschutz': ('Datenschutz', 'Informationen zur Datenbearbeitung in diesem privaten Website-Entwurf von LAPIS Immobilienverwaltung.'),
    '404': ('Seite nicht gefunden', 'Diese Seite ist nicht vorhanden. Zurück zur Startseite von LAPIS Immobilienverwaltung.')
}

def header(key):
    nav = [('leistungen', 'Leistungen'), ('eigentuemer', 'Für Eigentümer'), ('ueber-uns', 'Über uns')]
    links = ''.join(f'<a href="/{p}.html"'+(' aria-current="page"' if key==p else '')+f'>{label}</a>' for p,label in nav)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt</a>
    <header class="site-header"><div class="container header-inner">
      <a class="brand" href="/" aria-label="LAPIS Immobilienverwaltung – Startseite"><img src="/assets/lapis-logo.png" width="1331" height="373" alt="LAPIS Immobilienverwaltung"></a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="navigation" type="button"><span class="menu-lines" aria-hidden="true"></span><span class="menu-label">Menü</span></button>
      <nav id="navigation" aria-label="Hauptnavigation">{links}<a class="button button-small" href="/kontakt.html" {'aria-current="page"' if key=='kontakt' else ''}>Kontakt aufnehmen</a></nav>
    </div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="container footer-top">
      <div class="footer-brand"><a href="/" aria-label="Zur Startseite"><img src="/assets/lapis-logo.png" alt="LAPIS Immobilienverwaltung" width="1331" height="373" loading="lazy"></a><p>Persönlich. Strukturiert. Verlässlich.</p></div>
      <div><h2>Entdecken</h2><a href="/leistungen.html">Leistungen</a><a href="/eigentuemer.html">Für Eigentümer</a><a href="/ueber-uns.html">Über uns</a><a href="/kontakt.html">Kontakt</a></div>
      <div><h2>In der Ostschweiz zu Hause.</h2><p>St. Gallen · Thurgau<br>Appenzell Ausserrhoden<br>Appenzell Innerrhoden</p></div>
    </div><div class="container footer-bottom"><span>© {CONFIG['year']} LAPIS Immobilienverwaltung</span><div><a href="/impressum.html">Impressum & Bildnachweise</a><a href="/datenschutz.html">Datenschutz</a></div></div>
    <div class="container draft-note">Privater Website-Entwurf · Unternehmens- und Kontaktangaben werden vor dem öffentlichen Start vervollständigt. Die gezeigten Liegenschaften sind illustrative Bilder und keine LAPIS-Referenzen.</div></footer>'''

def image(name, alt, cls='', eager=False):
    sizes = [640,1200] + ([1800] if name == 'hero' else [1600] if name == 'residential' else [])
    srcset = ', '.join(f'/assets/{name}-{s}.webp {s}w' for s in sizes)
    return f'<img class="{cls}" src="/assets/{name}-1200.webp" srcset="{srcset}" sizes="(max-width: 760px) 100vw, 50vw" width="1200" height="900" alt="{escape(alt)}" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'

for key,(title,description) in PAGES.items():
    content = (ROOT / 'src' / f'{key}.html').read_text()
    replacements = {
      '{{hero_image}}': image('residential','Mehrfamilienhaus mit Backsteinfassade und verglasten Balkonen',eager=key=='index'),
      '{{detail_image}}': image('facade','Helle Fassade mit geometrischen Fensterelementen in Ascona'),
      '{{interior_image}}': image('interior','Heller Wohn- und Essbereich mit natürlichem Tageslicht'),
      '{{existing_image}}': image('hero','Bestehende Wohnliegenschaft mit Balkonen in Montreux'),
    }
    for token,value in replacements.items(): content=content.replace(token,value)
    contact = {k: CONFIG[k] for k in ['email','phone','address','domain']}
    contact_json = json.dumps(contact,ensure_ascii=False).replace('<','\\u003c')
    html = f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | LAPIS Immobilienverwaltung</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#174EA6"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="icon" href="/assets/lapis-logo.png" type="image/png"><link rel="preload" href="/assets/dm-sans-400.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/styles.css"><script src="/assets/site.js" defer></script>
</head><body data-page="{key}">{header(key)}<main id="inhalt">{content}</main>{footer()}
<script id="site-contact" type="application/json">{contact_json}</script></body></html>'''
    (OUT / f'{key}.html').write_text(html)
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Robots-Tag: noindex, nofollow\n  Content-Security-Policy: default-src \'self\'; img-src \'self\' data:; font-src \'self\'; style-src \'self\'; script-src \'self\'; connect-src \'self\'; object-src \'none\'; base-uri \'self\'; form-action \'self\' mailto:; frame-ancestors \'self\'\n')
print(f'Built {len(PAGES)} pages in {OUT}')
