import os, re, shutil, json
S='/tmp/claude-0/-home-claude/ab87ead7-ae52-5b05-bd81-2057583e5e6e/scratchpad/'
HERE=os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
SITE='https://kafalisgroup.com'
body=open('src/app.html').read()
logo=open('assets/logo-inline.svg').read()
arrow='<svg class="arr" width="18" height="18"><use href="#arrow"/></svg>'
CTA=f'''<section class="band deep cta">
    <svg class="bg" viewBox="0 0 100 100" aria-hidden="true"><use href="#k"/></svg>
    <div class="wrap">
      <p class="label">Votre prochain projet</p>
      <h2>Faisons avancer votre marque<span class="accent">.</span></h2>
      <div class="btns"><a class="btn" href="#contact">Demander un devis {arrow}</a><a class="btn line" href="mailto:contact@kafalisgroup.com">contact@kafalisgroup.com</a></div>
    </div>
  </section>'''
DELIVER='''<section class="band white">
    <div class="wrap">
      <div class="svc-head"><div class="stack"><p class="label">Ce que vous recevez</p><h2 class="h2">Clair avant, suivi pendant,<br>bilan après.</h2></div></div>
      <div class="deliver">
        <div><b>Un devis détaillé en GNF</b><span>Chaque poste expliqué, sans surprise. Toute variation vous est soumise.</span></div>
        <div><b>Un responsable dédié</b><span>Une seule personne à appeler, du lancement jusqu’à la fin de la mission.</span></div>
        <div><b>Un bilan complet</b><span>Photos, chiffres et retours du terrain, remis à la fin de chaque mission.</span></div>
      </div>
    </div>
  </section>'''
names={'activation':'Activation terrain','evenementiel':'Événementiel','impression':'Impression et supports'}
def nxt(cur):
    cards=''.join(f'<a href="#{k}"><span><small>Autre métier</small><b>{names[k]}</b></span>{arrow}</a>' for k in names if k!=cur)
    return f'<section class="band"><div class="wrap"><div class="next">{cards}</div></div></section>\n  '+CTA
body=body.replace('__LOGO__',logo).replace('__CTA__',CTA).replace('__DELIVER__',DELIVER)
for k in names: body=body.replace(f'__NEXT_{k}__',nxt(k))
assert '__NEXT' not in body and '__CTA' not in body
font='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap">'

# 1) Aperçu (une seule page, vues par #)
open(S+'kafalis-site.html','w').write('<title>Kafalis Group</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'+font+'\n'+body)

# 2) Vrai site : une page par rubrique
PAGES={
 'accueil':     ('/', 'Kafalis Group | Agence d’activation, événementiel et impression à Conakry',
                 'Agence de communication de proximité en Guinée : activation terrain (BTL), dégustations, événements et impression de supports à Conakry et partout en Guinée.'),
 'activation':  ('/activation-terrain/', 'Activation terrain et animation commerciale à Conakry | Kafalis Group',
                 'Dégustations, démonstrations, animations en points de vente et sur les marchés, animateurs et stands de marque : vos campagnes BTL en Guinée, avec rapport terrain.'),
 'evenementiel':('/evenementiel/', 'Organisation d’événements à Conakry, Guinée | Kafalis Group',
                 'Lancements de produits, conférences, cérémonies officielles et événements d’entreprise à Conakry : lieu, décoration, son, écrans, accueil et protocole pris en main.'),
 'impression':  ('/impression/', 'Impression de supports publicitaires à Conakry | Kafalis Group',
                 'Flyers, affiches, brochures, bâches, kakemonos, banderoles, signalétique et goodies personnalisés à Conakry. Conseil, bon à tirer, contrôle qualité et livraison.'),
 'agence':      ('/agence/', 'L’agence de communication de proximité en Guinée | Kafalis Group',
                 'Kafalis Group accompagne entreprises, institutions, ONG et porteurs de projets en Guinée : mission, valeurs et engagements de l’agence.'),
 'contact':     ('/contact/', 'Contact et demande de devis | Kafalis Group, Conakry',
                 'Décrivez votre projet d’activation, d’événement ou d’impression : Kafalis Group vous répond avec une proposition et un devis détaillé en GNF.'),
}
head_end=body.index('<main>'); main_end=body.index('</main>')
pre=body[:head_end]; post=body[main_end:]
main=body[head_end+len('<main>'):main_end]
views=dict(re.findall(r'<div class="view" data-view="(\w+)">(.*?)\n</div>\n(?=\n*(?:<!--|$))', main, re.S))
assert set(views)==set(PAGES), views.keys()

def links(html):
    for k,(path,_,_) in PAGES.items():
        html=html.replace(f'href="#{k}"', f'href="{path}"')
    html=re.sub(r'href="/contact/" data-need="([^"]+)"', lambda m: 'href="/contact/?besoin='+m.group(1).replace(' ','+')+'"', html)
    return html

org={"@type":"Organization","@id":SITE+"/#org","name":"Kafalis Group","url":SITE+"/","logo":SITE+"/apple-touch-icon.png","image":SITE+"/og-image.png",
     "email":"contact@kafalisgroup.com","description":"Agence de communication de proximité en Guinée : activation terrain, événementiel et impression.",
     "address":{"@type":"PostalAddress","addressLocality":"Conakry","addressCountry":"GN"},
     "areaServed":{"@type":"Country","name":"Guinée"},
     "knowsAbout":["Activation de marque","Marketing terrain","BTL","Événementiel","Impression publicitaire"]}
def jsonld(k):
    path,title,desc=PAGES[k]
    g=[org,{"@type":"WebSite","@id":SITE+"/#site","url":SITE+"/","name":"Kafalis Group","inLanguage":"fr","publisher":{"@id":SITE+"/#org"}},
       {"@type":"WebPage","url":SITE+path,"name":title,"description":desc,"inLanguage":"fr","isPartOf":{"@id":SITE+"/#site"}}]
    if k!='accueil':
        label={'activation':'Activation terrain','evenementiel':'Événementiel','impression':'Impression et supports','agence':'L’agence','contact':'Contact'}.get(k,'Page introuvable')
        g.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":SITE+"/"},{"@type":"ListItem","position":2,"name":label,"item":SITE+path}]})
    if k in names:
        g.append({"@type":"Service","name":names[k],"serviceType":names[k],"provider":{"@id":SITE+"/#org"},"areaServed":{"@type":"Country","name":"Guinée"},"url":SITE+path,"description":desc})
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":g},ensure_ascii=False)+'</script>'

def head(k, robots='index,follow'):
    path,title,desc=PAGES[k]
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#0B1A33">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kafalis Group">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
{font}
{jsonld(k)}
<style>[hidden]{{display:none!important}}</style>
</head>
<body>
'''
def page(k, inner, robots='index,follow'):
    path=PAGES[k][0]
    p=links(pre)
    # Menu : page en cours
    p=p.replace(f'<a href="{path}">', f'<a href="{path}" aria-current="page">',1) if k!='accueil' else p
    return head(k,robots)+p+'<main>\n<div class="view on" data-view="'+k+'">'+links(inner)+'\n</div>\n'+links(post)+'\n</body>\n</html>\n'

shutil.rmtree('dist',ignore_errors=True); os.makedirs('dist')
for k,(path,_,_) in PAGES.items():
    d='dist'+path; os.makedirs(d,exist_ok=True)
    open(d+'index.html','w').write(page(k, views[k]))
# 404
nf='''
  <section class="page-hero deep" style="min-height:60vh">
    <div class="wrap">
      <p class="crumb"><a href="/">Accueil</a><span>/</span><span>Page introuvable</span></p>
      <h1>Page<br>introuvable<span class="accent">.</span></h1>
      <p class="lead">Cette adresse n’existe pas ou plus. Repartez de l’accueil ou parlez-nous directement de votre projet.</p>
      <div class="btns" style="margin-top:8px"><a class="btn" href="/">Retour à l’accueil</a><a class="btn line" href="/contact/">Demander un devis</a></div>
    </div>
  </section>'''
PAGES['404']=('/404.html','Page introuvable | Kafalis Group','Cette page n’existe pas.')
open('dist/404.html','w').write(page('404', nf, 'noindex'))
del PAGES['404']
for f in ['favicon.svg','apple-touch-icon.png','og-image.png']: shutil.copy(f,'dist/'+f)
open('dist/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
urls=''.join(f'<url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="/" else "0.8"}</priority></url>' for p,_,_ in PAGES.values())
open('dist/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
# Cloudflare Pages : www et pages.dev -> adresse principale, cache
open('dist/_headers','w').write('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/*.png\n  Cache-Control: public, max-age=2592000\n/*.svg\n  Cache-Control: public, max-age=2592000\n\nhttps://kafalis-site.pages.dev/*\n  X-Robots-Tag: noindex\n\n/sources/*\n  X-Robots-Tag: noindex\n')
print('ok', sorted(os.listdir('dist')))
