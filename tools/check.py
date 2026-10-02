#!/usr/bin/env python3
"""Dependency-free structural and preservation checks for generated pages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import base64,hashlib,json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];site=json.loads((R/'data/site.json').read_text());base=site['url']
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.tags=[];self.links=[];self.assets=[];self.ids=set();self.meta={};self.schema=[];self.ld=False;self.data='';self.stack=[];self.feed(text);self.close()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append(tag)
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(tag)
  if 'id' in a:assert a['id'] not in self.ids;self.ids.add(a['id'])
  if tag=='a':self.links.append(a['href'])
  if tag=='img':assert a.get('alt');self.assets.append(a['src'])
  if tag=='script' and a.get('src'):self.assets.append(a['src'])
  if tag=='link':
   if a.get('rel')=='canonical':self.meta['canonical']=a['href']
   if a.get('rel')=='stylesheet':self.assets.append(a['href'])
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='script' and a.get('type')=='application/ld+json':self.ld=True;self.data=''
 def handle_data(self,data):
  if self.ld:self.data+=data
 def handle_endtag(self,tag):
  assert self.stack and self.stack.pop()==tag, ('Unbalanced HTML tag',tag)
  if tag=='script' and self.ld:self.schema.append(json.loads(self.data));self.ld=False
pages={p:Page(p.read_text()) for p in R.glob('*.html') if p.name!='A-Taste-of-Brazil-corrected-1.html'}
pages.update({p:Page(p.read_text()) for p in (R/'articles').glob('*.html')} if (R/'articles').exists() else {})
links=0;assets=0
for p,page in pages.items():
 rel=p.relative_to(R).as_posix();text=p.read_text();assert not page.stack,(rel,page.stack)
 for tag in ['html','head','body','main','h1','title']:assert page.tags.count(tag)==1,(rel,tag)
 for key in ['description','og:title','og:description','og:url','og:image','og:image:alt','twitter:card']:assert page.meta.get(key),(rel,key)
 assert page.meta['canonical']==(base if rel=='index.html' else base+rel)
 assert len(page.schema)==1
 graph=page.schema[0]['@graph'];types={x['@type'] for x in graph}
 assert {'Book','Person','WebSite','WebPage'}<=types
 if rel!='index.html':assert 'BreadcrumbList' in types
 assert [x['name'] for x in graph if x['@type']=='Person']==site['authors']
 assert 'REPLACE WITH' not in text and 'TODO' not in text and 'lorem ipsum' not in text.lower()
 for x in page.links+page.assets:
  if x.startswith('data:'):
   base64.b64decode(x.split(',',1)[1],validate=True);assets+=1;continue
  u=urlparse(x)
  if u.scheme in ['https','mailto']:continue
  assert not u.scheme and not u.netloc,(rel,x)
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target/= 'index.html'
  assert target.is_relative_to(R) and target.exists(),(rel,x)
  if u.fragment and target in pages:assert u.fragment in pages[target].ids,(rel,x)
  if x in page.assets:assets+=1
  else:links+=1
original=(R/'A-Taste-of-Brazil-corrected-1.html').read_bytes()
assert hashlib.sha1(f'blob {len(original)}\0'.encode()+original).hexdigest()=='90aa25c42d7f7ec495950992d0afb2103d991c17'
old=original.decode();new=(R/'index.html').read_text()
assert re.search(r'<style>.*?</style>',old,re.S).group()==re.search(r'<style>.*?</style>',new,re.S).group()
def main(s):
 s=re.search(r'<main[^>]*>(.*?)</main>',s,re.S).group(1)
 return re.sub(r'<a class="button"[^>]*>', '<a class="button">',s)
assert main(old)==main(new), 'Approved main content changed'
images=lambda s:re.findall(r'data:(image/[^;]+);base64,([A-Za-z0-9+/=]+)',s)
assert images(old)==images(new)
for path,(_,data) in zip(['assets/cover.jpg','assets/cover-food.jpg','assets/cover-rio.png'],images(old)):assert (R/path).read_bytes()==base64.b64decode(data)
google='https://play.google.com/store/books/details/Edneia_Silveira_A_Taste_of_Brazil?id=nNATEgAAQBAJ'
retailers=json.loads((R/'data/retailers.json').read_text());assert next(r for r in retailers if r['id']=='google-play-books')['url']==google
assert pages[R/'index.html'].links.count(google)==2
for name in ['buy.html','press.html']:assert google in pages[R/name].links
published=[x for x in json.loads((R/'data/articles.json').read_text()) if x.get('published')]
mentions=[x for x in json.loads((R/'data/coverage.json').read_text()) if x.get('published')]
assert (R/'reviews.html').exists()==bool(mentions)
assert {(R/'articles'/f'{x["slug"]}.html') for x in published}=={x for x in pages if x.parent.name=='articles'}
sm=ET.parse(R/'sitemap.xml');urls=[x.text for x in sm.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert set(urls)=={x.meta['canonical'] for x in pages.values()}
assert 'Sitemap: '+base+'sitemap.xml' in (R/'robots.txt').read_text()
print(f'PASS: {len(pages)} pages, {links} internal links, {assets} local/embedded assets, metadata, JSON-LD, sitemap, robots, original CSS/main/images, exact artwork bytes and preserved Google Play routes.')
