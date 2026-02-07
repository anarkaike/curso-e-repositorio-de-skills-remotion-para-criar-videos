import axios from 'axios';

// 📝 A Receita do Pedido
const pedido = {
  topic: "Morning Routine",
  videoStyle: "Cinematic",
  voice: "Sarah_US",
};

// 🏃‍♂️ O Menino de Recados (Envia o pedido pra fábrica)
async function pedirVideo() {
  console.log("🛵 Enviando pedido para a cozinha...");
  
  try {
    const resposta = await axios.post('http://localhost:3123/generate', pedido);
    console.log("✅ Vídeo pronto! Tá na mão:", resposta.data.url);
  } catch (erro) {
    console.log("🔥 A cozinha pegou fogo:", erro instanceof Error ? erro.message : erro);
  }
}

pedirVideo();
