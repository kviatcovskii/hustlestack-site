# 2026-08-16 — case-study-local (14h ET) — parou no PASSO 2, Metricool ausente

**O que foi feito antes de parar:**
- STEP 0 (git pull) OK nos dois repos (`creatorup`, `hustlestack-site`), ambos já atualizados.
- STEP 1 (leitura das regras) OK: `CLAUDE.md` raiz completo, seção "CASE STUDY FORMAT" de
  `creatorup-gerar-carrossel-en/SKILL.md`, e as subseções "Como baixar as fotos" /
  "Escolha de foto por slide" de `creatorup-gerar-carrossel/SKILL.md`.

**Onde parou:** STEP 2 (checar duplicata via `mcp__claude_ai_Metricool__getScheduledPosts`,
blogId `6566436`). A ferramenta Metricool não apareceu na lista de ferramentas disponíveis nesta
sessão headless — confirmado com duas buscas via `ToolSearch` (queries `"getScheduledPosts
Metricool"` e `"Metricool"`), nenhuma retornou o servidor. O reminder do sistema também listou
`claude.ai Metricool` entre os "MCP servers require authentication before their tools can be
used... This session is non-interactive, so Claude cannot run the OAuth flow here."

**Causa raiz:** já documentada no `CLAUDE.md` raiz, seção "Metricool MCP some nas execuções não
interativas — 2026-08-04". O token OAuth do conector Metricool expira para sessões não
interativas; uma sessão interativa consegue renovar sozinha (mascarando o problema), a headless
não consegue, e o harness remove o servidor da lista de ferramentas em vez de reportar erro
visível. Já tinha recorrido em 2026-08-10 (4 dias de silêncio nos formatos das 09h/12h/15h da
Creator Up). Esta é uma nova recorrência, agora atingindo a rotina local do case study do
HustleStack (14h ET).

**Por que parei aqui em vez de continuar:** sem `getScheduledPosts`, não dá pra confirmar se já
existe um post de hoje (evitando duplicata) nem, mais adiante, publicar de verdade ou confirmar
`PUBLISHED`/`PENDING` sem `ERROR`. Pesquisar o case e gerar as imagens sem conseguir publicar no
final desperdiçaria o trabalho sem nenhum ganho — melhor parar cedo e deixar rastro claro.

**Ação necessária, só o usuário consegue fazer:** reautorizar o conector Metricool
(`claude` → `/mcp` → `claude.ai Metricool` → reconectar, OU claude.ai → Settings → Connectors →
Metricool → desconectar/reconectar), depois validar em modo headless antes de confiar
(`claude -p "Use ToolSearch pra procurar getScheduledPosts do Metricool. Responda so SIM ou
NAO."`).

**Nenhuma pesquisa de case, foto ou imagem foi gerada nesta execução** — parou no passo de
checagem, antes de qualquer trabalho de conteúdo.
