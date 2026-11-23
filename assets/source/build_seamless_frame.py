with open('assets/source/new_frame.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .visual and .showcase-stage styles to be seamless
old_visual_css = """.visual.printer-demo{background:#eef4f8;isolation:isolate;overflow:hidden;position:relative;display:flex;align-items:center;justify-content:center;padding:22px 28px}
.visual.printer-demo:before{content:"";position:absolute;inset:18px;border:1px solid #d0dee8;z-index:6;pointer-events:none}

.showcase-stage{position:relative;width:100%;height:100%;border-radius:14px;background:#090f14;box-shadow:0 18px 45px rgba(20,40,58,0.22),inset 0 1px 0 rgba(255,255,255,0.1);overflow:hidden;border:1px solid #283a48}"""

new_visual_css = """.visual.printer-demo{background:radial-gradient(circle at 62% 48%,#ffffff 0%,#e4eff5 55%,#d8e7f0 100%);isolation:isolate;overflow:hidden;position:relative;display:flex;align-items:center;justify-content:center;padding:12px}
.visual.printer-demo:before{display:none}

.showcase-stage{position:relative;width:100%;height:100%;background:transparent;box-shadow:none;overflow:hidden;border:none;filter:drop-shadow(0 24px 38px rgba(15,35,48,0.22))}"""

html = html.replace(old_visual_css, new_visual_css)

# 2. Viewport background transparent
html = html.replace(
    '.cinematic-viewport{position:absolute;inset:0;perspective:1400px;overflow:hidden;background:#060a0e;display:flex;align-items:center;justify-content:center}',
    '.cinematic-viewport{position:absolute;inset:0;perspective:1400px;overflow:hidden;background:transparent;display:flex;align-items:center;justify-content:center}'
)

# 3. Hide all overlays: buttons, HUD telemetry, captions, progress bar, reticle
overlay_hide_css = """
.printer-overlay-top, .printer-overlay-bottom, .printer-progress, .focus-reticle { display: none !important; }
"""
html = html.replace('/* Top Bar: Director Angle Switcher */', overlay_hide_css + '\n/* Top Bar: Director Angle Switcher */')

with open('assets/source/seamless_frame.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully created assets/source/seamless_frame.html')
