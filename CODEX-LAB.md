# Codex Lab — regras obrigatórias

Esta branch pertence ao laboratório isolado do Codex.

## Segurança

- Nunca editar, publicar, fazer push ou merge diretamente na `main`.
- Todo trabalho do Codex deve permanecer em branches com prefixo `codex/`.
- Não abrir ou mesclar pull request sem aprovação explícita do usuário.
- Higgsfield está bloqueado: não gerar imagem, vídeo ou áudio e não consumir créditos.
- Publicações externas começam em dry-run. Não publicar nem agendar posts reais antes da aprovação explícita do usuário.
- Não alterar as rotinas Claude/produção nem o Agendador do Windows durante os testes.
- Não copiar tokens, cookies, PATs ou outras credenciais para arquivos ou commits.

## Testes

- Testar primeiro operações somente de leitura.
- Registrar duração, uso/créditos, resultado e erros.
- Só liberar uma ação externa depois de validar seu cancelamento ou reversão.
- Metricool deve usar o MCP oficial e ser validado antes de qualquer agendamento.

Se outra IA continuar este trabalho, deve ler este arquivo antes de executar qualquer mutação.
