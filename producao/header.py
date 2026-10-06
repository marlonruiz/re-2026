from playwright.sync_api import sync_playwright
css="""*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px}
.c{width:1920px;height:1080px;position:relative;overflow:hidden;background:#180E0A;font-family:Poppins,"Noto Color Emoji",sans-serif;color:#fff;
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.g{position:absolute;border-radius:50%}
.g1{width:1500px;height:1500px;left:210px;top:-210px;background:radial-gradient(circle,rgba(232,87,42,.55),rgba(232,87,42,0) 62%)}
.g2{width:900px;height:900px;left:-300px;top:500px;background:radial-gradient(circle,rgba(255,201,77,.18),rgba(255,201,77,0) 65%)}
.g3{width:900px;height:900px;right:-300px;top:-350px;background:radial-gradient(circle,rgba(255,201,77,.14),rgba(255,201,77,0) 65%)}
.bar{position:absolute;left:0;right:0;bottom:0;height:22px;background:#E8572A}
.f{position:absolute;font-size:120px;line-height:1;filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}
.e{font-size:120px;line-height:1;margin-bottom:20px;position:relative}
.k{font-weight:700;font-size:34px;letter-spacing:12px;color:#FFE2D3;position:relative;margin-bottom:16px}
.t{font-weight:800;font-size:124px;line-height:.98;position:relative;letter-spacing:-2px}
.t span{color:#FFC94D}
.s{position:relative;margin-top:36px;font-size:40px;font-weight:600;background:#E8572A;padding:16px 46px;border-radius:999px;box-shadow:0 14px 40px rgba(232,87,42,.35)}
.lojas{position:relative;margin-top:28px;font-size:26px;letter-spacing:6px;color:#E8A07F;font-weight:600}"""
fl=[('🎁',150,170,-12),('🏷️',300,760,14),('🧴',1640,190,10),('🛒',1600,720,-10),('✨',520,90,0),('💛',1380,880,12)]
fx=''.join(f"<div class=f style='left:{x}px;top:{y}px;transform:rotate({r}deg)'>{e}</div>" for e,x,y,r in fl)
html=f"""<style>{css}</style><div class=c><div class='g g1'></div><div class='g g2'></div><div class='g g3'></div>{fx}
<div class=e>🛍️</div><div class=k>ÁREA DE MEMBROS</div><div class=t>CLUBE DE <span>ACHADINHOS</span></div>
<div class=s>Indique e receba por cada compra</div><div class=lojas>SHOPEE · MERCADO LIVRE · AMAZON</div><div class=bar></div></div>"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.set_content(html); pg.wait_for_timeout(300)
    pg.screenshot(path='header_1920x1080.png')
    b.close()
