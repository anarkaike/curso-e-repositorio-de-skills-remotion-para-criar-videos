# Skill: Receita Personalizada (Props Dinâmicas)

## 📘 Traduzindo para o "Mamanês"
Imagine uma receita de bolo que tem um "espaço em branco" para o sabor.
*   Hoje você escreve "Chocolate" no papelzinho, e o bolo sai de Chocolate.
*   Amanhã você escreve "Morango", e sai de Morango.

Isso são **Props Dinâmicas**. E para ninguém colocar "Cimento" no lugar do sabor, a gente usa um fiscal chamado **Zod** (o segurança da receita).

1.  **Zod:** O segurança que confere: "Isso é texto? Isso é cor? O tamanho é número?".
2.  **Props:** Os ingredientes que você pode trocar sem ter que cozinhar uma receita nova do zero.

## 💻 Como fica o código

```tsx
import { z } from "zod";

// 1. A Lista de Ingredientes Permitidos (O Fiscal Zod)
export const receitaSchema = z.object({
  titulo: z.string(),           // Tem que ser texto!
  cor: z.string(),              // Tem que ser texto (código da cor)!
  tamanho: z.number().min(10),  // Tem que ser número, e no mínimo 10!
});

// 2. O Bolo que aceita os ingredientes
export const TituloDinamico = ({ titulo, cor, tamanho }) => {
  return (
    <h1 style={{ color: cor, fontSize: tamanho }}>
      {titulo}
    </h1>
  );
};
```
