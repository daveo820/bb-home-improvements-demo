# Static page builder for the B&B Home Improvements concept. Run: python3 build.py
import json
BASE = 'https://bb-home-improvements-demo.vercel.app/'  # Vercel production URL
TEL, TEL_H = '+19103367516', '(910) 336&#8209;7516'
EXA = 'https://exa.ai/library/place/ttt0sdt195x'
CR = 'https://www.contractorsranked.com/contractor/Fayetteville-NC/b-b-home-improvements'
ORG = {"@context":"https://schema.org","@type":"GeneralContractor","name":"B&B Home Improvements",
 "url":BASE,"telephone":"+1-910-336-7516",
 "founder":{"@type":"Person","name":"Bobby Wilburn"},
 "address":{"@type":"PostalAddress","addressLocality":"Fayetteville","addressRegion":"NC","postalCode":"28311","addressCountry":"US"},
 "geo":{"@type":"GeoCoordinates","latitude":35.151489,"longitude":-78.864491},
 "openingHours":"Mo-Sa 07:00-19:00","areaServed":"Fayetteville, NC",
 "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"58"}}
FONTS = 'https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,400;0,500;0,700;1,400&family=Rokkitt:wght@500;700;800&display=swap'

def K(t, cls=''): return f'<p class="kicker {cls}"><span class="tick" aria-hidden="true"></span>{t}</p>'
# signature: the tape. A tape measure blade with inch ticks; it pulls out when it comes into view
def TAPE(label='', cls=''):
    marks = ''.join(f'<span class="in"><b>{i}</b></span>' for i in range(1,25))
    return f'<div class="tape {cls}" aria-hidden="true"><div class="blade">{marks}</div>' + (f'<span class="tape-label">{label}</span>' if label else '') + '</div>'

HEAD = '''<!doctype html><html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="B&amp;B Home Improvements (concept)"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}"><meta property="og:image" content="{base}og.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{base}og.png">
<meta name="robots" content="noindex, nofollow"><!-- concept demo, not for indexing -->
<meta name="theme-color" content="#f2e6cf">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{fonts}"><link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="{fonts}"></noscript>
<link rel="stylesheet" href="css/design-system.css"><link rel="stylesheet" href="css/components.css"><link rel="stylesheet" href="css/pages.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%23a3201c'/%3E%3Ctext x='16' y='22' font-family='Georgia' font-weight='700' font-size='13' fill='%23fff' text-anchor='middle'%3EB%26amp;B%3C/text%3E%3C/svg%3E">
<script>document.documentElement.classList.replace('no-js','js-ready')</script><script type="application/ld+json">{ld}</script></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="demo-bar">Concept by <a href="https://luminarch.pro">LuminArch</a>. Not an official B&amp;B Home Improvements site; B&amp;B has no website today. Reviews are real and sourced; placeholders are labeled.</div>
<header class="top"><div class="wrap nav"><a class="mark" href="index.html"><span class="mk-b" aria-hidden="true">B<i>&amp;</i>B</span><span><b>B&amp;B Home Improvements</b><small>No job too big or small &middot; Fayetteville</small></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="menu">Menu</button><ul id="menu">{nav}</ul><a class="btn btn--red btn--call" href="tel:{tel}"><span class="cl-full">{telh}</span><span class="cl-short">Call Bobby</span></a></div></header><main id="main">'''

FOOT = f'''</main><footer class="site-foot">{TAPE('','tape--foot')}<div class="wrap">
<div class="sign">
 <p class="sign-k">Got a list of projects?</p>
 <p class="sign-h">Call Bobby.</p>
 <a class="sign-num" href="tel:{TEL}">{TEL_H}</a>
 <p class="sign-sub">Monday to Saturday, 7am to 7pm &middot; Fayetteville, NC 28311</p>
</div>
<div class="foot-grid">
 <p class="foot-quote">&ldquo;I call him an &lsquo;old school&rsquo; contractor.&rdquo;<span>Google review, December 2023</span></p>
 <nav aria-label="Footer"><a href="services.html">The work</a><a href="reviews.html">Reviews</a><a href="about.html">About Bobby</a><a href="contact.html">Free estimate</a></nav>
</div>
<div class="foot-row"><span>B&amp;B Home Improvements &middot; Fayetteville, North Carolina</span><span>Concept by <a href="https://luminarch.pro">LuminArch</a></span></div></div></footer>
<script src="js/main.js"></script></body></html>'''

NAV = [('services.html','The work'),('reviews.html','Reviews'),('about.html','About Bobby'),('contact.html','Free estimate')]
def bc(*n): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":a,"item":BASE+b} for i,(a,b) in enumerate(n)]}
def page(fn, t, d, body, ld=None):
    assert 50 <= len(t) <= 60, (fn, len(t), t)
    assert 140 <= len(d) <= 160, (fn, len(d), d)
    nav = ''.join(f'<li><a href="{h}"' + (' aria-current="page"' if h == fn else '') + f'>{n}</a></li>' for h, n in NAV)
    url = BASE + ('' if fn == 'index.html' else fn)
    open(fn,'w').write(HEAD.format(t=t,d=d,url=url,base=BASE,nav=nav,ld=json.dumps(ld or [ORG]),fonts=FONTS,tel=TEL,telh=TEL_H) + body + FOOT)

# Google reviews, word for word, from the Exa place page (Google listing data, checked 8 Oct 2026). "..." = cut short at the source. All 5 out of 5.
REV = [
 ('2026-02-13','Feb 2026','We are so pleased with our new bath remodel. Everything looks wonderful, from the tile install, paint, fixtures to the cleanup. Bobby and his team go above and beyond to make sure the construction is perfect. We hope to hire them for other home improvements. If you are looking for a great team that is a pleasure to work with, contact B and B Home Improvements!','Bath remodel'),
 ('2025-12-24','Dec 2025','I had the best experience with this company and the owner. We needed a rim joist replacement in order to finish repairing the rest of our home and he came out faster than any other company and fixed it within a few days. I&rsquo;m so glad that my husband found this company because it was extremely affordable! I&rsquo;ll definitely be looking forward to hiring them again for any future repairs.','Rim joist replacement'),
 ('2025-11-23','Nov 2025','Bobby saved the day! Recently, an unscrupulous, unknown driver mowed down our mailbox and left the scene. Because it&rsquo;s a lamp post mailbox repairing it was beyond our scope. After calling 5 different handymen I was becoming frustrated with the no shows, outrageous quotes, and getting the run around. It wasn&rsquo;t until my 6th call did I find a company willing to put us right, and that was B&amp;B Home Improvements. Bobby communicated well throughout the entire process, was on time, friendly, trustworthy, reasonably priced, and performed the work to my satisfaction. I will keep him in my contacts for...','Lamp post mailbox'),
 ('2025-08-22','Aug 2025','Bobby and his crew did an amazing job on my bathroom remodel. They were great at communicating with us and very professional. I recommend him to anyone who needs work done. We will be calling him for all of our future renovations. Bobby responded quickly when we called and gave us a quote within days. He quickly started our remodel and even finished earlier than expected. Which is always a plus. He has high standards and he makes sure things are done correctly.','Bathroom remodel'),
 ('2025-03-14','Mar 2025','Bobby Wilburn is an amazing contractor, highly skilled, great outcomes, reasonably priced and, most importantly, responsive and reliable. He renovated three bathrooms beautifully, installed light fixtures, replaced windows and more. Thankfully, we have both a fantastic contractor with very high standards and a commitment to excellence, and a long list of projects. I highly recommend B&amp;B, you cannot find better!','Three bathrooms, windows, lighting'),
 ('2024-11-23','Nov 2024','10 Stars!!!Where do I begin!! Bobby is a wonderful, personable, honest, and trustworthy professional! His expertise is unmatched! This project was one I waited to do as my ability to lift and carry laundry was not going too well. I did not want to go through the &ldquo;seasonal laundry&rdquo; debacle so I googled contractors and B&amp;B Home Improvements was my last and final quote! He was able to hone all of my wants into the plan the same day!! He will be the only Contractor I will ever recommend! I am so happy with my new laundry storage room! It is so beautiful and perfectly complements the rest of my...','Laundry storage room'),
 ('2023-12-30','Dec 2023','Awesome job completed by Bob and his team. The week before Christmas he did a remodel on my mother&rsquo;s bathroom. He was very professional and always kept us updated on his progress. I call him an &ldquo;old school&rdquo; contractor. There is just about nothing he hasn&rsquo;t seen or dealt with in all his 30-something years of working in his profession. I highly recommend his services for just about any home improvement issue you may have.','Bathroom remodel'),
 ('2022-05-11','May 2022','Bobby is my go to for all construction needs! I had a house fire and I talked to lots of contractors before I found Bobby and his team. He went above and beyond all expectations to get the house better than what it was originally. He is the go to contractor on all my home repair and improvements on my properties. I typically like to do my own work but Bobby is more efficient and quality driven and makes it easy for me to have him get them finished. He rebuilt a bonus addition on the house that was improperly constructed before and now the room is a great addition that is utilized for Man...','House fire rebuild, bonus room'),
]
# NB: reviewer typed "contractor- highly skilled" and "excellence - and"; dashes replaced with commas for house style. "30-something" kept as written in the quote.
def rcard(r, cls=''):
    iso,d,txt,job = r
    return (f'<figure class="rcard rv {cls}"><div class="rc-top"><span class="rc-job">{job}</span><span class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div>'
            f'<blockquote><p>{txt}</p></blockquote><figcaption>Google review &middot; <time datetime="{iso}">{d}</time></figcaption></figure>')

JOBS = [('Jun 2026','Complete kitchen remodel, &ldquo;from the joist to the ceiling&rdquo;','Bobby&rsquo;s Google post'),
 ('Feb 2026','Bath remodel: tile, paint, fixtures, cleanup','Google review'),
 ('Dec 2025','Rim joist replaced within a few days','Google review'),
 ('Nov 2025','Lamp post mailbox rebuilt after a hit and run','Google review'),
 ('Mar 2025','Three bathrooms, light fixtures, windows','Google review'),
 ('Nov 2024','Laundry room turned storage room','Google review'),
 ('May 2022','House fire rebuild and a bonus room redone','Google review')]

# ---------- HOME ----------
page('index.html','B&B Home Improvements | Remodeling Contractor, Fayetteville',
 'Bobby Wilburn and the B&B Home Improvements crew remodel kitchens and bathrooms and replace windows and decks in Fayetteville. 4.9 on Google. Call today.', f'''
<section class="hero"><div class="wrap hero-grid">
 <div class="hero-copy">{K('Remodeling and repairs &middot; Fayetteville, NC')}
  <h1>Kitchens, bathrooms, windows, decks. <em>And the job nobody else would take.</em></h1>
  <p class="lede">B&amp;B Home Improvements is Bobby Wilburn and his crew. A customer put it simply: &ldquo;There is just about nothing he hasn&rsquo;t seen or dealt with in all his 30&#8209;something years.&rdquo;</p>
  <div class="cta"><a class="btn btn--red" href="tel:{TEL}">Call Bobby {TEL_H}</a><a class="btn btn--line" href="contact.html">Free estimate</a></div>
  <div class="score"><span class="score-n" data-count="4.9" data-dec="1">4.9</span><span class="score-t"><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>58 Google reviews<br>Mon to Sat, 7am to 7pm</span></div>
 </div>
 <aside class="clip" aria-labelledby="clip-h"><p id="clip-h" class="clip-h">Recent jobs, per customers</p>
  <ol class="clip-list">{''.join(f'<li><time>{d}</time><b>{w}</b><span>{s}</span></li>' for d,w,s in JOBS[:5])}</ol>
  <a class="clip-more" href="services.html">All the work &rarr;</a>
 </aside>
</div>{TAPE('','tape--hero')}</section>

<section class="sixth wrap" aria-labelledby="sx-h">
 <div class="sx-num rv" aria-hidden="true">6<sup>th</sup></div>
 <div class="sx-copy rv">{K('Why people call')}<h2 id="sx-h">&ldquo;It wasn&rsquo;t until my 6th call did I find a company willing to put us right.&rdquo;</h2>
 <p>Five handymen didn&rsquo;t show, quoted too high or gave the run around on a lamp post mailbox. Bobby came, on time, and fixed it. That review is from November 2025, and it sounds a lot like the others: he calls back, he shows up, he finishes.</p></div>
</section>

<section class="rooms" aria-labelledby="rm-h"><div class="wrap">
 <div class="rooms-head rv">{K('The work')}<h2 id="rm-h">Room by room.</h2></div>
 <div class="rooms-grid">
  <a class="room room--bath rv" href="services.html#baths"><span class="room-k">Bathrooms</span><b>The most common job in the reviews.</b><span class="room-s">Four of the eight reviews here are bathroom remodels, including three in one house.</span></a>
  <a class="room room--kitchen rv" href="services.html#kitchens"><span class="room-k">Kitchens</span><b>From the joist to the ceiling.</b><span class="room-s">Bobby&rsquo;s own words on a June 2026 kitchen.</span></a>
  <a class="room room--windows rv" href="services.html#windows"><span class="room-k">Windows and siding</span><b>Replaced, trimmed, sealed.</b></a>
  <a class="room room--decks rv" href="services.html#decks"><span class="room-k">Decks and patios</span><b>Built and rebuilt.</b></a>
  <a class="room room--fix rv" href="services.html#repairs"><span class="room-k">Repairs</span><b>Rim joists, rot, damage, odd jobs.</b></a>
 </div>
 <p class="note rv"><span class="ph">Placeholder</span> before and after photos for each room. Bobbybefore and after photos for each room. Bobby already posts project photos to his Google profile; those would go here.rsquo;s June 2026 Google post already has a kitchen photo; more like it would go here.</p>
</div></section>

<section class="voices wrap" aria-labelledby="vo-h">
 <div class="voices-head rv">{K('What customers say')}<h2 id="vo-h">58 reviews. 4.9 stars. Here are three.</h2></div>
 <div class="voices-grid">{rcard(REV[4],'rcard--lead')}{rcard(REV[1])}{rcard(REV[3])}</div>
 <a class="btn btn--line rv" href="reviews.html">Read all eight</a>
</section>

<section class="ledger wrap rv" aria-labelledby="lg-h">
 {K('How it goes')}<h2 id="lg-h">Call, quote, start, finish early if he can.</h2>
 <ol class="ledger-list">
  <li><b>You call.</b><span>&ldquo;Bobby responded quickly when we called.&rdquo;</span></li>
  <li><b>He comes out.</b><span>&ldquo;He came out faster than any other company.&rdquo;</span></li>
  <li><b>A quote within days.</b><span>&ldquo;Gave us a quote within days.&rdquo;</span></li>
  <li><b>Updates as it goes.</b><span>&ldquo;Always kept us updated on his progress.&rdquo;</span></li>
  <li><b>Done.</b><span>&ldquo;Even finished earlier than expected.&rdquo;</span></li>
 </ol>
 <p class="fine">Every step is a line from a Google review, not a promise.</p>
</section>
''', ld=[ORG, bc(('Home',''))])

# ---------- SERVICES ----------
SV = [('baths','Bathroom remodels','Tile, paint, fixtures and the cleanup after. One customer had three bathrooms renovated; another had her mother&rsquo;s bathroom done the week before Christmas.',REV[0]),
 ('kitchens','Kitchen remodels','Bobby posted a complete kitchen remodel to his Google profile in June 2026, &ldquo;from the joist to the ceiling.&rdquo;',None),
 ('windows','Windows and siding','Window replacement shows up in the reviews alongside lighting and bath work. Siding is listed on his ContractorsRanked profile.',None),
 ('decks','Decks and patios','Listed on his ContractorsRanked profile.',None),
 ('repairs','Structural repairs and rebuilds','Rim joist replacement, a house fire rebuild, a badly built bonus room redone properly, a lamp post mailbox. The jobs other people turn down.',REV[7]),
 ('small','Small jobs and odd jobs','Light fixtures, a laundry room turned into storage, &ldquo;just about any home improvement issue.&rdquo; No job too big or small is the line on his logo.',REV[5])]
def sv(i,s):
    k,n,d,r = s
    quote = f'<blockquote class="sv-q"><p>{r[2][:220].rsplit(" ",1)[0]}...</p><footer>Google review, {r[1]}</footer></blockquote>' if r else '<p class="note"><span class="ph">Placeholder</span> two project photos and a sentence from Bobby.</p>'
    return f'<article id="{k}" class="sv rv"><span class="sv-n">{i+1:02d}</span><div class="sv-body"><h2>{n}</h2><p>{d}</p></div>{quote}</article>'
page('services.html','Remodeling Services, Fayetteville NC | B&B Home Improvements',
 'Bathroom and kitchen remodels, windows, siding, decks, structural repairs and odd jobs from Bobby Wilburn and B&B Home Improvements. Call (910) 336-7516.', f'''
<section class="page-head"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / The work</p>{K('The work')}<h1>No job too big or small.</h1>
<p class="lede">That is the line on Bobby&rsquo;s logo. Here is what it has meant for his customers.</p></div>{TAPE('','tape--head')}</section>
<div class="wrap sv-list">{''.join(sv(i,s) for i,s in enumerate(SV))}</div>
<section class="wrap jobs rv" aria-labelledby="jb-h"><h2 id="jb-h">The job log</h2><ol class="job-log">{''.join(f'<li><time>{d}</time><b>{w}</b><span>{s}</span></li>' for d,w,s in JOBS)}</ol>
<p class="fine">Each line comes from a dated Google review or Bobby&rsquo;s own Google post.</p></section>
''', ld=[ORG, bc(('Home',''),('The work','services.html'))]+[{"@context":"https://schema.org","@type":"Service","name":s[1],"provider":{"@type":"GeneralContractor","name":"B&B Home Improvements"},"areaServed":"Fayetteville, NC"} for s in SV])

# ---------- REVIEWS ----------
page('reviews.html','B&B Home Improvements Reviews | 4.9 Stars, Fayetteville NC',
 'Read eight Google reviews of Bobby Wilburn and B&B Home Improvements: bath and kitchen remodels, repairs and rebuilds in Fayetteville. Call (910) 336-7516.', f'''
<section class="page-head"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Reviews</p>{K('Reviews')}<h1>4.9 stars from 58 Google reviews.</h1>
<p class="lede">These are the eight most recent ones we could read in full, word for word.</p></div>{TAPE('','tape--head')}</section>
<div class="wrap rv-wall">{''.join(rcard(r) for r in REV)}</div>
<section class="wrap sources rv"><h2>Where these come from</h2><p>Copied from B&amp;B&rsquo;s Google listing data on the <a href="{EXA}" rel="noopener">Exa place page</a>. All eight are 5 out of 5. Reviewer names were not in the snapshot. Three dots mark where the snapshot cuts a review short. Two reviewers used dashes, which we changed to commas. <a href="{CR}" rel="noopener">ContractorsRanked</a> shows the same listing at 4.9 from 57.</p>
<p class="note"><span class="ph">Placeholder</span> a live Google reviews feed once Bobby approves it.</p></section>
''', ld=[ORG, bc(('Home',''),('Reviews','reviews.html'))])

# ---------- ABOUT ----------
page('about.html','About Bobby Wilburn | B&B Home Improvements, Fayetteville NC',
 'Bobby Wilburn runs B&B Home Improvements in Fayetteville: a hands on, old school contractor with 30 something years in the trade and a crew. Call today.', f'''
<section class="page-head page-head--red"><div class="wrap ab-head"><div><p class="crumbs"><a href="index.html">Home</a> / About</p>{K('About')}<h1>The old school contractor.</h1>
<p class="lede">That is what one customer called Bobby Wilburn. It fits.</p></div>
<div class="ab-ph"><span class="ph">Placeholder</span> photo of Bobby and the crew on a job</div></div></section>
<div class="wrap ab">
 <section class="ab-copy rv"><h2>What we know from his customers</h2>
  <p>Bobby Wilburn owns B&amp;B Home Improvements and works with a crew. Customers describe him as responsive, on time, honest and reasonably priced, with &ldquo;very high standards.&rdquo; One says he has 30&#8209;something years in the trade. A landlord calls him &ldquo;the go to contractor on all my home repair and improvements on my properties.&rdquo;</p>
  <p class="note"><span class="ph">Placeholder</span> Bobby&rsquo;s own story: how he started, what B&amp;B stands for, the size of the crew, and licensing and insurance details for the trust strip. Nothing here is invented.</p></section>
 <section class="ab-facts rv"><h2>The basics</h2><dl>
  <div><dt>Owner</dt><dd>Bobby Wilburn</dd></div>
  <div><dt>Based in</dt><dd>Fayetteville, NC 28311</dd></div>
  <div><dt>Hours</dt><dd>Monday to Saturday, 7am to 7pm</dd></div>
  <div><dt>Phone</dt><dd><a href="tel:{TEL}">{TEL_H}</a></dd></div>
  <div><dt>Google</dt><dd>4.9 from 58 reviews</dd></div>
  <div><dt>Tagline</dt><dd>&ldquo;No job too big or small&rdquo;</dd></div>
 </dl><p class="fine">From B&amp;B&rsquo;s Google listing and logo.</p></section>
</div>
''', ld=[ORG, bc(('Home',''),('About','about.html'))])

# ---------- CONTACT ----------
page('contact.html','Free Remodeling Estimate | B&B Home Improvements, NC',
 'Ask Bobby Wilburn for a free estimate on a bathroom, kitchen, windows, deck or repair in Fayetteville NC. Call (910) 336-7516, Monday to Saturday 7 to 7.', f'''
<section class="page-head"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / Free estimate</p>{K('Free estimate')}<h1>Tell Bobby about the job.</h1>
<p class="lede">Call Monday to Saturday, 7am to 7pm, or send the details and B&amp;B calls you back.</p></div>{TAPE('','tape--head')}</section>
<div class="wrap q-grid">
<form id="qform" class="rv" novalidate>
 <fieldset><legend>What is the job?</legend><div class="chips-in">{''.join(f'<label><input type="checkbox" name="job" value="{v}"' + (' checked' if i==0 else '') + f'> {v}</label>' for i,v in enumerate(['Bathroom','Kitchen','Windows or siding','Deck or patio','Repair','Something else']))}</div></fieldset>
 <div class="two"><div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required></div><div class="field"><label for="q-tel">Phone</label><input id="q-tel" name="tel" type="tel" autocomplete="tel" required></div></div>
 <div class="field"><label for="q-where">Neighborhood or address</label><input id="q-where" name="where" autocomplete="street-address"></div>
 <div class="field"><label for="q-msg">What do you have in mind?</label><textarea id="q-msg" name="msg" rows="5"></textarea></div>
 <button class="btn btn--red" type="submit">Send to Bobby</button><p id="qmsg" class="note" role="status" aria-live="polite">Demo form. Nothing is sent.</p>
</form>
<aside class="rv"><div class="card"><p class="kicker"><span class="tick" aria-hidden="true"></span>Call</p><a class="phone" href="tel:{TEL}">{TEL_H}</a><p>Monday to Saturday<br>7am to 7pm</p><p class="fine">Fayetteville, NC 28311</p></div></aside>
</div>
''', ld=[ORG, bc(('Home',''),('Free estimate','contact.html'))])

page('404.html','Page Not Found | B&B Home Improvements, Fayetteville NC',
 'That page is not here. Head back to the B&B Home Improvements home page, or call Bobby Wilburn at (910) 336-7516 for remodeling and repairs in Fayetteville.',
 f'<section class="wrap nf">{K("404")}<h1>Measured twice. Still not here.</h1><p class="lede">That page does not exist.</p><p><a class="btn btn--red" href="index.html">Back to the home page</a></p></section>')
print('built')
