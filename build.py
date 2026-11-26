"""Build the LAPIS static website. Python standard library only."""
from pathlib import Path
from html import escape
from hashlib import sha256
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
SITE = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
STYLE_VERSION = sha256((OUT / 'assets' / 'styles.css').read_bytes()).hexdigest()[:12]
PAGES = {
    'index': ('Immobilienverwaltung, die entlastet.', 'Persönliche Immobilienverwaltung für private Eigentümer von Mietliegenschaften in der Ostschweiz. Persönlich. Strukturiert. Verlässlich.')
}

def header(key):
    return f'''<a class="skip" href="#inhalt">Zum Inhalt</a>
    <header class="site-header"><div class="container header-inner">
      <a class="brand" href="/" aria-label="LAPIS Immobilienverwaltung – Startseite"><img src="/assets/lapis-logo.png" width="1331" height="373" alt="LAPIS Immobilienverwaltung"></a>
      <button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false"><span class="menu-label">Menü</span><span class="menu-lines" aria-hidden="true"></span></button>
      <nav id="navigation" aria-label="Hauptnavigation"><a href="#warum-lapis">Warum LAPIS</a><a href="#leistungen">Leistungen</a><a href="#zusammenarbeit">Zusammenarbeit</a><a class="button button-small" href="#kontakt">Kontakt aufnehmen</a></nav>
    </div></header>'''

def contact_details():
    email = str(SITE.get('email') or '').strip()
    phone = str(SITE.get('phone') or '').strip()
    if not email and not phone:
        return '<p>Geschäftliche Kontaktangaben folgen vor der Veröffentlichung.</p>'
    parts = []
    if email:
        safe_email = escape(email, quote=True)
        parts.append(f'<a href="mailto:{safe_email}">{escape(email)}</a>')
    if phone:
        safe_phone = escape(phone, quote=True)
        parts.append(f'<a href="tel:{safe_phone}">{escape(phone)}</a>')
    return ''.join(parts)

def footer():
    year = escape(str(SITE.get('year') or 2026))
    return f'''<footer class="site-footer"><div class="container footer-main-home">
      <div class="footer-identity"><a href="/" aria-label="LAPIS Immobilienverwaltung – Startseite"><img src="/assets/lapis-logo.png" width="1331" height="373" alt="LAPIS Immobilienverwaltung"></a><p>Persönlich. Strukturiert. Verlässlich.</p></div>
      <nav aria-label="Footernavigation"><a href="#warum-lapis">Warum LAPIS</a><a href="#leistungen">Leistungen</a><a href="#zusammenarbeit">Zusammenarbeit</a><a href="#kontakt">Kontakt</a></nav>
      <div class="footer-contact"><strong>Ostschweiz</strong><p>St. Gallen · Thurgau · Appenzell</p>{contact_details()}</div>
    </div><div class="container footer-bottom-home"><span>© {year} LAPIS Immobilienverwaltung</span><span>Impressum und Datenschutzhinweise: Angaben vor Veröffentlichung ergänzen.</span></div></footer>'''

def image(name, alt, cls='', eager=False):
    sizes = [640,1122] if name == 'entrance-v2' else [640,1200,1536] if name == 'architecture-v2' else [640,1200] + ([1800] if name == 'hero' else [1600] if name == 'residential' else [])
    srcset = ', '.join(f'/assets/{name}-{s}.webp {s}w' for s in sizes)
    dimensions = {
      'entrance-v2': (1122, 1402),
      'architecture-v2': (1536, 1024),
      'facade': (1200, 1690),
      'hero': (1800, 1200),
      'interior': (1200, 900),
      'residential': (1600, 1200),
    }
    width,height = dimensions.get(name, (1200,900))
    base = 1122 if name == 'entrance-v2' else 1200
    display_sizes = '(max-width: 680px) calc(100vw - 32px), (max-width: 900px) 55vw, 50vw' if eager else '(max-width: 760px) 100vw, 50vw'
    return f'<img class="{cls}" src="/assets/{name}-{base}.webp" srcset="{srcset}" sizes="{display_sizes}" width="{width}" height="{height}" alt="{escape(alt)}" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'

for key,(title,description) in PAGES.items():
    content = (ROOT / 'src' / f'{key}.html').read_text(encoding='utf-8')
    replacements = {
      '{{hero_image}}': image('architecture-v2','Mehrfamilienhaus mit hellen Fassaden und Balkonen'),
      '{{detail_image}}': image('entrance-v2','Heller Eingangsbereich mit Tageslicht'),
      '{{interior_image}}': image('interior','Wohnraum mit grossen Fenstern und natürlichem Licht'),
      '{{facade_image}}': image('facade','Architektonisches Fassadendetail mit regelmässiger Fensterstruktur'),
      '{{residential_image}}': image('residential','Wohnliegenschaft mit Balkonen und klarer Fassadengliederung'),
      '{{existing_image}}': image('architecture-v2','Wohnliegenschaft mit Balkonen und begrüntem Umfeld'),
      '{{architecture_hero}}': image('architecture-v2','Mehrfamilienhaus mit Balkonen und begrüntem Umfeld',eager=True),
      '{{architecture_tile}}': image('architecture-v2','Architekturvisualisierung eines Mehrfamilienhauses'),
      '{{entrance_tile}}': image('entrance-v2','Architekturvisualisierung eines hellen Eingangsbereichs'),
      '{{entrance_image}}': image('entrance-v2','Heller Hauseingang mit natürlichem Licht'),
      '{{about_image}}': image('hero','Architektonisches Fassadendetail einer Wohnliegenschaft'),
      '{{contact_details}}': contact_details(),
    }
    for token,value in replacements.items(): content=content.replace(token,value)
    contact_config = json.dumps({'email': SITE.get('email', '')}, ensure_ascii=False).replace('<', '\\u003c')
    html = f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | LAPIS Immobilienverwaltung</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#174EA6"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="icon" href="/assets/lapis-logo.png" type="image/png"><link rel="preload" href="/assets/dm-sans-400.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={STYLE_VERSION}"><script src="/assets/site.js" defer></script>
</head><body data-page="{key}">{header(key)}<main id="inhalt">{content}</main>{footer()}<script id="site-contact" type="application/json">{contact_config}</script></body></html>'''
    (OUT / f'{key}.html').write_text(html, encoding='utf-8')
(OUT / 'kontakt.html').write_text('''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><meta http-equiv="refresh" content="0; url=/#kontakt">
<title>Kontakt | LAPIS Immobilienverwaltung</title></head>
<body><main><h1>Kontakt</h1><p>Der Kontaktbereich befindet sich auf der <a href="/#kontakt">Startseite</a>.</p></main></body></html>''', encoding='utf-8')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Robots-Tag: noindex, nofollow\n  Content-Security-Policy: default-src \'self\'; img-src \'self\' data:; font-src \'self\'; style-src \'self\'; script-src \'self\'; connect-src \'self\'; object-src \'none\'; base-uri \'self\'; form-action \'self\' mailto:; frame-ancestors \'self\'\n')
print(f'Built {len(PAGES)} pages in {OUT}')
