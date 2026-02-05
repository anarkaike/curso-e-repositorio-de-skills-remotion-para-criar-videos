# Skill: Organizando a Gaveta (Pastas)

## 📘 Traduzindo para o "Mamanês"
Sabe aquela gaveta de talheres? Garfo com garfo, faca com faca.
Se você jogar tudo misturado, na hora da pressa não acha nada.
No Remotion, usamos **Pastas (Folders)** para não misturar os vídeos do Instagram com os vídeos do YouTube.

1.  **Folder:** É a divisória da gaveta.
2.  **Organização:** Deixa o menu lateral bonitinho e fácil de achar.

## 💻 Como fica o código

```tsx
import { Composition, Folder } from 'remotion';

export const CozinhaOrganizada = () => {
  return (
    <>
      {/* Gaveta de Marketing */}
      <Folder name="Instagram">
        <Composition id="StoryDaPromo" width={1080} height={1920} />
        <Composition id="ReelDancinha" width={1080} height={1920} />
      </Folder>

      {/* Gaveta de Aulas */}
      <Folder name="YouTube">
        <Composition id="TutorialCompleto" width={1920} height={1080} />
      </Folder>
    </>
  );
};
```
