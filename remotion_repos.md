# Repositórios e Recursos para Remotion

Aqui está uma lista expandida e curada de repositórios públicos no GitHub e recursos externos (MCPs, Skills) relacionados ao **Remotion** (https://www.remotion.dev/), organizados por categoria.

## 🧠 Skills de Agentes & Model Context Protocol (MCP)

Ferramentas essenciais para integrar Remotion com assistentes de IA (Claude, Cursor, Windsurf).

*   **[remotion-dev/skills](https://github.com/remotion-dev/skills)**
    *   **Tipo:** Agent Skills Oficiais
    *   **Comando:** `npx skills add remotion-dev/skills`
    *   **Descrição:** Ensina ao agente (Claude Code, Cursor) as melhores práticas, arquitetura de componentes e APIs de animação do Remotion. Essencial para gerar código correto.

*   **[Remotion Documentation MCP](https://www.remotion.dev/docs/ai/mcp)**
    *   **Tipo:** Servidor MCP Oficial
    *   **Instalação (Claude Desktop/Cursor):**
        ```json
        {
          "mcpServers": {
            "remotion-documentation": {
              "command": "npx",
              "args": ["@remotion/mcp@latest"]
            }
          }
        }
        ```
    *   **Descrição:** Permite que o assistente consulte a documentação oficial do Remotion em tempo real, garantindo respostas atualizadas.

*   **[stephengpope/remotion-media-mcp](https://github.com/stephengpope/remotion-media-mcp)**
    *   **Tipo:** Servidor MCP Comunitário
    *   **Descrição:** Servidor MCP para gerar mídia (imagens, vídeos, música) dinamicamente dentro de projetos Remotion. Ideal para agentes autônomos.

## 🌟 Destaques Oficiais (Remotion Team)

Repositórios mantidos pela equipe oficial, garantindo qualidade e atualização.

*   **[remotion-dev/remotion](https://github.com/remotion-dev/remotion)**
    *   **Descrição:** Repositório principal do framework.
    *   **Uso:** Referência técnica e contribuição.

*   **[remotion-dev/template-helloworld](https://github.com/remotion-dev/template-helloworld)**
    *   **Descrição:** Template minimalista.
    *   **Ideal para:** Projetos limpos, sem excesso de configurações.

*   **[remotion-dev/template-skia](https://github.com/remotion-dev/template-skia)**
    *   **Descrição:** Configurado com `@shopify/react-native-skia`.
    *   **Ideal para:** Gráficos 2D de alta performance.

*   **[remotion-dev/template-prompt-to-motion-graphics](https://github.com/remotion-dev/template-prompt-to-motion-graphics)**
    *   **Descrição:** IA para transformar prompts de texto em código Remotion.
    *   **Ideal para:** Automação via IA.

*   **[remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok)**
    *   **Descrição:** Gera legendas estilo TikTok usando **Whisper.cpp**.
    *   **Ideal para:** Automação de vídeos verticais com legendas.

*   **[remotion-dev/github-unwrapped](https://github.com/remotion-dev/github-unwrapped)**
    *   **Descrição:** Código do vídeo "GitHub Unwrapped".
    *   **Ideal para:** Exemplos complexos baseados em dados (data-driven).

*   **[remotion-dev/template-music-visualization](https://github.com/remotion-dev/template-music-visualization)**
    *   **Descrição:** Visualizadores de música sincronizados com áudio.
    *   **Ideal para:** Clipes musicais e podcasts.

## 🤖 Integrações com IA e Automação

Projetos que combinam Remotion com LLMs (GPT, Claude), TTS e APIs de vídeo.

*   **[gyoridavid/short-video-maker](https://github.com/gyoridavid/short-video-maker)**
    *   **Descrição:** Ferramenta completa para criar Shorts/TikToks a partir de texto.
    *   **Stack:** Remotion, **Whisper** (legendas), **Kokoro** (TTS), **Pexels** (vídeo de fundo).
    *   **Destaque:** Funciona como servidor MCP e API REST.

*   **[MoJuBaGod/Claude-x-Remotion](https://github.com/MoJuBaGod/Claude-x-Remotion)**
    *   **Descrição:** Starter kit para criar vídeos programaticamente com **Claude Code**.
    *   **Destaque:** Componentes prontos para uso com assistentes de IA.

## 🚀 SaaS e Plataformas

Exemplos de como construir produtos (SaaS) usando Remotion.

*   **[remotion-dev/template-react-router](https://github.com/remotion-dev/template-remix)**
    *   **Descrição:** Template SaaS usando React Router 7 + Remotion Lambda.
    *   **Ideal para:** Criar plataformas de renderização de vídeo na nuvem.

*   **[scastiel/github-stars-video](https://github.com/scastiel/github-stars-video)**
    *   **Descrição:** Gera vídeos celebrando milestones de estrelas no GitHub.
    *   **Ideal para:** Exemplo prático de "Video as a Service".

## 🎨 Criatividade e Clones

Recriações de interfaces famosas e efeitos visuais.

*   **[JonnyBurger/remotion-wrapped](https://github.com/JonnyBurger/remotion-wrapped)**
    *   **Descrição:** Recriação do **Spotify Wrapped**.
    *   **Ideal para:** Aprender a fazer vídeos personalizados baseados em estatísticas.

*   **[satelllte/remotion-template](https://github.com/satelllte/remotion-template)**
    *   **Descrição:** Template opinativo com TailwindCSS.
    *   **Ideal para:** Quem prefere estilizar com classes utilitárias.

## 🛠️ Ferramentas Auxiliares

*   **[stefanwittwer/remotion-animated](https://github.com/stefanwittwer/remotion-animated)**
    *   **Descrição:** Animações declarativas para simplificar o código.
