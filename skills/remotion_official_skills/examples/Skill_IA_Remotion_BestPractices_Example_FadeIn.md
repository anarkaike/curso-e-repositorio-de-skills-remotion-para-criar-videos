# Skill: Animação Básica (O tal do FadeIn)

## 📘 Traduzindo para o "Mamanês"
Sabe quando você aumenta o volume da TV devagarinho? Isso é um **FadeIn**.
No Remotion, a gente não gira um botão. A gente usa matemática (mas calma, o robô faz a conta).

1.  **useCurrentFrame():** É o relógio do vídeo. Ele diz: "Estamos na foto número 10!".
2.  **interpolate():** É a "Regra de Três Mágica".
    *   *Se no frame 0 a opacidade é 0 (invisível)...*
    *   *E no frame 30 a opacidade é 1 (visível)...*
    *   *No frame 15, a opacidade é 0.5 (metade)!*
3.  **PROIBIDO:** Usar animação de site (CSS Transitions). O vídeo precisa de certeza absoluta de como está cada foto, e o CSS é meio "vida louca".

## 💻 Como fica o código (O Robô escreve isso)

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const FadeInExample = () => {
  const frame = useCurrentFrame(); // O Relógio
  const { fps } = useVideoConfig(); // A Velocidade (30 fotos por segundo)

  // A Mágica: Transforma o tempo (frame) em visibilidade (opacity)
  const opacity = interpolate(frame, [0, fps], [0, 1], {
    extrapolateRight: 'clamp', // Quando acabar, fica visível pra sempre
  });

  return (
    <div style={{ opacity }}> 
      <h1>Olá Mamãe!</h1>
    </div>
  );
};
```
