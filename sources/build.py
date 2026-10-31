import os, re, shutil, json
S='/tmp/claude-0/-home-claude/ab87ead7-ae52-5b05-bd81-2057583e5e6e/scratchpad/'
HERE=os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
SITE='https://kafalisgroup.com'
body=open('src/app.html').read()
logo_svg=open('assets/logo-inline.svg').read()
# Le logo est dessiné une seule fois (symbole) puis réutilisé : pages plus légères
_vb=re.search(r'viewBox="([^"]+)"',logo_svg).group(1)
_inner=logo_svg[logo_svg.index('>')+1:logo_svg.rindex('</svg>')]
logo_symbol=f'<symbol id="logo" viewBox="{_vb}">{_inner}</symbol>'
_w,_h=_vb.split()[2:]
logo=f'<svg class="logo" role="img" aria-label="Kafalis Group" viewBox="0 0 {_w} {_h}"><use href="#logo" width="{_w}" height="{_h}"/></svg>'
CTA='''<section class="band deep cta">
    <svg class="bg" viewBox="0 0 100 100" aria-hidden="true"><use href="#k"/></svg>
    <div class="wrap">
      <h2>Vous préparez un lancement, un événement ou une campagne ?</h2>
      <p>Décrivez-nous votre besoin. Nous revenons vers vous avec une proposition et un devis détaillé en GNF.</p>
      <div class="btns"><a class="btn" href="#contact">Demander un devis</a><a class="btn line" href="mailto:contact@kafalisgroup.com">contact@kafalisgroup.com</a></div>
    </div>
  </section>'''
DELIVER='''<section class="band white">
    <div class="wrap">
      <div class="svc-head"><h2 class="h2">Ce que vous recevez</h2></div>
      <div class="deliver">
        <div><b>Un devis détaillé en GNF</b><span>Chaque poste expliqué, sans surprise. Toute variation vous est soumise.</span></div>
        <div><b>Un responsable dédié</b><span>Une seule personne à appeler, du lancement jusqu’à la fin de la mission.</span></div>
        <div><b>Un bilan complet</b><span>Photos, chiffres et retours du terrain, remis à la fin de chaque mission.</span></div>
      </div>
    </div>
  </section>'''
names={'activation':'Activation terrain','evenementiel':'Événementiel','impression':'Impression et supports'}
def nxt(cur):
    links=''.join(f'<a href="#{k}">{names[k]}</a>' for k in names if k!=cur)
    cards=f'<p>Nos autres métiers</p>{links}'
    return f'<section class="band"><div class="wrap"><div class="next">{cards}</div></div></section>\n  '+CTA
FILMS={
 'accueil':('Nos métiers en 12 secondes',[('On active.','Démonstrations, animations, points de vente'),('On organise.','Lancements, cérémonies, conférences'),('On imprime.','Bâches, kakemonos, flyers, goodies')]),
 'activation':('Une activation en 12 secondes',[('On briefe.','Animateurs formés à votre produit'),('On anime.','Démonstrations en points de vente et marchés'),('On mesure.','Photos, quantités, retours clients')]),
 'evenementiel':('Un événement en 12 secondes',[('On prépare.','Lieu, décor, son, écrans'),('On installe.','Montage, accueil, protocole'),('On reçoit.','Le jour J, tout est coordonné')]),
 'impression':('Une commande en 12 secondes',[('On conçoit.','Formats, papiers, finitions'),('On imprime.','Bon à tirer validé par vous'),('On livre.','Contrôlé, à la date convenue')]),
 'agence':('Kafalis en 12 secondes',[('On active.','Démonstrations, animations, points de vente'),('On organise.','Lancements, cérémonies, conférences'),('On imprime.','Bâches, kakemonos, flyers, goodies')]),
}
def film(k):
    title,words=FILMS[k]
    ws=''.join(f'<p class="f-word"><b>{w}</b><span>{t}</span></p>' for w,t in words)
    label='Animation : le k de Kafalis se construit et avance d’un pas, puis les mots '+', '.join(w.rstrip('.') for w,_ in words)+', et le logo Kafalis Group avec le slogan Donner vie aux idées, créer l’impact.'
    return f'''<section class="band film-band" aria-labelledby="film-{k}">
    <div class="wrap">
      <div class="svc-head"><h2 class="h2" id="film-{k}">{title}</h2></div>
      <div class="film" role="img" aria-label="{label}">
        <div class="f-k" aria-hidden="true"><svg viewBox="-6 -84 92 92"><path class="f-stem" d="M6.1 0V-72H17.1V0Z"/><path class="f-leg" d="M23.15 -22.56 L47.15 -48.00 L62.27 -48.00 L39.82 -24.20 L73.79 0 L54.83 0 Z"/><circle class="f-dot" cx="69.99" cy="-62.65" r="6.82"/></svg></div>
        <div class="f-words" aria-hidden="true">{ws}</div>
        <div class="f-end" aria-hidden="true">__LOGO__<p>Donner vie aux idées. <b>Créer l’impact.</b></p></div>
        <span class="f-bar" aria-hidden="true"></span>
        <button class="f-ctrl" type="button" aria-label="Mettre l’animation en pause"><svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg></button>
      </div>
    </div>
  </section>'''
for k in FILMS: body=body.replace(f'__FILM_{k}__',film(k))
assert '__FILM' not in body
assert body.count('<defs>')==1
body=body.replace('<defs>','<defs>\n    '+logo_symbol,1)
body=body.replace('__LOGO__',logo).replace('__CTA__',CTA).replace('__DELIVER__',DELIVER)
for k in names: body=body.replace(f'__NEXT_{k}__',nxt(k))
assert '__NEXT' not in body and '__CTA' not in body
font='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap">'
# Vrai site : police Outfit hébergée sur le site (sous-ensemble français, 300 à 600), préchargée, sans aller-retour vers Google
font_site='<link rel="preload" href="/fonts/outfit.woff2" as="font" type="font/woff2" crossorigin><style>@font-face{font-family:"Outfit";src:url("/fonts/outfit.woff2") format("woff2");font-weight:300 600;font-style:normal;font-display:swap}</style>'

import base64
def imgs(html, preview):
    for i in range(1,7):
        if preview:
            src='data:image/jpeg;base64,'+base64.b64encode(open(f'assets/realisations/maridor-{i}-apercu.jpg','rb').read()).decode()
        else:
            src=f'/img/realisations/maridor-{i}.jpg'
        html=html.replace(f'__IMG_{i}__',src)
    return html
# 1) Aperçu (une seule page, vues par #)
open(S+'kafalis-site.html','w').write('<title>Kafalis Group</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'+font+'\n'+imgs(body,True))
body=imgs(body,False)

# 2) Vrai site : une page par rubrique
PAGES={
 'accueil':     ('/', 'Kafalis Group | Agence d’activation, événementiel et impression à Conakry',
                 'Agence de communication de proximité en Guinée : activation terrain (BTL), démonstrations produit, événements et impression de supports à Conakry et partout en Guinée.'),
 'activation':  ('/activation-terrain/', 'Activation terrain et animation commerciale à Conakry | Kafalis Group',
                 'Démonstrations produit, essais, animations en points de vente et sur les marchés, animateurs et stands de marque : vos campagnes BTL en Guinée, avec rapport terrain.'),
 'evenementiel':('/evenementiel/', 'Organisation d’événements à Conakry, Guinée | Kafalis Group',
                 'Lancements de produits, conférences, cérémonies officielles et événements d’entreprise à Conakry : lieu, décoration, son, écrans, accueil et protocole pris en main.'),
 'impression':  ('/impression/', 'Impression de supports publicitaires à Conakry | Kafalis Group',
                 'Flyers, affiches, brochures, bâches, kakemonos, banderoles, signalétique et goodies personnalisés à Conakry. Conseil, bon à tirer, contrôle qualité et livraison.'),
 'agence':      ('/agence/', 'L’agence de communication de proximité en Guinée | Kafalis Group',
                 'Kafalis Group accompagne entreprises, institutions, ONG et porteurs de projets en Guinée : mission, valeurs et engagements de l’agence.'),
 'realisations':('/realisations/', 'Réalisations : activation, événementiel, photo et vidéo | Kafalis Group',
                 'Projets menés par Kafalis Group pour ses clients en Guinée, dont le shooting photo produit de MARIDOR, marque d’assaisonnements aux fruits de mer.'),
 'lacadence':   ('/la-cadence/', 'La Cadence, la lettre du marketing terrain et de l’événementiel en Guinée | Kafalis Group',
                 'Toutes les deux semaines, par e-mail ou sur WhatsApp : conseils, check-lists et décryptages sur l’activation de produits, l’événementiel, la décoration et l’audiovisuel en Guinée. Gratuit.'),
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
        label={'activation':'Activation terrain','evenementiel':'Événementiel','impression':'Impression et supports','agence':'L’agence','lacadence':'La Cadence','realisations':'Réalisations','contact':'Contact'}.get(k,'Page introuvable')
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
{font_site}
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
      <h1>Cette page n’existe pas</h1>
      <p class="lead">L’adresse a peut-être changé. Repartez de l’accueil, ou écrivez-nous directement.</p>
      <div class="btns" style="margin-top:8px"><a class="btn" href="/">Retour à l’accueil</a><a class="btn line" href="/contact/">Demander un devis</a></div>
    </div>
  </section>'''
PAGES['404']=('/404.html','Page introuvable | Kafalis Group','Cette page n’existe pas.')
open('dist/404.html','w').write(page('404', nf, 'noindex'))
del PAGES['404']
for f in ['favicon.svg','apple-touch-icon.png','og-image.png']: shutil.copy(f,'dist/'+f)
os.makedirs('dist/img/realisations',exist_ok=True)
for i in range(1,7): shutil.copy(f'assets/realisations/maridor-{i}.jpg',f'dist/img/realisations/maridor-{i}.jpg')
os.makedirs('dist/fonts',exist_ok=True); shutil.copy('assets/fonts/outfit.woff2','dist/fonts/outfit.woff2')
open('dist/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
urls=''.join(f'<url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="/" else "0.8"}</priority></url>' for p,_,_ in PAGES.values())
open('dist/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
# Cloudflare Pages : www et pages.dev -> adresse principale, cache
open('dist/_headers','w').write('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/*.png\n  Cache-Control: public, max-age=2592000\n/*.svg\n  Cache-Control: public, max-age=2592000\n/*.jpg\n  Cache-Control: public, max-age=2592000\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n  Access-Control-Allow-Origin: *\n\nhttps://kafalis-site.pages.dev/*\n  X-Robots-Tag: noindex\n\n/sources/*\n  X-Robots-Tag: noindex\n')
print('ok', sorted(os.listdir('dist')))
