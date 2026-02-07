# 🔐 Guia de Segredos e Chaves (Secrets Guide)

Este guia centraliza todas as chaves de API, credenciais e variáveis de ambiente necessárias para operar o **Laboratório de Automação** e o **Tradutor Imersivo**.

> ⚠️ **IMPORTANTE:** Nunca comite este arquivo com chaves reais. Use `.env` ou gerenciadores de segredos. Este arquivo serve apenas como referência de *quais* chaves você precisa.

## 1. 🎮 Twitch & Clips (O Cronista)
Para a skill `tool_twitch_compiler`:
- **Arquivo:** `skills/automation_lab/tool_twitch_compiler/key.txt` (ou `.env` se refatorado)
- **Conteúdo:**
  ```text
  CLIENT_ID=seu_client_id_aqui
  CLIENT_SECRET=seu_client_secret_aqui
  ```
- **Onde obter:** [Twitch Developer Console](https://dev.twitch.tv/console)

## 2. 🧠 OpenAI / LLMs (O Cérebro)
Para skills que geram roteiros ou analisam conteúdo:
- **Variável de Ambiente:** `OPENAI_API_KEY`
- **Onde obter:** [OpenAI Platform](https://platform.openai.com/)

## 3. ☁️ Google Cloud (TTS & Vision)
Para `template_gcptts` e outras automações:
- **Arquivo:** `gcp_key.json` (caminho configurável)
- **Onde obter:** [Google Cloud Console](https://console.cloud.google.com/) -> IAM -> Service Accounts -> Create Key

## 4. 🗣️ ElevenLabs (Voz Neural)
Para narrações ultra-realistas:
- **Variável de Ambiente:** `ELEVENLABS_API_KEY`
- **Onde obter:** [ElevenLabs Profile](https://elevenlabs.io/)

## 5. 📱 Redes Sociais (Uploaders)
Para `tool_youtube_uploader` e outros:
- **Método:** Cookies (`cookies.json` ou `session` files)
- **Ferramenta Sugerida:** Extensão "EditThisCookie" para exportar sessão do navegador.
- **Caminho:** `skills/automation_lab/tool_youtube_uploader/cookies.json`

## 6. 🌐 Wikipedia & Dados Públicos
- **Chave:** Não requer chave (Acesso Público).
- **Nota:** Respeite o rate-limit (pausas entre requisições).

---

## 🛡️ Protocolo de Segurança (Revisão)
1. **Nunca** suba chaves para o GitHub.
2. Adicione `key.txt`, `.env`, `*.json` (credenciais) ao `.gitignore`.
3. Use o **Sandbox** para testar skills que pedem credenciais de alto privilégio.
