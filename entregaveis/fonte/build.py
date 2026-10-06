import markdown, sys, pathlib, base64, re
from playwright.sync_api import sync_playwright

CSS = """
@page { size: 148mm 210mm; margin: 14mm 12mm 16mm 12mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: Poppins, "Noto Color Emoji", sans-serif; color: #2A1E1A; font-size: 10.3pt; line-height: 1.46; margin: 0; }
h2 { font-weight: 800; font-size: 18pt; line-height: 1.15; color: #E8572A; margin: 0 0 10pt; letter-spacing: -.01em; }
h3 { font-weight: 800; font-size: 12.5pt; margin: 14pt 0 6pt; color: #2A1E1A; }
h4 { font-weight: 700; font-size: 11pt; margin: 12pt 0 4pt; color: #C4421A; }
p { margin: 0 0 7pt; }
ul, ol { margin: 0 0 8pt; padding-left: 16pt; }
li { margin-bottom: 3pt; }
strong, b { font-weight: 700; }
table { width: 100%; border-collapse: collapse; font-size: 8.6pt; margin: 6pt 0 8pt; page-break-inside: avoid; }
th { background: #E8572A; color: #fff; font-weight: 700; text-align: left; padding: 5pt; }
td { border-bottom: 1px solid #F1D9CC; padding: 5pt; vertical-align: top; }
tr:nth-child(even) td { background: #FFF4EC; }
.pb { page-break-after: always; break-after: page; height: 0; }
body.modular h2 { break-before: page; page-break-before: always; }
body.flow h2 { margin-top: 16pt; break-after: avoid; }
.capa + h2 { }
h3, h4 { break-after: avoid; page-break-after: avoid; }
.fim { break-before: page; page-break-before: always; }
.fim h2 { break-before: auto; page-break-before: auto; margin-top: 0; }
.formula { background: #180E0A; color: #FFE2D3; border-radius: 8pt; padding: 10pt 12pt; font-weight: 600; text-align: center; margin: 8pt 0 10pt; }
.link { background: #E8572A; color: #fff; font-weight: 800; text-align: center; border-radius: 10pt; padding: 14pt 10pt; margin: 6pt 0; font-size: 11pt; }
.box { background: #FFF1E6; border-left: 4pt solid #FFC94D; border-radius: 6pt; padding: 8pt 10pt; margin: 10pt 0; page-break-inside: avoid; }
.box p:last-child { margin: 0; }
.msg { background: #fff; border: 1px solid #F1D9CC; border-radius: 10pt 10pt 10pt 3pt; padding: 6pt 9pt; margin: 0 0 5pt; page-break-inside: avoid; font-size: 10pt; box-shadow: 0 1pt 0 #F1D9CC; }
.msg b { color: #E8572A; }
.print { border: 2px dashed #E8A07F; border-radius: 10pt; color: #B8653F; background: #FFF8F1; text-align: center; font-weight: 600; font-size: 9pt; padding: 22pt 10pt; margin: 6pt 0 10pt; page-break-inside: avoid; }
.nota { font-size: 8.4pt; color: #8a7468; }
.shot { text-align: center; margin: 6pt 0 12pt; page-break-inside: avoid; }
.shot.dupla img { width: 82%; }
.shot.media img { width: 78%; border-radius: 8pt; }
.shot img { width: 44%; border-radius: 12pt; border: 1px solid #F1D9CC; box-shadow: 0 4pt 14pt rgba(42,30,26,.18); }
.capa { break-after: page; page-break-after: always; height: 178mm; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
  background: #180E0A; color: #fff; border-radius: 12pt; padding: 20pt; margin: -2mm -2mm 0; }
.capa .selo { font-weight: 700; letter-spacing: 4pt; font-size: 8.5pt; color: #FFC94D; margin-bottom: 14pt; }
.capa .titulo { font-weight: 800; font-size: 34pt; line-height: 1; }
.capa .titulo span { color: #FFC94D; }
.capa .sub { font-size: 11pt; margin: 18pt 10pt 8pt; color: #FFE2D3; }
.capa .lojas { font-size: 9pt; color: #E8A07F; letter-spacing: 1pt; }
.capa .icone { font-size: 46pt; margin-bottom: 8pt; }
.fim { text-align: center; padding-top: 40mm; }
.fim h2 { font-size: 22pt; }
.assin { font-weight: 700; color: #E8572A; margin-top: 20pt; }
"""

def build(src, out, title, mode='modular'):
    md = pathlib.Path(src).read_text(encoding='utf-8')
    body = markdown.markdown(md, extensions=['md_in_html', 'tables'])
    base = pathlib.Path(src).parent / 'prints'
    body = re.sub(r'PRINT:([\w.-]+)', lambda m: 'data:image/png;base64,' + base64.b64encode((base / m.group(1)).read_bytes()).decode(), body)
    html = f"<!doctype html><html lang=pt-BR><head><meta charset=utf-8><title>{title}</title><style>{CSS}</style></head><body class={mode}>{body}</body></html>"
    pathlib.Path(out).with_suffix('.html').write_text(html, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page()
        pg.set_content(html, wait_until='load'); pg.wait_for_timeout(300)
        pg.pdf(path=out, prefer_css_page_size=True, print_background=True,
               display_header_footer=True, header_template='<span></span>',
               footer_template='<div style="width:100%;text-align:center;font-family:Poppins;font-size:7pt;color:#b39a8c"><span class="pageNumber"></span></div>')
        b.close()

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv)>4 else 'modular')
