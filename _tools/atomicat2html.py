#!/usr/bin/env python3
"""Converte o JSON do builder da Atomicat em uma pagina HTML estatica.

Uso: python3 atomicat2html.py builder.json saida.html --video-id ID --account ACC [--title T]
"""
import argparse, json, re, html

MOBILE_BP = 767
fonts = set()
css_desktop, css_tablet, css_mobile = [], [], []
UNITLESS = {"fontWeight", "zIndex", "lineHeight", "opacity", "flexGrow", "flexShrink", "order"}


def kebab(p):
    return re.sub(r"([A-Z])", lambda m: "-" + m.group(1).lower(), p)


def split(v):
    """Return (desktop, tablet, mobile) from a plain value or a responsive dict."""
    if isinstance(v, dict) and any(k in v for k in ("desktop", "tablet", "mobile")):
        return v.get("desktop"), v.get("tablet"), v.get("mobile")
    return v, None, None


def decls(style, skip=()):
    d, t, m = [], [], []
    for p, v in (style or {}).items():
        if p in skip or v is None:
            continue
        if p == "border" and isinstance(v, dict):
            if v.get("style"):
                d.append(f"border-style:{v['style']}")
            if v.get("color"):
                d.append(f"border-color:{v['color']}")
            continue
        if isinstance(v, dict) and not any(k in v for k in ("desktop", "tablet", "mobile")):
            continue  # nested group handled elsewhere
        if p == "fontFamily":
            fonts.add(str(v).split(",")[0].strip("'\" "))
        vals = list(split(v))
        if p in ("right", "left") and isinstance(vals[0], str) and vals[0].startswith("-") and vals[2] is None:
            vals[2] = "20%"  # selos posicionados fora do card: no mobile trazemos para dentro
        for bucket, val in zip((d, t, m), vals):
            if val is None or val == "":
                continue
            if isinstance(val, (int, float)) and p not in UNITLESS:
                val = f"{val}px"
            prop = kebab(p)
            if p == "fontFamily":
                val = f"'{val}',sans-serif" if "," not in str(val) else val
            bucket.append(f"{prop}:{val}")
    return d, t, m


def rule(sel, style, skip=()):
    d, t, m = decls(style, skip)
    if d:
        css_desktop.append(f"{sel}{{{';'.join(d)}}}")
    if t:
        css_tablet.append(f"{sel}{{{';'.join(t)}}}")
    if m:
        css_mobile.append(f"{sel}{{{';'.join(m)}}}")


def link_wrap(inner, misc):
    href = misc.get("href")
    if href:
        return f'<a href="{html.escape(href, quote=True)}" class="ac-link">{inner}</a>'
    return inner


def render_icon(misc, cls):
    ic = misc.get("icon") or {}
    if ic.get("isCustom") and ic.get("svg"):
        svg = re.sub(r"^<p>|</p>$", "", ic["svg"].strip())
        return f'<span class="ac-icon {cls}">{svg}</span>'
    if misc.get("src"):
        return f'<span class="ac-icon {cls}"><img src="{misc["src"]}" alt="{html.escape(misc.get("alt") or "")}"></span>'
    klass = ic.get("class") or []
    if isinstance(klass, list) and klass:
        fa = [klass[0]] + ["fa-" + k if not k.startswith("fa-") else k for k in klass[1:]]
        return f'<span class="ac-icon {cls}"><i class="{" ".join(fa)}"></i></span>'
    return f'<span class="ac-icon {cls}"></span>'


def render(node, video_html, top=False):
    misc = node.get("misc", {})
    t = misc.get("type")
    key = (node.get("compKey") or node.get("contKey"))[:8]
    st = node.get("style") or {}
    o, n = f"o-{key}", f"n-{key}"
    rule(f".{o}", {**(st.get("topCont") or {}), **(st.get("outer") or {})})

    if t == "container":
        cst = dict(st.get("container") or {})
        if top and misc.get("contentWidth") != "fullWidth":
            # Atomicat pinta fundo/borda do container raiz na largura total e centraliza só o conteúdo
            move = {k: cst.pop(k) for k in list(cst) if k.startswith("background") or k.startswith("border")}
            rule(f".{o}", move)
        rule(f".{n}", cst)
        kids = "".join(render(c, video_html) for c in node.get("contents", []) or [] if isinstance(c, dict))
        if top:
            boxed = misc.get("contentWidth") != "fullWidth"
            return (f'<section class="ac-sec {o}"><div class="ac-cont {n}{" ac-boxed" if boxed else ""}">'
                    f"{kids}</div></section>")
        boxed = misc.get("contentWidth") == "boxed"
        return f'<div class="ac-wrap {o}"><div class="ac-cont {n}{" ac-boxed" if boxed else ""}">{kids}</div></div>'

    if t == "text":
        tag = misc.get("tag") or "div"
        rule(f".{n}", st.get("text"))
        rule(f".{n} a", {"color": (st.get("text") or {}).get("color")})
        inner = f'<{tag} class="ac-text {n}">{misc.get("content") or ""}</{tag}>'
        return f'<div class="ac-wrap {o}">{link_wrap(inner, misc)}</div>'

    if t == "image":
        rule(f".{n}", st.get("image"))
        alt = html.escape(misc.get("alt") or "", quote=True)
        lazy = ' loading="lazy"' if misc.get("lazyLoad") else ""
        w, h = misc.get("width"), misc.get("height")
        dims = f' width="{w}" height="{h}"' if w and h else ""
        inner = f'<img class="ac-img {n}" src="{misc.get("src")}" alt="{alt}"{dims}{lazy}>'
        return f'<div class="ac-wrap {o}">{link_wrap(inner, misc)}</div>'

    if t == "icon":
        ist = dict(st.get("icon") or {})
        rule(f".{n}", ist)
        rule(f".{n} svg,.{n} img", {"width": "100%", "height": "auto"})
        return f'<div class="ac-wrap {o}">{render_icon(misc, n)}</div>'

    if t == "button":
        bst = dict(st.get("button") or {})
        rule(f".{n}", bst, skip=("icon",))
        if isinstance(bst.get("icon"), dict):
            rule(f".{n} i", bst["icon"])
            rule(f".{n} i", {"fontSize": bst["icon"].get("height")})
        icon = ""
        ic = misc.get("icon") or {}
        if ic.get("class"):
            k = ic["class"]
            icon = f'<i class="{k[0]} ' + " ".join("fa-" + x for x in k[1:]) + '"></i>'
        content = re.sub(r"^<p>(.*)</p>$", r"\1", (misc.get("content") or "").strip())
        body = f"{icon}<span>{content}</span>" if ic.get("position", "before") == "before" else f"<span>{content}</span>{icon}"
        href = html.escape(misc.get("href") or "#", quote=True)
        return f'<div class="ac-wrap {o}"><a class="ac-btn {n}" href="{href}">{body}</a></div>'

    if t == "countdown":
        cst = st.get("countdown") or {}
        rule(f".{n}", cst.get("container"))
        rule(f".{n}", {k: v for k, v in cst.items() if k in ("gap", "maxWidth")})
        rule(f".{n} .cd-d", cst.get("digits"))
        rule(f".{n} .cd-l", cst.get("label"))
        items = misc.get("items") or []
        show = [i["text"].lower() for i in items if i.get("show")]
        parts = "".join(
            f'<span class="cd-u" data-u="{u}"><span class="cd-d">00</span>'
            + ("" if misc.get("hideLabel") else f'<span class="cd-l">{u.title()}</span>') + "</span>"
            for u in show)
        dur = misc.get("dateTime") or "10:00"
        return f'<div class="ac-wrap {o}"><div class="ac-cd {n}" data-dur="{dur}">{parts}</div></div>'

    if t == "video":
        rule(f".{n}", st.get("video"))
        return f'<div class="ac-wrap {o}"><div class="ac-video {n}">{video_html}</div></div>'

    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("builder"); ap.add_argument("out")
    ap.add_argument("--video-id", required=True); ap.add_argument("--account", required=True)
    ap.add_argument("--title", default=None); ap.add_argument("--max-width", default="400px")
    ap.add_argument("--ratio", default="177.77777777777777%")
    ap.add_argument("--src-map", default=None, help='JSON {"url antiga": "url nova"} para trocar imagens')
    ap.add_argument("--delay", type=int, default=0, help="segundos do pitch para revelar a oferta")
    ap.add_argument("--hide-from", type=int, default=None, help="indice da 1a secao (0-based) escondida ate o pitch")
    ap.add_argument("--hide-to", type=int, default=None, help="indice da ultima secao escondida (inclusive)")
    a = ap.parse_args()
    d = json.load(open(a.builder))
    page = d.get("page") or {}
    for f in (page.get("fontFamily") or {}).values():
        if f:
            fonts.add(f)

    vid = a.video_id
    video_html = (
        f'<vturb-smartplayer id="vid-{vid}" style="display:block;margin:0 auto;width:100%;max-width:{a.max_width};">'
        f'<div class="vturb-player-placeholder" style="position:relative;width:100%;padding:{a.ratio} 0 0;z-index:0;background-color:black;"></div>'
        f"</vturb-smartplayer>"
        f'<script type="text/javascript">var s=document.createElement("script");'
        f's.src="https://scripts.converteai.net/{a.account}/players/{vid}/v4/player.js",s.async=!0,document.head.appendChild(s);</script>'
    )

    parts = []
    for i, sec in enumerate(d["sections"]):
        h = render(sec, video_html, top=True)
        if a.delay and a.hide_from is not None and a.hide_from <= i <= (a.hide_to if a.hide_to is not None else 10**6):
            h = h.replace('<section class="ac-sec ', '<section class="ac-sec esconder ', 1)
        parts.append(h)
    body = "".join(parts)
    colors = page.get("color") or {}
    ff = page.get("fontFamily") or {}
    base = f"""
*,*::before,*::after{{box-sizing:border-box}}
html,body{{margin:0;padding:0;overflow-x:hidden}}
body{{background:{page.get('background') or '#fff'};color:{colors.get('text') or '#222'};font-family:'{ff.get('text') or 'Montserrat'}',sans-serif;line-height:1.4;-webkit-font-smoothing:antialiased}}
h1,h2,h3,h4,h5,h6{{color:{colors.get('heading') or 'inherit'};font-family:'{ff.get('heading') or 'Montserrat'}',sans-serif;margin:0}}
p{{margin:0}}
img{{max-width:100%;display:block}}
a{{color:inherit}}
.ac-link{{text-decoration:none;color:inherit;display:block}}
.ac-sec{{width:100%;display:flex;flex-direction:column;align-items:center}}
.ac-cont{{width:100%;display:flex;flex-direction:column}}
.ac-sec>.ac-boxed{{max-width:1140px;margin:0 auto}}
.ac-wrap>.ac-boxed{{max-width:1140px;margin:0 auto}}
.ac-wrap{{display:flex;flex-direction:column;max-width:100%;min-width:0;position:relative}}
.ac-cont{{min-width:0;position:relative}}\n.ac-wrap>.ac-cont{{flex-grow:1}}
.ac-cont>*{{min-width:0}}
.ac-text{{margin:0;word-wrap:break-word}}
.ac-text *:not(i),.ac-btn *:not(i){{font-family:inherit}}
.ac-icon{{display:inline-flex;align-items:center;justify-content:center;line-height:1}}
.ac-btn{{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;cursor:pointer;line-height:1.2;border-color:transparent}}
.ac-cd{{display:flex;justify-content:center;align-items:center}}
.ac-cd .cd-u{{display:flex;flex-direction:column;align-items:center;line-height:1}}
.ac-video{{width:100%}}
"""
    fam = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700;800" for f in sorted(fonts) if f)
    custom = page.get("customCss") or ""
    title = html.escape(a.title or d.get("title") or "Video")
    css = base + "\n".join(css_desktop)
    if css_tablet:
        css += "\n@media (max-width:1024px){" + "\n".join(css_tablet) + "}"
    if css_mobile:
        css += f"\n@media (max-width:{MOBILE_BP}px){{" + "\n".join(css_mobile) + "}"
    js = """
<script>
(function(){document.querySelectorAll('.ac-cd').forEach(function(el){
var p=(el.getAttribute('data-dur')||'10:00').split(':').map(Number);var total=p.length===3?p[0]*3600+p[1]*60+p[2]:p[0]*60+(p[1]||0);
var end=Date.now()+total*1000;function pad(n){return(n<10?'0':'')+n}
function tick(){var r=Math.max(0,Math.round((end-Date.now())/1000));var v={days:Math.floor(r/86400),hours:Math.floor(r%86400/3600),minutes:Math.floor(r%3600/60),seconds:r%60};
var units=[].slice.call(el.querySelectorAll('.cd-u'));var showSec=units.some(function(u){return u.dataset.u==='seconds'});
if(!showSec&&r>0&&v.seconds>0&&units.length&&units[units.length-1].dataset.u==='minutes'){v.minutes+=1}
units.forEach(function(u){u.querySelector('.cd-d').textContent=pad(v[u.dataset.u]||0)});if(r>0)setTimeout(tick,1000)}tick()})})();
</script>"""
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link rel="preload" href="https://scripts.converteai.net/{a.account}/players/{vid}/v4/player.js" as="script">
<link rel="preload" href="https://scripts.converteai.net/lib/js/smartplayer-wc/v4/smartplayer.js" as="script">
<link rel="dns-prefetch" href="https://cdn.converteai.net">
<style>{css}</style>
<style>{custom}</style>
</head>
<body>
{body}
{js}
</body>
</html>
"""
    if a.src_map:
        for old, new in json.loads(a.src_map).items():
            out = out.replace(old, new)
    if a.delay:
        delay_js = (
            "<style>.esconder{display:none}</style>\n<script>var delaySeconds=%d;"
            "var player=document.querySelector('vturb-smartplayer');"
            "player.addEventListener('player:ready',function(){"
            "player.displayHiddenElements(delaySeconds,['.esconder'],{persist:true});});"
            "if(/[?&]preview=1/.test(location.search)){document.querySelectorAll('.esconder').forEach(function(e){e.style.display='block'})}"
            "</script>" % a.delay)
        out = out.replace("</body>", delay_js + "\n</body>")
    open(a.out, "w").write(out)
    print("ok", len(out), "bytes; fonts:", sorted(fonts))


if __name__ == "__main__":
    main()
