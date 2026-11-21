"""Check built navigation, images, headings and form accessibility without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import re

ROOT=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.ids=[]; self.links=[]; self.resources=[]; self.headings=[]; self.labels=set(); self.fields=[];self.errors=[];self.parse_text=text;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag in ['script','img'] and 'src' in a:self.resources.append(a['src'])
        if tag=='link' and a.get('rel') in ['stylesheet','preload','icon']:self.resources.append(a['href'])
        if tag=='img' and not a.get('alt'):self.errors.append('Image missing alternative text')
        if tag=='img' and 'srcset' in a:self.resources += [entry.strip().split(' ')[0] for entry in a['srcset'].split(',')]
        if re.fullmatch('h[1-6]',tag):self.headings.append(int(tag[1]))
        if tag=='label':self.labels.add(a.get('for'))
        if tag in ['input','textarea','select']:self.fields.append(a.get('id'))

pages={p.name:Page(p.read_text()) for p in ROOT.glob('*.html') if not p.name.startswith('__qa')}
errors=[]
for name,page in pages.items():
    errors += [f'{name}: {error}' for error in page.errors]
    assert page.headings.count(1)==1,(name,'Expected one h1')
    assert '{{' not in page.parse_text,(name,'Unexpanded placeholder')
    assert 'noindex' in page.parse_text,(name,'Draft index protection absent')
    assert '<html lang="de-CH">' in page.parse_text,(name,'Language absent')
    for ident,count in Counter(page.ids).items():
        if count>1:errors.append(f'{name}: duplicate id {ident}')
    for ident in page.fields:
        if ident not in page.labels:errors.append(f'{name}: missing label for {ident}')
    for url in page.links+page.resources:
        u=urlsplit(url)
        if u.scheme or u.netloc:
            if url in page.resources:errors.append(f'{name}: external render resource {url}')
            continue
        target=ROOT/(unquote(u.path).lstrip('/') or name)
        if u.path=='/':target=ROOT/'index.html'
        if not target.is_file():errors.append(f'{name}: missing {url}');continue
        if u.fragment and target.suffix=='.html':
            if u.fragment not in pages[target.name].ids:errors.append(f'{name}: missing anchor {url}')

css=(ROOT/'assets/styles.css').read_text()
for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css):
    if not url.startswith('data:') and not (ROOT/url.lstrip('/')).is_file():errors.append('Missing CSS resource '+url)
js=(ROOT/'assets/site.js').read_text()
for forbidden in ['fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'document.cookie']:
    assert forbidden not in js,('Unexpected data transmission/storage',forbidden)
assert not errors,'\n'.join(errors)
size=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file() and not p.name.startswith('__qa'))
print(f'PASS: {len(pages)} pages; local links and anchors; accessible form labels; local assets; no form transmission/storage. Total {size/1024:.0f} KiB.')
