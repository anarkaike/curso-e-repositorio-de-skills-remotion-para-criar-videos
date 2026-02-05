# Skill: O Chefe e a Forma do Bolo (Root e Compositions)

## 📘 Traduzindo para o "Mamanês"
Imagine que você vai fazer um bolo.
1.  **Composition (A Forma):** Você precisa decidir se a forma é redonda ou quadrada (largura/altura) e quanto tempo vai ficar no forno (duração). Sem forma, a massa escorre.
2.  **RemotionRoot (O Chefe de Cozinha):** É quem organiza todas as formas na bancada. Ele diz: "Aqui sai o bolo de chocolate, ali sai o de cenoura".

## 💻 Como fica o código

```tsx
import { Composition } from 'remotion';
import { FadeInExample } from './FadeIn';

export const RemotionRoot = () => {
  return (
    <>
      {/* Aqui é a Forma do Bolo */}
      <Composition
        id="MeuPrimeiroVideo"       // Nome na etiqueta
        component={FadeInExample}   // A massa (o recheio)
        durationInFrames={150}      // Tempo de forno (5 segundos)
        fps={30}                    // Velocidade
        width={1920}                // Largura (TV Grande)
        height={1080}               // Altura
      />
    </>
  );
};
```
