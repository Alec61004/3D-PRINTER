import json

# Read original frame output
with open('C:/Users/PC/.gemini/antigravity/brain/b5133d84-ab1d-40dc-8afd-28ec28e9a0c1/.system_generated/steps/5059/output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

data = json.loads(text)
html = data['html']

# 1. Replace image src with 4K Master
html = html.replace('https://doop.design/a/vecf4JbEZh.jpg', 'https://doop.design/a/pGL9LC_97X.jpg')

# 2. Update transform-origin to exact nozzle coordinates: 55.81% 44.01%
html = html.replace('transform-origin:55.67% 43.88%', 'transform-origin:55.81% 44.01%')
html = html.replace('circle at 55.67% 43.88%', 'circle at 55.81% 44.01%')
html = html.replace('left:55.67%;top:43.88%', 'left:55.81%;top:44.01%')

# 3. Viewport & Gimbal 16:9 alignment
html = html.replace(
    '.cinematic-viewport{position:absolute;inset:0;perspective:1400px;overflow:hidden;background:#060a0e}',
    '.cinematic-viewport{position:absolute;inset:0;perspective:1400px;overflow:hidden;background:#060a0e;display:flex;align-items:center;justify-content:center}'
)
html = html.replace(
    '.camera-gimbal-3d{position:relative;width:100%;height:100%;transform-style:preserve-3d;transform-origin:55.81% 44.01%;will-change:transform;transition:transform 1.8s cubic-bezier(0.25, 1.0, 0.3, 1.0)}',
    '.camera-gimbal-3d{position:relative;height:100%;aspect-ratio:16/9;flex-shrink:0;transform-style:preserve-3d;transform-origin:55.81% 44.01%;will-change:transform;transition:transform 1.8s cubic-bezier(0.25, 1.0, 0.3, 1.0)}'
)

# 4. Replace old CSS blocks with active printing simulation styles
old_css_marker = '/* KINEMATIC VIBRATION & TOOLPATH CHUY\u1ec2N \u0110\u1ed8NG TH\u1ef0C T\u1ebe C\u1ee4M \u0110\u1ea6U \u0110\u00d9N COREXY 250 MM/S */'
end_css_marker = '/* V\u00f2ng ng\u1eafm ti\u00eau c\u1ef1 khi \u1ed1ng k\u00ednh ti\u1ebfp c\u1eadn c\u1ee5m v\u00f2i phun */'

idx_start = html.find(old_css_marker)
idx_end = html.find(end_css_marker)

print(f'CSS indices: {idx_start} to {idx_end}')

new_css = '''/* =========================================================================
   AUTHENTIC 3D PRINTING SIMULATION: CNC TOOLPATH, MOLTEN BEAD & ACTIVE FORMING
   ========================================================================= */
.active-print-rig{position:absolute;inset:0;pointer-events:none;z-index:4}
.extrusion-toolpath-svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}

/* Đế liên kết lớp dưới đang bồi đắp */
.bead-substrate{fill:none;stroke:rgba(25,30,36,0.9);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}

/* Dải nhựa PA-CF nóng chảy 245°C bồi đắp theo quỹ đạo toolpath CNC thực tế */
.bead-molten-active{fill:none;stroke:url(#coolingFilament);stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:118;stroke-dashoffset:118;animation:drawToolpath 5.4s cubic-bezier(0.4,0,0.2,1) infinite;filter:drop-shadow(0 0 1.5px rgba(255,120,20,0.75))}

@keyframes drawToolpath{
  0%{stroke-dashoffset:118;opacity:1}
  25.5%{stroke-dashoffset:88}
  28.2%{stroke-dashoffset:84.8}
  52.1%{stroke-dashoffset:56.8}
  54.7%{stroke-dashoffset:53.7}
  76.9%{stroke-dashoffset:27.7}
  79.6%{stroke-dashoffset:24.5}
  94%{stroke-dashoffset:0;opacity:1}
  98%{stroke-dashoffset:0;opacity:0.95}
  100%{stroke-dashoffset:118;opacity:0}
}

/* Cụm đầu phun E2 di chuyển thực tế theo G-code 250 mm/s */
.active-nozzle-carriage{position:absolute;left:55.81%;top:44.01%;pointer-events:none;z-index:5;will-change:transform;animation:corexyToolpath 5.4s cubic-bezier(0.4,0,0.2,1) infinite}

@keyframes corexyToolpath{
  0%{transform:translate(-12.1px,0px)}
  25.5%{transform:translate(17.9px,0px)}
  28.2%{transform:translate(17.9px,2.0px)}
  52.1%{transform:translate(-10.1px,2.0px)}
  54.7%{transform:translate(-10.1px,3.7px)}
  76.9%{transform:translate(15.9px,3.7px)}
  79.6%{transform:translate(15.9px,5.3px)}
  94%{transform:translate(-8.1px,5.3px)}
  98%{transform:translate(-12.1px,0px)}
  100%{transform:translate(-12.1px,0px)}
}

/* Điểm phát nhiệt & dòng chảy nóng chảy 245.2°C tại vòi đồng E2 */
.nozzle-thermal-glow{position:absolute;left:0;top:0;width:14px;height:14px;border-radius:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(255,235,120,1) 0%,rgba(255,120,20,0.85) 35%,rgba(255,40,0,0.35) 65%,transparent 85%);filter:drop-shadow(0 0 5px rgba(255,130,0,0.9));animation:thermalPulse 0.35s ease-in-out infinite alternate}
@keyframes thermalPulse{
  0%{transform:translate(-50%,-50%) scale(0.9);opacity:0.85}
  100%{transform:translate(-50%,-50%) scale(1.25);opacity:1.0;filter:drop-shadow(0 0 7px rgba(255,140,0,1))}
}

.nozzle-meniscus-dot{position:absolute;left:0;top:0;width:3.5px;height:3.5px;border-radius:50%;transform:translate(-50%,-50%);background:#ffffff;box-shadow:0 0 3px #ffbb00,0 0 5px #ff5500}

'''

if idx_start != -1 and idx_end != -1:
    html = html[:idx_start] + new_css + html[idx_end:]

# 5. Replace DOM block inside camera-gimbal
dom_marker_start = '<div class="kinematic-vibe-rig">'
dom_marker_end = '<!-- V\u00f2ng ng\u1eafm ti\u00eau c\u1ef1 khi \u1ed1ng k\u00ednh ti\u1ebfp c\u1eadn c\u1ee5m v\u00f2i phun E2 -->'

d_start = html.find(dom_marker_start)
d_end = html.find(dom_marker_end)
print(f'DOM indices: {d_start} to {d_end}')

new_dom = '''<!-- H\u1ec6 TH\u1ed0NG \u0110\u00d9N NH\u1ef0A N\u00d3NG CH\u1ea2Y B\u1ed2I \u0110\u1eaeP \u0110\u1ed2 G\u00c1 PA-CF THEO TH\u1edcI GIAN TH\u1ef0C -->
        <div class="active-print-rig">
          <svg class="extrusion-toolpath-svg" viewBox="0 0 1000 562.5" preserveAspectRatio="none">
            <defs>
              <linearGradient id="coolingFilament" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#14181c" />
                <stop offset="85%" stop-color="#242c34" />
                <stop offset="98%" stop-color="#ff7b00" />
                <stop offset="100%" stop-color="#ffe680" />
              </linearGradient>
            </defs>
            <!-- \u0110\u1ebf li\u00ean k\u1ebft l\u1edbp d\u01b0\u1edbi \u0111ang b\u1ed3i \u0111\u1eafp -->
            <path class="bead-substrate" d="M 546 247.5 L 576 247.5 A 1.2 1.2 0 0 1 576 249.5 L 548 249.5 A 1.2 1.2 0 0 1 548 251.2 L 574 251.2 A 1.2 1.2 0 0 1 574 252.8 L 550 252.8" />
            <!-- D\u1ea3i nh\u1ef1a PA-CF n\u00f3ng ch\u1ea3y 245\u00b0C b\u1ed3i \u0111\u1eafp theo qu\u1ef9 \u0111\u1ea1o toolpath CNC th\u1ef1c t\u1ebf -->
            <path class="bead-molten-active" d="M 546 247.5 L 576 247.5 A 1.2 1.2 0 0 1 576 249.5 L 548 249.5 A 1.2 1.2 0 0 1 548 251.2 L 574 251.2 A 1.2 1.2 0 0 1 574 252.8 L 550 252.8" />
          </svg>

          <!-- \u0110i\u1ec3m ph\u00e1t nhi\u1ec7t & d\u00f2ng ch\u1ea3y n\u00f3ng ch\u1ea3y t\u1ea1i \u0111\u1ea7u phun \u0111\u1ed3ng E2 -->
          <div class="active-nozzle-carriage" id="active-nozzle" title="Nozzle E2 245.2\u00b0C \u0111\u00f9n nh\u1ef1a PA-CF n\u00f3ng ch\u1ea3y">
            <div class="nozzle-thermal-glow"></div>
            <div class="nozzle-meniscus-dot"></div>
          </div>
        </div>

        '''

if d_start != -1 and d_end != -1:
    html = html[:d_start] + new_dom + html[d_end:]

# Also update alt text of image
html = html.replace('alt=\"To\u00e0n c\u1ea3nh m\u00e1y in 3D c\u00f4ng nghi\u1ec7p Deltrol CoreXY bu\u1ed3ng k\u00edn v\u00e0 c\u1ee5m \u0111\u1ea7u \u0111\u00f9n k\u00e9p E1/E2\"',
                    'alt=\"To\u00e0n c\u1ea3nh m\u00e1y in 3D c\u00f4ng nghi\u1ec7p Deltrol CoreXY bu\u1ed3ng k\u00edn \u0111ang in 3D \u0111\u1ed3 g\u00e1 PA-CF 4K\"')

with open('assets/source/new_frame.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success! Result written to assets/source/new_frame.html')
print('HTML length:', len(html))
print('doop-use count:', html.count('<doop-use'))
