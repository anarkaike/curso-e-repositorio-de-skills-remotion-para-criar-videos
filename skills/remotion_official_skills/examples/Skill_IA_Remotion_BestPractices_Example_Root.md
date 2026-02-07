# Skill: A Origem e a Manifestação (Root e Compositions)

## 🌱 A Raiz e o Fruto
Para que a criação exista, ela precisa de um solo (Root) e de uma forma definida (Composition).

1.  **Composition (A Manifestação):** É a definição física da obra. Qual o tamanho do quadro? Quanto tempo dura essa realidade?
2.  **RemotionRoot (A Origem):** É o ponto de partida, o solo fértil onde todas as composições são registradas e organizadas.

## 🎬 O Código da Estrutura

```tsx
import { Composition } from 'remotion';
import { ExemploAmanhecer } from './FadeIn';

export const RemotionRoot = () => {
  return (
    <>
      {/* A Manifestação Principal */}
      <Composition
        id="CampanhaVerao"          // O Nome da Obra
        component={ExemploAmanhecer} // A Essência Visual
        durationInFrames={150}      // A Duração (5 segundos de existência)
        fps={30}                    // O Ritmo do Tempo
        width={1920}                // A Largura do Olhar
        height={1080}               // A Altura do Olhar
      />
    </>
  );
};
```
