#!/usr/bin/env python3
"""Generate a dependency-free GitHub Pages portfolio from structured project data."""
from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'projects.json').read_text(encoding='utf-8'))
OWNER = 'choppa129'
BASE = 'https://choppa129.github.io'

def esc(x): return html.escape(str(x), quote=True)

def header(depth=0):
    home = '../' * depth or './'
    return f'''<header class="site-header" id="top">
  <div class="container nav-shell">
    <a class="logo" href="{home}index.html" aria-label="Xue Jiang homepage"><span class="logo-mark">X<span class="logo-slash">/</span>J</span><span class="logo-label">XUE JIANG<span class="logo-detail">ROBOTICS & RESEARCH</span></span></a>
    <button class="menu-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="main-menu"><span></span><span></span></button>
    <nav class="site-nav" id="main-menu" aria-label="Main navigation">
      <a href="{home}index.html#about">About</a>
      <a href="{home}index.html#research">Research</a>
      <a href="{home}index.html#projects">Projects</a>
      <a href="{home}index.html#experience">Experience</a>
      <a class="nav-contact" href="{home}index.html#contact">Let's connect <span aria-hidden="true">↗</span></a>
    </nav>
  </div>
</header>'''

def footer(depth=0):
    home = '../' * depth or './'
    return f'''<footer class="site-footer"><div class="container footer-inner"><a class="footer-monogram" href="{home}index.html">X/J</a><p>Built with curiosity, code & good coffee.<br><span>© 2026 Xue Jiang · Atlanta, GA</span></p><a href="{home}index.html#top">Back to top <span aria-hidden="true">↑</span></a></div></footer>'''

def base(title, description, body, depth=0):
    prefix = '../' * depth or './'
    url = BASE + ('/' if depth == 0 else '/projects/' + title.lower().replace(' ', '-') + '/')
    # Set canonical at callsite below to avoid deriving inaccurate paths from titles.
    canonical = BASE + ('/' if depth == 0 else f'/projects/{CURRENT_SLUG}/')
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f6f6f1"><meta name="color-scheme" content="light">
<title>{esc(title)} | Xue Jiang</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} | Xue Jiang"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/main.js" defer></script>
</head><body><a href="#main" class="skip-link">Skip to content</a>
{header(depth)}
<main id="main">{body}</main>
{footer(depth)}
</body></html>'''

THUMB_LABELS = {
    'dexterous-manipulation': ('HUMAN MOTION', 'HAND POSE / ROBOT LEARNING'),
    'video-to-simulation': ('VIDEO → SIM', 'SCENE RECONSTRUCTION'),
    'radar-camera-fusion': ('SENSOR FUSION', 'RADAR × CAMERA'),
    'autonomous-marine-vehicle': ('AUTONOMOUS NAVIGATION', 'RRT / PID'),
    'toroidal-propeller': ('COMPUTATIONAL DESIGN', 'PARAMETRIC / CFD'),
}

def project_card(p, index, cls=''):
    label, sub = THUMB_LABELS[p['slug']]
    return f'''<a class="project-card {cls}" href="./projects/{esc(p['slug'])}/">
      <div class="project-visual typographic-thumb" aria-label="{esc(label)} — {esc(sub)}">
      <span class="visual-number">0{index}</span><div class="thumb-words"><span class="thumb-pre">{esc(p['category'])} / SELECTED WORK</span><strong>{esc(label)}</strong><span class="thumb-sub">{esc(sub)}</span></div></div>
      <div class="project-meta"><span>{esc(p['category'])}</span><span>{esc(p['year'])}</span></div>
      <h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p>
      <div class="card-foot"><span>{' / '.join(esc(t) for t in p['tags'][:3])}</span><span class="circle-arrow" aria-hidden="true">↗</span></div>
    </a>'''

def home_page():
    featured = DATA[:2]
    remaining = DATA[2:]
    research_cards = ''.join(project_card(p,i+1,'research-project') for i,p in enumerate(featured))
    works = ''.join(project_card(p,i+3,'') for i,p in enumerate(remaining))
    body=f'''
<section class="hero section-pad" aria-labelledby="hero-title"><div class="container hero-grid">
  <div class="hero-copy">
    <div class="eyebrow"><span class="eyebrow-line"></span> PORTFOLIO / 2026 <span class="eyebrow-small">GEORGIA TECH · ATLANTA</span></div>
    <p class="hero-intro">HELLO, I'M XUE JIANG <span class="wave">✳</span></p>
    <h1 id="hero-title">Making robots<br><em>understand</em> the<br>physical world<span class="period">.</span></h1>
    <p class="hero-desc">Robotics M.S. student at <strong>Georgia Tech</strong>. I work at the intersection of <strong>robot learning, perception, and simulation</strong>—turning real-world complexity into systems that can sense, reason, and act.</p>
    <div class="hero-actions"><a class="btn btn-dark" href="#projects">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="#about">More about me <span aria-hidden="true">↓</span></a></div>
    <div class="hero-status"><span class="status-dot"></span> Exploring Summer 2027 robotics & ML internships</div>
  </div>
  <div class="hero-visual"><div class="hero-art hero-type" aria-label="Three research areas: robot learning, perception and simulation"><div class="hero-type-header"><span>XJ / RESEARCH INDEX</span><span>2026 — ONGOING</span></div><div class="hero-type-body"><span class="hero-type-caption">FIELDS OF EXPLORATION</span><strong>ROBOT<br>LEARNING<span> /01</span></strong><strong>PERCEPTION<span> /02</span></strong><strong>SIMULATION<span> /03</span></strong></div><div class="hero-type-footer"><span>ENGINEERING ↗ INTELLIGENCE</span><span>GT / ATL</span></div></div></div>
</div></section>
<section class="overview-rail" aria-label="At a glance"><div class="container overview-inner"><div><span class="overview-label">CURRENT FOCUS</span><strong>Embodied AI</strong></div><div><span class="overview-label">RESEARCH</span><strong>Manipulation · Real-to-Sim</strong></div><div><span class="overview-label">BACKGROUND</span><strong>Ocean Engineering → Robotics</strong></div><div class="rail-round" aria-hidden="true">↘</div></div></section>
<section class="about-section section-pad" id="about"><div class="container about-grid"><div class="section-heading"><span class="section-index">01 / ABOUT</span><h2>Driven by a curiosity for <span class="serif-em">how things move.</span></h2></div>
<div class="about-content"><p class="about-lead">I am a first-year Master's student in Robotics at the Georgia Institute of Technology, with an undergraduate background in Naval Architecture and Ocean Engineering from Shanghai Jiao Tong University.</p><p>From building an autonomous surface vehicle to reconstructing robot-ready environments from video, I'm interested in connecting rigorous engineering with learning-based intelligence. Today, my research spans dexterous manipulation and real-to-sim pipelines for robot learning.</p><div class="about-tags"><span>Robot Learning</span><span>Computer Vision</span><span>Simulation</span><span>Controls</span><span>Sensor Fusion</span></div><div class="achievement"><span class="achievement-icon">✳</span><div><strong>RoboMaster 2023 National Champion</strong><small>Member of the Shanghai Jiao Tong University robotics team</small></div></div><a class="inline-arrow" href="https://github.com/{OWNER}" target="_blank" rel="noopener noreferrer">Find me on GitHub <span aria-hidden="true">↗</span></a></div></div></section>
<section class="research-section section-pad" id="research"><div class="container"><div class="section-topline"><span class="section-index light">02 / RESEARCH</span><span class="micro-note">ONGOING WORK · 2026—PRESENT</span></div><div class="section-title-row"><h2>Researching the next<br>generation of <em>robot intelligence.</em></h2><p>Combining physical understanding, scalable data, and simulation to make robots more capable in unstructured environments.</p></div><div class="research-grid">{research_cards}</div><p class="research-disclaimer">Research descriptions are high-level summaries of ongoing work. No generated illustrations are used.</p></div></section>
<section class="work-section section-pad" id="projects"><div class="container"><div class="section-topline"><span class="section-index">03 / SELECTED PROJECTS</span><span class="micro-note">BUILD · TEST · ITERATE</span></div><div class="section-title-row work-title"><h2>Ideas translated into <em>working systems.</em></h2><p>Hands-on engineering across autonomous navigation, perception, and computational design.</p></div><div class="project-grid">{works}</div></div></section>
<section class="experience-section section-pad" id="experience"><div class="container experience-grid"><div><span class="section-index">04 / EXPERIENCE</span><h2>A foundation in<br><em>engineering practice.</em></h2><p class="experience-sub">Research-led exploration, informed by design, simulation and real-world validation.</p></div><div class="timeline">
<div class="timeline-item"><div class="timeline-date">2026 — NOW</div><div><h3>Georgia Institute of Technology</h3><p>Robotics M.S. · Research with LIDAR Lab and STAR Lab</p></div><span>01</span></div>
<div class="timeline-item"><div class="timeline-date">2024 — 2025</div><div><h3>Eaton</h3><p>Mechanical Design Intern · Consumer electrical products, packaging, and design validation</p></div><span>02</span></div>
<div class="timeline-item"><div class="timeline-date">2024</div><div><h3>China Merchants Group</h3><p>Electrical Engineering Intern · Marine automation drawings and I/O documentation</p></div><span>03</span></div>
<div class="timeline-item"><div class="timeline-date">2022 — 2025</div><div><h3>Shanghai Jiao Tong University</h3><p>B.Eng. · Naval Architecture & Ocean Engineering · Robotics and hydrodynamics projects</p></div><span>04</span></div></div></div></section>
<section class="publication-section section-pad" id="publications"><div class="container publication-layout"><div><span class="section-index">05 / PUBLICATIONS & HIGHLIGHTS</span><h2>Research, on paper<br>and <em>in practice.</em></h2></div><div class="pub-panel"><div class="pub-top"><span>CONFERENCE PAPER · 2024</span><span aria-hidden="true">↗</span></div><h3>Research on the Influence of Key Geometry Parameters on the Hydrodynamic Performance of Toroidal Propellers</h3><p>35th National Conference on Hydrodynamics · Harbin, China</p><div class="pub-bottom"><span>Computational Fluid Dynamics</span><span>Propeller Design</span><span>Parametric Modeling</span></div></div></div></section>
<section class="contact-section section-pad" id="contact"><div class="container contact-grid"><div><span class="section-index light">06 / WHAT'S NEXT</span><h2>Let's build something<br><em>meaningful.</em></h2></div><div class="contact-copy"><p>I'm interested in research collaborations and Summer 2027 internship opportunities in robotics, machine learning, and simulation.</p><a class="btn btn-light" href="https://github.com/{OWNER}" target="_blank" rel="noopener noreferrer">Explore my GitHub <span aria-hidden="true">↗</span></a><p class="contact-note">For direct inquiries, use the contact information on my GitHub profile.</p></div></div><div class="contact-orbit orbit-one"></div><div class="contact-orbit orbit-two"></div></section>'''
    return base('Robotics Portfolio','Xue Jiang is a Georgia Tech Robotics M.S. student working on robot learning, dexterous manipulation, scene reconstruction, computer vision, and simulation.',body)

def detail_page(p, prev, nextp):
    category=esc(p['category']); slug=esc(p['slug']); title=esc(p['title']);
    tags=''.join(f'<span>{esc(t)}</span>' for t in p['tags'])
    contributions=''.join(f'<li><span class="li-arrow" aria-hidden="true">↗</span><span>{esc(c)}</span></li>' for c in p['contributions'])
    workflow=''.join(f'<div class="workflow-step"><span class="step-no">0{i+1}</span><div><h3>{esc(s[0])}</h3><p>{esc(s[1])}</p></div></div>' for i,s in enumerate(p['workflow']))
    highlights=''.join(f'<div class="highlight"><strong>{esc(h[0])}</strong><span>{esc(h[1])}</span></div>' for h in p['highlights'])
    repo = f'<a class="btn btn-dark" href="{esc(p["repo"])}" target="_blank" rel="noopener noreferrer">View source on GitHub <span aria-hidden="true">↗</span></a>' if p.get('repo') else ''
    note='Ongoing research · details are intentionally high-level.' if p['category']=='Research' else 'Read the linked repository for source code and original project material.'
    body=f'''
<section class="detail-hero section-pad"><div class="container"><a class="breadcrumb" href="../../index.html#projects"><span aria-hidden="true">←</span> BACK TO ALL PROJECTS</a><div class="detail-hero-grid"><div><div class="detail-label">{category} / {esc(p['year'])}</div><h1>{title}<span class="period">.</span></h1><p class="detail-summary">{esc(p['summary'])}</p><div class="detail-buttons">{repo}<a class="btn btn-outline" href="../../index.html#contact">Get in touch <span aria-hidden="true">↗</span></a></div></div><div class="detail-art detail-type" aria-label="{esc(p['focus'])}"><span class="detail-type-eyebrow">PROJECT FILE / {category}</span><strong>{esc(THUMB_LABELS[p['slug']][0])}</strong><span class="detail-type-sub">{esc(THUMB_LABELS[p['slug']][1])}</span><div class="detail-art-caption">FOCUS / {esc(p['focus'])} <span aria-hidden="true">↗</span></div></div></div>
<div class="detail-facts"><div><span>FOCUS AREA</span><strong>{esc(p['focus'])}</strong></div><div><span>WHEN</span><strong>{esc(p['timeline'])}</strong></div><div><span>SETTING</span><strong>{esc(p['setting'])}</strong></div></div></div></section>
<section class="detail-content section-pad"><div class="container detail-content-grid"><aside class="detail-aside"><span>THE PROJECT</span><div class="vertical-rule"></div><nav aria-label="On this page"><a href="#overview">01 Overview</a><a href="#contribution">02 Contributions</a><a href="#approach">03 Approach</a><a href="#takeaways">04 Highlights</a></nav></aside><div class="article-content"><section id="overview"><span class="section-index">01 / OVERVIEW</span><h2>The challenge</h2><p class="article-lead">{esc(p['challenge'])}</p><p>{esc(p['overview'])}</p></section><section id="contribution"><span class="section-index">02 / MY WORK</span><h2>What I contributed</h2><ul class="contributions">{contributions}</ul></section><section id="approach"><span class="section-index">03 / APPROACH</span><h2>How the system works</h2><div class="workflow">{workflow}</div></section><section id="takeaways"><span class="section-index">04 / HIGHLIGHTS</span><h2>{'Current direction' if p['category']=='Research' else 'Results & takeaways'}</h2><div class="highlight-grid">{highlights}</div><p class="article-note">{esc(p['takeaway'])}</p></section><div class="detail-tools"><span class="section-index">TECHNOLOGY / METHODS</span><div class="about-tags">{tags}</div><p class="diagram-note">{esc(note)}</p></div></div></div></section>
<section class="next-project"><div class="container"><span class="section-index light">NEXT PROJECT</span><a href="../{esc(nextp['slug'])}/"><span>{esc(nextp['title'])}</span><span class="next-arrow" aria-hidden="true">↗</span></a></div></section>'''
    global CURRENT_SLUG
    CURRENT_SLUG=p['slug']
    return base(p['title'],p['summary'],body,depth=2)

(ROOT/'index.html').write_text(home_page(),encoding='utf-8')
for i,p in enumerate(DATA):
    d=ROOT/'projects'/p['slug'];d.mkdir(parents=True,exist_ok=True)
    (d/'index.html').write_text(detail_page(p, DATA[(i-1)%len(DATA)], DATA[(i+1)%len(DATA)]),encoding='utf-8')
urls=[BASE+'/']+[f"{BASE}/projects/{p['slug']}/" for p in DATA]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+u+'</loc></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
print('Built',len(DATA),'project pages and the homepage.')
