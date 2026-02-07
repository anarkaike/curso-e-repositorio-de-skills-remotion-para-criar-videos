# 🏗️ A Planta da Fábrica (Fluxo de Trabalho)

Imagine uma linha de montagem de carros, mas para vídeos.

1.  **O Cliente (Você)**
    *   Entrega o pedido: "Quero um vídeo sobre café."

2.  **O Roteirista (LLM - Opcional)**
    *   Escreve o texto: "Café é a gasolina do programador..."

3.  **O Locutor (Kokoro TTS)**
    *   Lê o texto e grava o áudio (MP3).

4.  **O Estagiário da Legenda (Whisper)**
    *   Ouve o áudio e anota tudo o que foi dito, com o tempo exato (Legendas).

5.  **O Produtor de Imagem (Pexels API)**
    *   Procura vídeos de xícaras, grãos de café, pessoas bebendo.

6.  **O Editor (Remotion)**
    *   Junta o áudio, a legenda e os vídeos de fundo.
    *   Corta tudo no tamanho certo (9:16 pro TikTok).

7.  **O Forno (Render)**
    *   Assa tudo e cospe um arquivo `.mp4` pronto.
