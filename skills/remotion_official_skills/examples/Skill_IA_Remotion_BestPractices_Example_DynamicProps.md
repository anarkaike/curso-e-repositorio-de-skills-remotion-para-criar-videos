# Skill: A Personalização (Props)

## 🧬 O DNA da Criação
Não construímos uma nova realidade para cada pessoa. Criamos uma estrutura única (Template) que se adapta a quem a observa.
Os **Props** são como o DNA: instruções que mudam a cor, o texto e a forma do resultado final, mantendo a mesma essência.

*   **Props:** As variáveis que tornam cada vídeo único (Nome, Cor, Título).

## 🎬 O Código da Adaptação

```tsx
import { z } from "zod"; // O Guardião da Estrutura

// O Molde (O que esperamos receber)
export const myCompSchema = z.object({
  title: z.string(), // Um texto
  color: z.string(), // Uma cor
});

export const TemplateMestre = ({ title, color }) => {
  return <h1 style={{ color }}>{title}</h1>;
};
```
