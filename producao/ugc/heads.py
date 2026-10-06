from playwright.sync_api import sync_playwright
H={'A':'você manda link de graça<br>pra todo mundo? 😅',
   'B':'o que ninguém fala<br>sobre a Shopee 🤫',
   'C':'antes da Black Friday,<br>faz isso 👇'}
css="""*{margin:0;padding:0} html,body{width:1080px;height:420px;background:transparent}
.w{position:absolute;top:150px;left:0;right:0;display:flex;justify-content:center}
.t{background:#fff;color:#111;font:600 50px/1.25 Poppins,"Noto Color Emoji",sans-serif;padding:18px 34px;border-radius:22px;text-align:center;box-shadow:0 6px 24px rgba(0,0,0,.25)}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg=b.new_page(viewport={'width':1080,'height':420})
    for k,v in H.items():
        pg.set_content(f"<style>{css}</style><div class=w><div class=t>{v}</div></div>"); pg.wait_for_timeout(150)
        pg.screenshot(path=f'/root/ads/ugc/head{k}.png',omit_background=True)
    b.close()
