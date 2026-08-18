# 2026-08-18 — case-study-local (14h ET) — parou no PASSO 2, Instagram desconectado no Metricool

**O que foi feito antes de parar:**
- STEP 0 (git pull) OK nos dois repos (`creatorup`, `hustlestack-site`), ambos já atualizados.
- STEP 1 (leitura das regras) OK: `CLAUDE.md` raiz completo, seção "CASE STUDY FORMAT" de
  `creatorup-gerar-carrossel-en/SKILL.md`, e as subseções "Como baixar as fotos" /
  "Escolha de foto por slide" de `creatorup-gerar-carrossel/SKILL.md`.
- STEP 2 (checar duplicata via `getScheduledPosts`, blogId `6566436`): **diferente de 08-16, a
  ferramenta Metricool está disponível e respondeu normalmente** — não é o bug de token OAuth já
  documentado ("Metricool MCP some nas execuções não interativas").

**Onde parou e por quê:** `getScheduledPosts` (blogId `6566436`, hoje, `America/New_York`) mostra
os dois posts já agendados hoje com status `ERROR`:
- 09:08 ET (`aiavatar`/`tiktokshop`, formato "curso principal"): `ERROR`, `detailedStatus: "Unknown."`
- 10:09 ET (tactic format, "content calendar"): `ERROR`, `detailedStatus: "Instagram was
  disconnected"`

Cruzando com `getBrandSettings`: o brand `hustlestackhq` (id `6566436`) tem
`"networksData": {}` — **nenhuma rede social conectada**, diferente da Creator Up (`6553817`) e do
Marcos Moraes (`6577352`), que mostram `instagramData` normalmente preenchido. Olhando o histórico
de 15 a 18/08, a última publicação bem-sucedida foi o case study de ontem (Dollar Shave Club,
19:20 ET, `PUBLISHED`, `instagram.com/p/DcKNQnnClIx`) — ou seja, o Instagram do HustleStack
desconectou dentro do Metricool em algum momento entre 17/08 19:20 ET e 18/08 09:08 ET.

**Isso é diferente do bug de token OAuth do conector já documentado no `CLAUDE.md`** (esse faz a
ferramenta MCP sumir da lista inteira, sem erro visível). Aqui a ferramenta funciona normal — é a
conexão da rede social dentro da própria conta Metricool que caiu, um problema de nível de conta,
não de sessão/harness.

**Por que parei aqui em vez de continuar:** publicar hoje vai falhar de qualquer forma enquanto o
Instagram estiver desconectado — os dois posts de hoje já provam isso. Pesquisar um case novo e
gerar as 8-10 imagens sem conseguir publicar no final desperdiçaria o trabalho sem nenhum ganho, e
arriscaria "queimar" um case bom que teria que ser reaproveitado depois sem estar mais tão
atual/verificado. Melhor parar cedo, deixar rastro claro, e avisar o usuário — só ele consegue
reconectar a rede.

**Ação necessária, só o usuário consegue fazer:** abrir o Metricool (app ou metricool.com) →
marca `hustlestackhq` → Configurações/redes conectadas → reconectar o Instagram (provavelmente
pede login/autorização do Instagram de novo, igual conectar pela primeira vez). Depois de
reconectar, os posts de hoje que já estão em `ERROR` (09:08 e 10:09 ET) provavelmente precisam ser
reagendados/republicados manualmente — o Metricool normalmente não tenta de novo sozinho um post
que já falhou.

**Nenhuma pesquisa de case, foto ou imagem foi gerada nesta execução** — parou no passo de
checagem, antes de qualquer trabalho de conteúdo.
