import os, shutil
S='/tmp/claude-0/-home-claude/ab87ead7-ae52-5b05-bd81-2057583e5e6e/scratchpad/'
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
    others=[k for k in names if k!=cur]
    cards=''.join(f'<a href="#{k}"><span><small>Autre métier</small><b>{names[k]}</b></span>{arrow}</a>' for k in others)
    return f'<section class="band"><div class="wrap"><div class="next">{cards}</div></div></section>\n  '+CTA
body=body.replace('__LOGO__',logo).replace('__CTA__',CTA).replace('__DELIVER__',DELIVER)
for k in names: body=body.replace(f'__NEXT_{k}__',nxt(k))
assert '__' not in body.replace('__proto__','') or print([l for l in body.splitlines() if '__' in l][:3])
font='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap">'
open(S+'kafalis-site.html','w').write('<title>Kafalis Group</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'+font+'\n'+body)
desc="Kafalis Group, agence guinéenne de communication de proximité : activation terrain, événementiel, impression et supports. Conakry et toute la Guinée."
head=f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Kafalis Group</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1A33">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="https://kafalisgroup.com/">
<meta property="og:type" content="website">
<meta property="og:title" content="Kafalis Group">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://kafalisgroup.com/">
<meta property="og:image" content="https://kafalisgroup.com/og-image.png">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
{font}
<style>[hidden]{{display:none!important}}</style>
</head>
<body>
'''
shutil.rmtree('dist',ignore_errors=True); os.makedirs('dist')
open('dist/index.html','w').write(head+body+'\n</body>\n</html>\n')
for f in ['favicon.svg','apple-touch-icon.png','og-image.png']: shutil.copy(f,'dist/'+f)
open('dist/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://kafalisgroup.com/sitemap.xml\n')
open('dist/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://kafalisgroup.com/</loc></url></urlset>\n')
