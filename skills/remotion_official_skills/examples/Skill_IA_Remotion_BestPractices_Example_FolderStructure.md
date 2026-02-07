# Skill: A Arquitetura da Informação (Pastas)

## 🌿 O Conceito (A Textura da Organização)
Imagine uma biblioteca imensa. Se todos os livros estivessem jogados no chão, o conhecimento seria inacessível.
No Remotion, usamos **Folders** como prateleiras temáticas. É a **simplicidade** de saber exatamente onde cada história está guardada.

1.  **Folder:** A Prateleira.
2.  **Composição:** O Livro (A História Visual).

## 🎬 A Tradução para Código

```tsx
import { Composition, Folder } from 'remotion';

export const BibliotecaVisual = () => {
  return (
    <>
      {/* A Prateleira do Instagram */}
      <Folder name="Instagram">
        <Composition id="StoryInfluencer" width={1080} height={1920} />
        <Composition id="ReelViral" width={1080} height={1920} />
      </Folder>

      {/* A Prateleira do YouTube */}
      <Folder name="YouTube">
        <Composition id="Documentario" width={1920} height={1080} />
      </Folder>
    </>
  );
};
```
