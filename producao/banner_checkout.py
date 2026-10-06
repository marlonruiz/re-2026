from playwright.sync_api import sync_playwright
base="""*{margin:0;padding:0;box-sizing:border-box}
.c{position:relative;overflow:hidden;background:#180E0A;font-family:Poppins,"Noto Color Emoji",sans-serif;color:#fff;display:flex;align-items:center}
.g{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(232,87,42,.55),rgba(232,87,42,0) 62%)}
.bar{position:absolute;left:0;right:0;bottom:0;background:#E8572A}
.t{font-weight:800;line-height:1;letter-spacing:-.5px}.t span{color:#FFC94D}
.s{color:#FFE2D3;font-weight:500}
.sel{display:flex;gap:14px;flex-wrap:wrap}
.sel div{background:rgba(255,255,255,.08);border:1.5px solid rgba(255,226,211,.35);border-radius:999px;font-weight:600;color:#fff;white-space:nowrap}
.sel div b{color:#26C25A}"""
sel="<div><b>✓</b> Acesso imediato</div><div><b>✓</b> Garantia de 7 dias</div><div><b>✓</b> Compra 100% segura</div>"
D=(2200,400,f"""<style>{base}
.c{{width:2200px;height:400px;padding:0 110px;gap:60px}}.g{{width:1300px;height:1300px;left:-250px;top:-450px}}.bar{{height:12px}}
.e{{font-size:150px;position:relative}}.txt{{position:relative;flex:1}}.t{{font-size:96px}}.s{{font-size:36px;margin-top:14px}}
.sel{{position:relative;flex-direction:column;gap:16px}}.sel div{{font-size:32px;padding:12px 30px}}</style>
<div class=c><div class=g></div><div class=e>🛍️</div><div class=txt><div class=t>CLUBE DE <span>ACHADINHOS</span></div>
<div class=s>Seu acesso chega no seu e-mail logo após o pagamento</div></div><div class=sel>{sel}</div><div class=bar></div></div>""")
M=(1080,540,f"""<style>{base}
.c{{width:1080px;height:540px;flex-direction:column;justify-content:center;text-align:center;padding:0 50px}}.g{{width:1100px;height:1100px;left:-10px;top:-500px}}.bar{{height:10px}}
.e{{font-size:84px;position:relative;line-height:1;margin-bottom:10px}}.t{{font-size:80px;position:relative}}.t span{{display:block}}
.s{{font-size:31px;margin-top:16px;position:relative}}.sel{{position:relative;justify-content:center;margin-top:26px;gap:10px}}.sel div{{font-size:24px;padding:9px 18px}}</style>
<div class=c><div class=g></div><div class=e>🛍️</div><div class=t>CLUBE DE <span>ACHADINHOS</span></div>
<div class=s>Seu acesso chega no e-mail logo após o pagamento</div><div class=sel>{sel}</div><div class=bar></div></div>""")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for n,(w,h,html) in [('desktop',D),('mobile',M)]:
        pg=b.new_page(viewport={'width':w,'height':h}); pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=f'entregaveis/capas/checkout_banner_{n}_{w}x{h}.png'); pg.close()
    b.close()
