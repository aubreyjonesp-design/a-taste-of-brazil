#!/usr/bin/env python3
"""Build the static publishing hub with Python's standard library only."""
from pathlib import Path
from html import escape as e
from urllib.parse import urlparse
import json,re
from datetime import date
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text())
site=load('data/site.json'); retailers=load('data/retailers.json'); articles=load('data/articles.json'); coverage=load('data/coverage.json')
base=site['url']; root=urlparse(base).path
assert base.startswith('https://') and base.endswith('/')
def https(url):
 p=urlparse(url); assert p.scheme=='https' and p.netloc and not p.username and not p.password, 'Use a verified HTTPS URL'
ids=set()
for retailer in retailers:
 assert re.fullmatch('[a-z0-9-]+',retailer['id']) and retailer['id'] not in ids
 ids.add(retailer['id']);https(retailer['url']);assert retailer['verified_in'].strip()
assert 'google-play-books' in ids, 'Keep the existing Google Play Books route'
for social in site['social_links']:https(social['url'])
if site['contact_email']:assert re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',site['contact_email'])
slugs=set()
for item in articles:
 assert re.fullmatch('[a-z0-9-]+',item['slug']) and item['slug']!='index' and item['slug'] not in slugs
 slugs.add(item['slug'])
 if item.get('published'):
  assert item.get('approved_by') and item.get('sources') and item.get('sections')
  assert 'REPLACE WITH' not in json.dumps(item), 'Replace template text before publishing'
  for source in item['sources']:https(source['url'])
for item in coverage:
 if item.get('published'):
  https(item['url']);assert item.get('title') and item.get('type') and item.get('source_name') and item.get('date')
  date.fromisoformat(item['date']);assert 'REPLACE WITH' not in json.dumps(item), 'Replace template text before publishing'
  if item.get('quote'):assert item.get('reuse_permission'), 'Permission/source required for reusable quotations'
published=[x for x in articles if x.get('published')];mentions=[x for x in coverage if x.get('published')]
authors=' & '.join(site['authors'])
nav=[('index.html','Home'),('about-the-book.html','The book'),('authors.html','The authors'),('brazilian-food.html','Brazilian food'),('buy.html','Buy the book'),('press.html','Press & reviewers')]
if mentions:nav.append(('reviews.html','Reviews & press'))
pages=[]
def navigation(path,prefix=''):
 return '<nav class="hub-nav" aria-label="Main navigation">'+''.join(f'<a href="{prefix}{p}"'+(' aria-current="page"' if p==path else '')+f'>{e(label)}</a>' for p,label in nav)+'</nav>'
def footer(prefix=''):
 socials=''.join(f'<a href="{e(x["url"],quote=True)}">{e(x["name"])}</a>' for x in site['social_links'])
 return f'<footer>{e(site["title"])} · {e(authors)}<br>Purchase and reading options are provided by the linked retailer.<div class="hub-footer-links"><a href="{prefix}buy.html">Buy the book</a><a href="{prefix}press.html">Press &amp; reviewers</a><a href="{prefix}privacy.html">Privacy</a>{socials}</div></footer>'
def schema(path,title):
 url=base if path=='index.html' else base+path
 people=[{'@type':'Person','@id':base+f'#author-{i+1}','name':a} for i,a in enumerate(site['authors'])]
 book={'@type':'Book','@id':base+'#book','name':site['title'],'alternateName':site['title']+': '+site['subtitle'],'author':[{'@id':p['@id']} for p in people],'description':site['description'],'bookFormat':'https://schema.org/EBook','image':base+'assets/cover.jpg','url':base+'about-the-book.html'}
 graph=people+[book,{'@type':'WebSite','@id':base+'#website','name':site['title'],'url':base},{'@type':'WebPage','@id':url+'#webpage','name':title,'url':url,'isPartOf':{'@id':base+'#website'},'about':{'@id':base+'#book'}}]
 if path!='index.html':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':base},{'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':url}]})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
def metadata(path,title,description,prefix=''):
 url=base if path=='index.html' else base+path
 return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description,quote=True)}">
<link rel="canonical" href="{e(url,quote=True)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="A TASTE OF BRAZIL">
<meta property="og:title" content="{e(title,quote=True)}">
<meta property="og:description" content="{e(description,quote=True)}">
<meta property="og:url" content="{e(url,quote=True)}">
<meta property="og:image" content="{base}assets/cover.jpg">
<meta property="og:image:width" content="1056">
<meta property="og:image:height" content="1377">
<meta property="og:image:alt" content="A Taste of Brazil cover, featuring Brazilian dishes and Rio de Janeiro scenery">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title,quote=True)}">
<meta name="twitter:description" content="{e(description,quote=True)}">
<meta name="twitter:image" content="{base}assets/cover.jpg">
<meta name="twitter:image:alt" content="A Taste of Brazil book cover">
<link rel="stylesheet" href="{prefix}assets/hub.css">
<script src="{prefix}assets/hub.js" defer></script>
<script type="application/ld+json">{schema(path,title)}</script>'''
def retailer_buttons(placement='buy'):
 return ''.join(f'<div class="retailer"><h2>{e(r["name"])}</h2><p>{e(r["format"])} · See the current price, preview options and availability for your region on {e(r["name"])}.</p><a class="button" href="{e(r["url"],quote=True)}" data-retailer="{e(r["id"])}" data-placement="{placement}">Discover the book on {e(r["name"])} ↗</a></div>' for r in retailers)
cover='<img class="cover" src="assets/cover.jpg" alt="A Taste of Brazil cover, featuring Brazilian dishes and Rio de Janeiro scenery" width="1056" height="1377">'
def page(path,heading,description,body,eyebrow='A Taste of Brazil',prefix=''):
 title=heading+' | A Taste of Brazil'
 content=f'''<!doctype html>
<!-- Generated by tools/build.py -->
<html lang="en" data-site-root="{root}"><head>
{metadata(path,title,description,prefix)}
</head><body class="hub-page">
<a class="skip-link" href="#main-content">Skip to content</a>
<header><a href="{prefix}index.html">A TASTE OF BRAZIL</a><span>Brazilian family cooking</span></header>
{navigation(path,prefix)}
<main id="main-content" tabindex="-1"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="{prefix}index.html">Home</a> / <span aria-current="page">{e(heading)}</span></nav><div class="eyebrow">{e(eyebrow)}</div><h1>{e(heading)}</h1>{body}</main>
{footer(prefix)}
</body></html>
'''
 (R/path).parent.mkdir(parents=True,exist_ok=True);(R/path).write_text(content);pages.append(path)
# Rebuild from the untouched archive. The approved main section, CSS and all embedded images are retained.
home=(R/'A-Taste-of-Brazil-corrected-1.html').read_text()
home=re.sub(r'<!-- HANDOVER:.*?-->', '<!-- Approved homepage retained; supporting pages are built by tools/build.py. -->',home,flags=re.S)
home=home.replace('<html lang="en">',f'<html lang="en" data-site-root="{root}"><head>')
home=re.sub(r'<meta charset="utf-8">.*?(?=<style>)',metadata('index.html','A Taste of Brazil | '+authors,site['description'])+'\n',home,flags=re.S)
home=home.replace('</style>','</style></head><body>\n<a class="skip-link" href="#main-content">Skip to content</a>',1)
home=home.replace('</header>','</header>\n'+navigation('index.html'),1)
home=home.replace('<main>','<main id="main-content" tabindex="-1">',1)
google=next(x for x in retailers if x['id']=='google-play-books')
# The Google Play URL remains exactly the verified route, managed here from one config.
home=re.sub(r'href="https://play.google.com/store/books/details/Edneia_Silveira_A_Taste_of_Brazil\?id=nNATEgAAQBAJ"',f'href="{e(google["url"],quote=True)}" data-retailer="google-play-books" data-placement="home"',home)
home=re.sub(r'<footer>.*?</footer>',footer(),home,flags=re.S).replace('</html>','</body></html>')
(R/'index.html').write_text(home);pages.append('index.html')
page('about-the-book.html','About the book','Discover A Taste of Brazil: Authentic Family Recipes from the Heart of Brazil, by Edneia “Neia” Silveira and Philip Aubrey-Jones.',f'''<div class="split"><div><h2>A TASTE OF BRAZIL</h2><p class="subtitle">{e(site['subtitle'])}</p><p>By {e(authors)}</p><p>{e(site['description'])}</p><h2>A little Brazil at your table</h2><p>Explore Brazilian home cooking through <i>A Taste of Brazil</i>. Visit the book’s retailer listing to learn more and see the preview options available in your region.</p><p><a class="button" href="buy.html">Find the ebook</a></p><p><a href="authors.html">Meet the authors</a> · <a href="brazilian-food.html">A closer look at the cover</a></p></div>{cover}</div>''')
page('authors.html','About the authors','Meet the authors of A Taste of Brazil: Edneia “Neia” Silveira and Philip Aubrey-Jones.',f'''<p><i>A Taste of Brazil — {e(site['subtitle'])}</i> is by {e(authors)}.</p><section aria-labelledby="neia"><h2 id="neia">Edneia “Neia” Silveira</h2><p>Co-author of <i>A Taste of Brazil</i>.</p></section><section aria-labelledby="philip"><h2 id="philip">Philip Aubrey-Jones</h2><p>Co-author of <i>A Taste of Brazil</i>.</p></section><p><a class="button" href="about-the-book.html">Discover the book</a></p><p>For the book description, cover and publication resources, visit <a href="press.html">Press &amp; reviewers</a>.</p>''')
page('buy.html','Buy the book','Find A Taste of Brazil on Google Play Books. Follow the verified retailer link for regional availability, previews and current pricing.',f'''<p><i>A Taste of Brazil</i><br>{e(site['subtitle'])}<br>By {e(authors)}</p>{retailer_buttons()}<p>Purchase and reading options are provided by the retailer. Check its listing for availability in your region.</p>''',eyebrow='Bring Brazil to your table')
facts=f'''A TASTE OF BRAZIL
{site['subtitle']}
Authors: {authors}
Format confirmed on the approved website: Ebook

{site['description']}

Official website: {base}
Press and reviewer resources: {base}press.html
Purchase link: {google['url']}

This sheet includes only information confirmed in the project. Publication date, ISBN, publisher, pricing and media contact details are not supplied here.
'''
(R/'assets/book-facts.txt').write_text(facts)
contact=''
if site['contact_email']:contact=f'<h2>Media enquiries</h2><p><a href="mailto:{e(site["contact_email"],quote=True)}">{e(site["contact_email"])}</a></p>'
page('press.html','Press & reviewers','Factual book information, author names, the cover and the purchase link for reviewers, journalists, bloggers and food writers.',f'''<div class="split"><div><p>Book information and resources for reviewers, journalists, bloggers and food writers.</p><dl><dt>Title</dt><dd>A TASTE OF BRAZIL</dd><dt>Subtitle</dt><dd>{e(site['subtitle'])}</dd><dt>Authors</dt><dd>{e(authors)}</dd><dt>Format</dt><dd>Ebook</dd><dt>Official website</dt><dd><a href="{base}">{base}</a></dd></dl></div>{cover}</div><h2>Book description</h2><p>{e(site['description'])}</p><h2>Resources</h2><div class="resource-links"><a href="assets/book-facts.txt" download>Download the book facts (text)</a><a href="assets/cover.jpg" download>Download the book cover (JPEG)</a><a href="authors.html">Author information</a><a href="buy.html">Retailer information</a></div><p>The cover is the artwork already used on this website. This page does not grant additional reproduction rights.</p>{contact}{retailer_buttons('press')}''',eyebrow='Media resources')
article_links=''
if published:article_links='<h2>From the authors</h2><ul>'+''.join(f'<li><a href="articles/{e(x["slug"])}.html">{e(x["title"])}</a></li>' for x in published)+'</ul>'
page('brazilian-food.html','Brazilian food & the book','Explore the warmth and colour of Brazilian home cooking through A Taste of Brazil and the artwork already featured on its cover.',f'''<p>Authentic Brazilian family cooking is at the heart of <i>A Taste of Brazil</i>. Bring the warmth, colour and generosity of Brazilian home cooking to your table.</p><h2>Colour. Flavour. Brazil.</h2><p>A closer look at the book’s cover artwork.</p><div class="gallery"><figure><img src="assets/cover-food.jpg" alt="Detail of the cover artwork showing grilled meat, rice, salad and golden savoury snacks" width="1056" height="842" loading="lazy"><figcaption>A feast of colour — detail from the book’s cover artwork.</figcaption></figure><figure><img src="assets/cover-rio.png" alt="Detail of the back cover artwork showing Rio de Janeiro’s coastline and Sugarloaf Mountain" width="1489" height="1056" loading="lazy"><figcaption>A sense of place — adapted from the back cover artwork.</figcaption></figure></div>{article_links}<p><a href="about-the-book.html">Discover the book</a> or <a href="buy.html">visit its retailer listing for preview options</a>.</p>''')
page('privacy.html','Privacy & campaign links','How this static website handles campaign links and privacy, without cookies or visitor analytics collection.','''<p>This website does not use cookies, browser storage, advertising trackers or an analytics reporting service.</p><h2>Campaign links</h2><p>A link may contain a campaign label, such as <code>utm_source</code> or <code>utm_campaign</code>. These labels can travel with you between pages so that a publicity campaign can be distinguished. Please do not put personal information in campaign labels.</p><p>The website makes page and retailer-click event details available within the current browser page. It does not store or send those events to an analytics service. No visitor counts or sales are recorded by this feature.</p><h2>Hosting and retailers</h2><p>GitHub Pages hosts the website. GitHub handles hosting requests under its <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">privacy statement</a>. When you follow a purchase link, the retailer handles your visit and any purchase under its own policies.</p>''')
for a in published:
 body=f'<p>By {e(a["author"])}</p>'
 for section in a['sections']:
  body+=f'<h2>{e(section["heading"])}</h2>'+''.join(f'<p>{e(p)}</p>' for p in section['paragraphs'])
 body+='<h2>Sources</h2><ul>'+''.join(f'<li><a href="{e(x["url"],quote=True)}">{e(x["title"])}</a></li>' for x in a['sources'])+'</ul><p><a href="../brazilian-food.html">Explore Brazilian food &amp; the book</a></p>'
 page('articles/'+a['slug']+'.html',a['title'],a['description'],body,prefix='../')
if mentions:
 body=''
 for c in mentions:
  body+=f'<article><h2><a href="{e(c["url"],quote=True)}">{e(c["title"])}</a></h2><p>{e(c["type"])} · {e(c["source_name"])} · <time datetime="{e(c["date"])}">{e(c["date"])}</time></p>'
  if c.get('quote'):body+=f'<blockquote><p>{e(c["quote"])}</p></blockquote>'
  body+='</article>'
 page('reviews.html','Reviews & press','Genuine reviews and coverage of A Taste of Brazil, with links to their original sources.',body)
# Remove only generated entries that were unpublished; never remove authored input.
for f in (R/'articles').glob('*.html') if (R/'articles').exists() else []:
 if f.relative_to(R).as_posix() not in pages and '<!-- Generated by tools/build.py -->' in f.read_text():f.unlink()
if not mentions and (R/'reviews.html').exists() and '<!-- Generated by tools/build.py -->' in (R/'reviews.html').read_text():(R/'reviews.html').unlink()
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+e(base if p=='index.html' else base+p)+'</loc></url>\n' for p in pages)+'</urlset>\n')
(R/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+base+'sitemap.xml\n')
print(f'Built {len(pages)} public pages; {len(retailers)} verified retailer; {len(published)} articles; {len(mentions)} coverage items.')
