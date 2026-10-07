from playwright.sync_api import sync_playwright
C=[('01_cover_Clube-de-Achadinhos','GUIA COMPLETO','CLUBE DE','ACHADINHOS','Indique e receba por cada compra','🛍️','#180E0A'),
   ('02_cover_Kit-Black-Friday','BÔNUS','KIT BLACK','FRIDAY','30 mensagens prontas','🖤','#0E0E10'),
   ('03_cover_Revenda-no-Bairro','BÔNUS','REVENDA','NO BAIRRO','Compre barato, revenda perto','🏘️','#180E0A'),
   ('04_cover_Achadinhos-ate-o-Natal','ACESSO ATÉ 25/12','ACHADINHOS','ATÉ O NATAL','5 achadinhos prontos, 2x por semana','🎄','#0F2A1C')]
css="""*{margin:0;padding:0;box-sizing:border-box}html,body{width:200px;height:300px}
.c{width:200px;height:300px;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:Poppins,"Noto Color Emoji",sans-serif;color:#fff;padding:0 12px}
.c:before{content:"";position:absolute;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(232,87,42,.55),rgba(232,87,42,0) 65%);top:-70px;left:-60px}
.c:after{content:"";position:absolute;left:0;right:0;bottom:0;height:8px;background:#E8572A}
.e{font-size:46px;line-height:1;margin-bottom:12px;position:relative}
.k{font-weight:700;font-size:9px;letter-spacing:2.5px;color:#FFE2D3;position:relative;margin-bottom:8px}
.t1{font-weight:800;font-size:23px;line-height:1.02;position:relative}
.t2{font-weight:800;font-size:24px;line-height:1.02;position:relative;color:#FFC94D}
.s{position:relative;margin-top:14px;font-size:10.5px;font-weight:600;line-height:1.25;background:#E8572A;padding:6px 10px;border-radius:12px;max-width:170px}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for scale,suf in [(1,''),(2,'@2x')]:
        pg=b.new_page(viewport={'width':200,'height':300},device_scale_factor=scale)
        for n,k,t1,t2,s,e,bg in C:
            pg.set_content(f"<style>{css}</style><div class=c style='background:{bg}'><div class=e>{e}</div><div class=k>{k}</div><div class=t1>{t1}</div><div class=t2>{t2}</div><div class=s>{s}</div></div>")
            pg.wait_for_timeout(150); pg.screenshot(path=f'entregaveis/capas/{n}{suf}.png')
    b.close()
