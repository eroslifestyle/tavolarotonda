# TODO — tavolarotonda-due

## Attivo
- [ ] Eseguire un vero turno di roundtable `claude-cli-oauth` + `codex-cli-oauth` su un topic reale (es. CRAM Plugin) nel flow debate/GUI vero — i due provider hanno passato solo lo smoke test "PONG"
- [ ] Monitorare stabilità symlink `~/.local/bin/codex` (pinnato al binario alpha dell'estensione VSCode "ChatGPT": si rompe se disinstallata o aggiornata incompatibilmente)
- [ ] Decidere se committare/gestire `graphify-out/` (5 file auto-generati dall'hook post-commit, non committati)

## Completati
- [x] [2026-09-12] Trovato `~/.codex/auth.json` già autenticato (OAuth); binario `codex` introvabile in PATH — era dentro l'estensione VSCode "ChatGPT" (`~/.vscode/extensions/openai.chatgpt-26.908.40401-linux-x64/bin/linux-x86_64/codex`, codex-cli 0.154.0-alpha.6.2), installata lo stesso giorno
- [x] [2026-09-12] Creato symlink `~/.local/bin/codex` → binario estensione; `codex --version` verificato funzionante
- [x] [2026-09-12] Verificato formato output CLI non-interattive: `claude -p "..." --output-format json` → JSON campo `"result"`; `codex exec "..." -s read-only --skip-git-repo-check -o <file>` → testo puro su file
- [x] [2026-09-12] Letto pattern reale `tavolarotonda/providers.py`: `async complete(..., provider_kind, model_tier) -> ProviderResult`, switch su `provider_kind`, ogni backend metodo `_nome(...) -> str` che solleva eccezione su errore
- [x] [2026-09-12] Implementati provider CLI (subagent coder, verificato con git diff + test): `providers.py` (import tempfile, `ProviderKind` + `"claude_cli"`/`"codex_cli"`, metodi `_claude_cli`/`_codex_cli` subprocess asyncio con permission-mode "plan" / sandbox "read-only", sottoclassi `ClaudeCliProvider`/`CodexCliProvider`); `config.yaml` (voci `claude-cli-oauth`, `codex-cli-oauth`, `env_required: []`); aggancio in `debate.py` `_make_provider` e `gui/app.py` (`_build_provider` + `/api/models`)
- [x] [2026-09-12] Test end-to-end reale: `LLMProvider().complete(..., provider_kind="claude_cli")` → `'PONG'`, stesso per `codex_cli` → `'PONG'`
- [x] [2026-09-12] Commit `d227434` "feat: provider CLI OAuth (claude_cli, codex_cli)" — 10 file, non pushato
