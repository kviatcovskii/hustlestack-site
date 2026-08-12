# Case study format — instructions (self-contained copy, 2026-08-12)

This file exists so the `hustlestack-carrossel-case-14h-et` RemoteTrigger never needs to read the
private `creatorup-carrosseis-automation` repo from the cloud again — that repo is not reachable
from this trigger's session (`sources` scope only includes `hustlestack-site`, and declaring the
automation repo via `sources` was already tried and rejected with 403 at trigger creation time).
This is a copy of the relevant rules from that repo's `SKILL.md` files, kept here so everything the
trigger needs lives inside a repo it can already read and write. If you're editing the master copy
in `creatorup-carrosseis-automation`, remember to sync meaningful changes here too — there is no
automatic sync between the two.

## Format spec (from `creatorup-gerar-carrossel-en/SKILL.md`, "CASE STUDY FORMAT")

A real, researched marketing case study (Liquid Death, Duolingo, that kind of thing), told in 7-10
slides, that **never sells anything**.

- **Never mentions a HustleStack product, never says "link in bio."** If it reads like an ad, it
  defeats the purpose.
- **Structure** (`generate_case_study.py`, imports `render_case_cover`, `render_story_slide`,
  `render_case_outro` from `generate_template.py`, both in this same folder):
  1. **Cover** (`render_case_cover`) — real photo of the brand/founder/scene up top, dark panel
     below with an editorial serif headline, key phrase gold-boxed. Ends with "swipe for the
     story" + arrow, no comment CTA.
  2. **Story** (`render_story_slide`, 5-7 slides) — the case in real depth, each slide with its
     OWN support photo matching what THAT slide specifically says (never a generic/repeated photo
     unless genuinely no alternative exists).
  3. **Lesson** (`render_story_slide` again, second-to-last) — an explicit marketing-specific
     lesson ("The marketing lesson here is: ..."), never a legal/ownership/general-business one.
  4. **Outro** (`render_case_outro`) — plain ivory background, gold tagline + "Follow for the
     next one." + handle.
- **Instagram only** — HustleStack's Metricool brand has no TikTok connected, so there's no
  PNG/JPG-per-network split to manage (unlike the Creator Up version). The `.jpg` siblings the
  functions still emit are harmless unused spares.
- Cases must be genuinely different from what's already run — check `carousels/case-study/*/` in
  this repo (`hustlestack-site`) before picking one.
- No em dash, no emoji, short sentences, AIDA-ish hook energy.

## Photo sourcing (from `creatorup-gerar-carrossel/SKILL.md`, "Como baixar as fotos" +
"Escolha de foto por slide" — brand-agnostic, written in Portuguese originally, kept as-is)

**Ordem de tentativa a cada execução — teste o domínio de controle PRIMEIRO:**

1. Teste conectividade geral: `curl -s -o /dev/null -w "%{http_code}" --max-time 8 https://www.google.com`.
   Se NÃO vier `200`, é bloqueio geral do ambiente — pare e reporte, não invente um terceiro método.
2. Teste Openverse: `curl -s -o /dev/null -w "%{http_code}" --max-time 8 https://api.openverse.org/v1/images/?q=test`.
   Se vier `200`, use Openverse.
3. Busca no Openverse:
   `curl -s "https://api.openverse.org/v1/images/?q=<termo>&license_type=commercial,modification&page_size=10"`.
   Licenças permitidas: qualquer uma com `commercial,modification` no filtro (nunca NC-only ou
   ND-only). **Prefira sempre o proxy do próprio Openverse pra baixar, não a `url` direta** — o
   Flickr (fonte da maioria dos resultados) costuma estar bloqueado mesmo com a API funcionando:
   ```
   curl -sL -o foto.jpg "https://api.openverse.org/v1/images/<id>/thumb/?full_size=true"
   ```
   Sem `full_size=true` vem miniatura de 600px (baixa demais); com ele vem a resolução original.
4. Wikimedia Commons (só se Openverse falhou ou não achou fotos suficientes):
   teste `https://commons.wikimedia.org/w/api.php?action=query&format=json` primeiro, depois
   `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=<termo>&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata&format=json&gsrlimit=10`.
   Confira `extmetadata.LicenseShortName` — só CC0/CC-BY/CC-BY-SA/Public Domain, nunca NC/ND.
   Baixe com `User-Agent` identificável e ~2-3s entre downloads (rate limit real, já bateu nisso
   antes) — `curl -s -A "HustleStackBot/1.0 (contato)" -o <arquivo> "<url>"` + `sleep 2`. **Sempre
   valide cada arquivo com PIL (`Image.open(...).size`)** antes de usar — arquivo de poucos KB que
   falha ao abrir é quase sempre página de erro salva no lugar da foto.
5. Se tudo falhar: pare e reporte claramente que o ambiente de rede bloqueou hoje — isso é
   resultado esperado em dia ruim de rede, não é falha da rotina.

**Uma foto DIFERENTE por slide** (capa + cada slide de história + lição) — nunca repita a mesma
foto em dois slides.

**Escolha de foto por slide — casar com o texto, não só "estádio/prédio genérico":**
- A foto de cada slide precisa ilustrar literalmente o que aquele slide específico fala, não só o
  tema geral do case (ex.: slide sobre dinheiro/patrocínio → foto que evoque isso visualmente, não
  uma foto neutra qualquer).
- Nunca use foto com data/ano visível que contradiga o ano do case — corte pra tirar o texto, ou
  troque de foto.
- Nunca use foto com marca de TERCEIRO em destaque no enquadramento (logo grande de outra empresa
  no fundo) — corte pra tirar, ou troque de foto.
- **Sempre abra e olhe cada foto baixada antes de usar** — nome de arquivo e resultado de busca
  mentem com frequência (já aconteceu foto chamada "Mountain bike jump" que era rampa vazia sem
  ciclista nenhum). Validar só com PIL detecta arquivo corrompido, não detecta foto errada.
- Pré-corte com PIL antes de passar pro script sempre que o elemento importante (rosto, letreiro,
  marca) não estiver nos ~60% superiores da foto original — o crop automático (`_cover_crop`,
  `vertical_bias=0.25`) reduz mas não elimina o corte ruim em fotos descentralizadas.
- Headshot de imprensa muito fechado (proporção largura/altura < ~0.8) ainda corta queixo/boca
  mesmo com o rosto nos 50% superiores — pré-corte removendo uma fatia do topo, ou prefira plano
  mais aberto (corpo inteiro, evento, bastidor).

## Meta account restriction (from `creatorup-estrategia-engajamento-hustlestack/SKILL.md`,
"RECURRING META ACCOUNT RESTRICTION")

Since 2026-07-26, `@hustlestackhq`'s Instagram provider has repeatedly returned this error on
`createScheduledPost` attempts: **"We restrict certain activity to protect our community. Tell us
if you think we made a mistake."** — account-level, not tied to a specific image/caption.

**Standing rule for all 3 HustleStack RemoteTrigger routines (10am/2pm/7pm ET):** before calling
`createScheduledPost` with `autoPublish: true`, call `getScheduledPosts` for today's window first.
If any earlier post today already shows Instagram `status: "ERROR"` with this specific message, do
NOT attempt another live publish in the same window — create the new post as `draft: true,
autoPublish: false` instead, confirm via `getScheduledPosts` that it landed as `PENDING`/draft (not
`ERROR`, not duplicate), and log it. Forcing a third live attempt in the same restricted window has
never once succeeded when tried and risks worsening the flag.
