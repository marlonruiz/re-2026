from playwright.sync_api import sync_playwright
C=[('01_capa_Clube-de-Achadinhos','GUIA COMPLETO','CLUBE DE','ACHADINHOS','Indique e receba por cada compra','🛍️','#180E0A','#FFC94D'),
   ('02_capa_Kit-Black-Friday','BÔNUS','KIT BLACK','FRIDAY','30 mensagens prontas','🖤','#0E0E10','#FFC94D'),
   ('03_capa_Revenda-no-Bairro','BÔNUS','REVENDA','NO BAIRRO','Compre barato, revenda perto','🏘️','#180E0A','#FFC94D'),
   ('04_capa_Achadinhos-ate-o-Natal','ACESSO ATÉ 25/12','ACHADINHOS','ATÉ O NATAL','5 achadinhos prontos, 2x por semana','🎄','#0F2A1C','#FFC94D')]
css="""*{margin:0;padding:0;box-sizing:border-box}html,body{width:300px;height:250px}
.c{width:300px;height:250px;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:Poppins,"Noto Color Emoji",sans-serif;color:#fff}
.c:before{content:"";position:absolute;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(232,87,42,.55),rgba(232,87,42,0) 65%);top:-60px;left:-20px}
.c:after{content:"";position:absolute;left:0;right:0;bottom:0;height:8px;background:#E8572A}
.e{font-size:38px;line-height:1;margin-bottom:6px;position:relative}
.k{font-weight:700;font-size:10px;letter-spacing:3px;color:#FFE2D3;position:relative;margin-bottom:6px}
.t1{font-weight:800;font-size:28px;line-height:1;position:relative}
.t2{font-weight:800;font-size:31px;line-height:1.02;position:relative}
.s{position:relative;margin-top:10px;font-size:11.5px;font-weight:600;background:#E8572A;padding:5px 12px;border-radius:999px}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for scale,suf in [(1,''),(2,'@2x')]:
        pg=b.new_page(viewport={'width':300,'height':250},device_scale_factor=scale)
        for n,k,t1,t2,s,e,bg,acc in C:
            pg.set_content(f"<style>{css}</style><div class=c style='background:{bg}'><div class=e>{e}</div><div class=k>{k}</div><div class=t1>{t1}</div><div class=t2 style='color:{acc}'>{t2}</div><div class=s>{s}</div></div>")
            pg.wait_for_timeout(150); pg.screenshot(path=f'{n}{suf}.png')
    b.close()
