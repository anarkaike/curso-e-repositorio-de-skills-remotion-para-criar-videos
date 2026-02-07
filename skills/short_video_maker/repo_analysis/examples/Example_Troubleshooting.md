# 🧹 Guia de Faxina (Troubleshooting)

Se o robô engasgar, siga esse guia:

## 1. "O vídeo ficou mudo!"
*   **Causa:** O Kokoro (locutor) pode estar cansado ou o volume está baixo.
*   **Solução:** Verifique se o texto está em Inglês. O Kokoro *só fala inglês* por enquanto. Se mandar português, ele vai tentar ler com sotaque gringo ou ficar mudo.

## 2. "Não achou vídeo de fundo"
*   **Causa:** O Pexels não achou nada com a palavra que você mandou.
*   **Solução:** Tente palavras mais comuns. Em vez de "ornitorrinco albino", tente "natureza".

## 3. "Demorou 3 dias pra fazer um vídeo de 1 minuto"
*   **Causa:** Seu computador está sofrendo. Renderizar vídeo gasta muita energia.
*   **Solução:**
    *   Feche outras coisas.
    *   Use o Docker "Tiny" (versão leve).
    *   Tenha paciência (ou compre um computador da NASA).

## 4. "Deu erro de API Key"
*   **Causa:** Você não deu a chave do clube pro porteiro.
*   **Solução:** Garanta que `PEXELS_API_KEY` está configurado. Sem chave, sem festa.
