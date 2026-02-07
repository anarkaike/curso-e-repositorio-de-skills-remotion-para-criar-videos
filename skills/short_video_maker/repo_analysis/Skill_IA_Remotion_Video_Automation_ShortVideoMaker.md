# Skill: O Narrador Onisciente (Short Video Maker)

## 📌 O Conceito (A Ideia Viva)
**Nome:** Short Video Maker
**Papel:** "O Narrador Onisciente"
**Criador:** David Gyori
**A Promessa:** Você planta a semente (ideia), ele entrega a floresta (vídeo completo). Da voz à imagem, do som à legenda, tudo brota de um único comando.

## 🕵️ A Análise Sensorial

### 📉 O Labirinto (A Complexidade)
Criar um vídeo viral manualmente é navegar por um labirinto de ferramentas desconexas:
1.  Escrever (Roteiro).
2.  Falar (Locução).
3.  Buscar (Imagens).
4.  Costurar (Edição).
5.  Escrever de novo (Legenda).

### 💡 O Caminho Reto (A Simplicidade)
Esta skill é uma linha reta entre a intenção e o resultado.
*   **Voz (Kokoro):** O som humano, sintético mas com alma.
*   **Texto (Whisper):** A compreensão exata do que foi dito.
*   **Olhar (Pexels):** A janela para o mundo visual.
*   **Mãos (Remotion):** O artesão que une as peças.

### 📊 A Clareza do Valor
*   **Abundância:** A matéria-prima (assets) é acessível e vasta.
*   **Tempo:** O que levava horas, agora leva o tempo de um café.
*   **Validação:** Uma comunidade de visionários já percorreu este caminho.

## 🌿 O Ritual de Preparação (Instalação)

### 📋 Os Elementos
Para esta alquimia, precisamos de:
1.  **A Chave do Mundo (Pexels API Key):** Seu acesso à biblioteca visual infinita. [Obtenha aqui](https://www.pexels.com/api/).
2.  **O Recipiente (Docker):** Um ambiente puro e isolado para a criação acontecer sem interferências.

### Opção 1: O Contêiner (Docker)
Se você já possui o Docker:

```bash
docker run -it --rm --name short-video-maker -p 3123:3123 -e PEXELS_API_KEY=SUA_CHAVE_AQUI gyoridavid/short-video-maker:latest-tiny
```
*Tradução:* "Crie um espaço seguro, abra uma janela (porta 3123) e use esta chave para buscar inspiração."

### Opção 2: O Artesanato Local (NPM - Manual)
Para construir em seu próprio solo:

1.  **Reunir as Ferramentas (Install):**
    ```bash
    npm install
    ```
2.  **Iniciar a Criação (Start):**
    ```bash
    npm run build
    npm start
    ```

## 🎩 A Performance (Como Operar)

A ferramenta se torna um "Oráculo". Você pergunta, ela responde com vídeo.

### A Intenção (Input)
Você envia um desejo (JSON):
*"Tema: Gatos. Sentimento: Dominação mundial. Tom: Humorístico."*

O sistema:
1.  Visualiza (Busca vídeos).
2.  Verbaliza (Gera áudio).
3.  Materializa (Renderiza o vídeo).

## 🩺 Diagnóstico e Cura (Troubleshooting)

*   **Sintoma: "Pexels API Key missing"**
    *   *Causa:* A porta da biblioteca visual está trancada.
    *   *Cura:* Ofereça a chave correta no arquivo `.env`.
    
*   **Sintoma: "Out of Memory"**
    *   *Causa:* O sonho foi maior que a capacidade de sonhar (RAM).
    *   *Cura:* Simplifique o pedido ou feche outras janelas da mente (navegador).

---

## 📂 Galeria de Inspiração
*   [💌 O Pedido (Payload JSON)](./examples/Example_Payload_SimpleStory.json)
*   [🔌 A Conexão (MCP Config)](./examples/Example_MCP_Config.json)
*   [🏗️ O Mapa (Arquitetura)](./examples/Example_Architecture_Flow.md)
*   [📝 A Escritura (Script)](./examples/Example_Script_Generate.ts)
