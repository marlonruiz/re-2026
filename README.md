# Renda Extra 2026 · Clube de Achadinhos

Produto low ticket de renda extra para mulheres 30+, vendido por tráfego pago na Meta e checkout na Cakto. Domínio: clubedeachadinhos.online.

## Pastas

| Pasta | O que tem |
|---|---|
| `descritivo-projeto.md` | Base do projeto: decisões, público, regras |
| `perfil-publico-mulheres-35-renda-extra.md` | Perfil do público |
| `levantamento-anuncios-meta-out2026.md` | Pesquisa na Biblioteca de Anúncios |
| `roteiros-vsl-e-anuncios.md` | Oferta, preços, roteiros da VSL e dos anúncios, textos e títulos |
| `pagina/` | Página de vendas (`index.html`, `vsl.mp4`, `vsl-capa.jpg`). Subir os três arquivos juntos na hospedagem |
| `videos/` | VSL final em alta |
| `anuncios/` | 6 criativos (A, B, C em versão motion e UGC), avatares e vozes |
| `entregaveis/` | PDFs para a Cakto, capas 300x250 e textos-fonte (`fonte/`) |
| `audio/`, `avatar/` | Voz e avatar da VSL |
| `producao/` | Código usado para gerar vídeos, PDFs e capas (Remotion, Python) |

## Antes de publicar a página

No topo do `pagina/index.html`, no bloco `CONFIG`:
- `checkoutUrl`: link do checkout da Cakto
- `delaySeconds`: segundo da VSL em que o botão aparece (82)

E colar o código do pixel da Meta onde está indicado.

## Pendências

- Prints do cadastro nas lojas para os 7 espaços "COLE AQUI O PRINT" do guia
- Link do canal do WhatsApp no PDF do upsell
- Primeiro lote do upsell (achadinhos de outubro)

## Regerar os PDFs

```
pip install markdown playwright pypdf
python entregaveis/fonte/build.py entregaveis/fonte/guia.md guia.pdf "Clube de Achadinhos" modular
```
(Os bônus usam o modo `flow`.)
