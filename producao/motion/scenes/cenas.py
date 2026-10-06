from playwright.sync_api import sync_playwright
CSS = """
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;font-family:Poppins,"Noto Color Emoji",sans-serif;color:#fff}
.wrap{position:absolute;left:0;right:0;top:300px;height:980px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px}
.kicker{font-weight:700;font-size:38px;letter-spacing:6px;color:#FFC94D}
.h{font-weight:800;font-size:78px;line-height:1.08;text-align:center;text-transform:uppercase;text-shadow:0 6px 0 #000}
.h em{font-style:normal;background:#E8572A;padding:0 16px;border-radius:14px}
.chat{width:860px;background:#FFF8F1;border-radius:34px;padding:26px 30px;color:#2A1E1A;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.chat .top{display:flex;align-items:center;gap:18px;margin-bottom:16px}
.av{width:62px;height:62px;border-radius:31px;display:grid;place-items:center;font-size:34px;font-weight:800;color:#fff}
.nm{font-weight:700;font-size:34px} .sub{font-size:24px;color:#8a7468}
.b{display:inline-block;background:#fff;border-radius:22px 22px 22px 6px;padding:16px 24px;font-size:36px;line-height:1.25;box-shadow:0 2px 0 rgba(0,0,0,.08)}
.me{display:flex;justify-content:flex-end;margin-top:12px} .me .b{background:#FFE2D3;border-radius:22px 22px 6px 22px}
.tile{width:820px;padding:34px 40px;border-radius:30px;background:#FFF8F1;color:#2A1E1A;font-weight:800;font-size:66px;text-align:center;letter-spacing:1px;box-shadow:0 0 0 4px #FFC94D,0 18px 40px rgba(0,0,0,.45)}
.row{width:880px;display:flex;align-items:center;gap:26px;background:rgba(255,248,241,.96);color:#2A1E1A;border-radius:28px;padding:26px 34px;font-size:44px;font-weight:700;box-shadow:0 14px 34px rgba(0,0,0,.4)}
.ic{width:74px;height:74px;border-radius:37px;display:grid;place-items:center;font-size:42px;flex:none;color:#fff;font-weight:800}
.cal{width:430px;border-radius:30px;overflow:hidden;background:#FFF8F1;color:#2A1E1A;text-align:center;box-shadow:0 18px 40px rgba(0,0,0,.45)}
.cal .t{background:#E8572A;color:#fff;font-weight:800;font-size:40px;padding:18px} .cal .d{font-weight:800;font-size:150px;line-height:1.1;padding:10px 0 0}
.cal .m{font-weight:700;font-size:42px;padding-bottom:26px;color:#8a7468}
.logo{font-weight:800;text-align:center;line-height:.95}
"""
S = {
'cena-conversas': """<div class=wrap>
 <div class=chat><div class=top><div class=av style="background:#E8572A">J</div><div><div class=nm>Ju (amiga)</div><div class=sub>online</div></div></div>
  <div class=b>Ameeei essa panela 😍 onde você comprou??</div><div class=me><div class=b>Te mando o link!</div></div></div>
 <div class=chat><div class=top><div class=av style="background:#3A7D5C">💼</div><div><div class=nm>Pessoal do trabalho</div><div class=sub>Carla, Rô, Bia e mais 9</div></div></div>
  <div class=b>Gente, alguém indica um organizador bom e barato?</div></div>
 <div class=chat><div class=top><div class=av style="background:#C4421A">🎒</div><div><div class=nm>Mães da escola</div><div class=sub>Paula, Dani e mais 21</div></div></div>
  <div class=b>Onde vocês compram as coisas de Natal?</div></div>
</div>""",
'cena-lojas': """<div class=wrap><div class=kicker>ESSAS LOJAS PAGAM POR INDICAÇÃO</div>
 <div class=tile>SHOPEE</div><div class=tile>MERCADO LIVRE</div><div class=tile>AMAZON</div></div>""",
'cena-sem': """<div class=wrap>
 <div class=row><div class=ic style="background:#C4421A">✕</div>Não vende nada</div>
 <div class=row><div class=ic style="background:#C4421A">✕</div>Não tem estoque</div>
 <div class=row><div class=ic style="background:#C4421A">✕</div>Não entrega nada</div>
 <div class=row style="background:#FFC94D"><div class=ic style="background:#1F8A4C">✓</div>Só indica, do celular</div></div>""",
'cena-logo': """<div class=wrap><div class=kicker>APRESENTANDO</div>
 <div class=logo><div style="font-size:120px">🛍️</div><div style="font-size:110px">CLUBE DE</div><div style="font-size:126px;color:#FFC94D">ACHADINHOS</div></div>
 <div style="font-size:42px;font-weight:600;color:#FFE2D3">passo a passo pelo celular</div></div>""",
'cena-modulos': """<div class=wrap><div class=kicker>O QUE VOCÊ RECEBE</div>
 <div class=row><div class=ic style="background:#1F8A4C">✓</div>Suas contas criadas em 10 min</div>
 <div class=row><div class=ic style="background:#1F8A4C">✓</div>Os achadinhos que mais vendem</div>
 <div class=row><div class=ic style="background:#1F8A4C">✓</div>Como indicar sem parecer chata</div>
 <div class=row style="background:#FFC94D"><div class=ic style="background:#E8572A">60</div>Mensagens prontas</div></div>""",
'cena-rotina': """<div class=wrap><div class=kicker>NO SEU TEMPO</div>
 <div class=row><div class=ic style="background:#E8572A">☕</div>No intervalo do dia</div>
 <div class=row><div class=ic style="background:#3A4A7D">🌙</div>Enquanto as crianças dormem</div>
 <div class=row><div class=ic style="background:#3A7D5C">🛒</div>Na fila do mercado</div></div>""",
'cena-calendario': """<div class=wrap><div class=kicker>A MELHOR ÉPOCA DO ANO</div>
 <div style="display:flex;gap:40px"><div class=cal><div class=t>BLACK FRIDAY</div><div class=d>27</div><div class=m>novembro</div></div>
 <div class=cal><div class=t style="background:#3A7D5C">NATAL</div><div class=d>25</div><div class=m>dezembro</div></div></div>
 <div class=h style="font-size:62px">Os meses que <em>mais se compra</em> presente</div></div>""",
'logo-outro': """<div class=wrap style="top:0;height:1920px"><div class=logo><div style="font-size:130px">🛍️</div><div style="font-size:110px">CLUBE DE</div><div style="font-size:126px;color:#FFC94D">ACHADINHOS</div></div></div>""",
}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    p = b.new_page(viewport={'width':1080,'height':1920})
    for k,v in S.items():
        p.set_content(f"<style>{CSS}</style>{v}"); p.wait_for_timeout(200)
        p.screenshot(path=f'/root/motion/public/assets/{k}.png', omit_background=True)
    b.close()
print('ok')
