# Skill: A Suavidade do Amanhecer (FadeIn)

## 🌅 O Conceito (A Cor da Simplicidade)
Nada na natureza aparece "do nada". O sol nasce aos poucos; uma flor desabrocha lentamente.
O **FadeIn** é essa tradução digital da naturalidade. É trazer um elemento à luz com respeito aos olhos de quem vê.

1.  **useCurrentFrame():** O fluir do tempo (O Agora).
2.  **interpolate():** O tradutor. Ele converte "tempo passando" em "luz aparecendo".
    *   *Começo:* Escuridão (0).
    *   *Fim:* Claridade total (1).

## 🎬 A Tradução para Código

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const ExemploAmanhecer = () => {
  const frame = useCurrentFrame(); // O tempo correndo
  const { fps } = useVideoConfig(); // A velocidade da realidade

  // A Jornada da Luz: Do invisível ao visível
  const opacidade = interpolate(frame, [0, fps], [0, 1], {
    extrapolateRight: 'clamp', // A luz permanece
  });

  return (
    <div style={{ opacity: opacidade }}> 
      <h1>Olá, Mundo! (Com Naturalidade)</h1>
    </div>
  );
};
```
