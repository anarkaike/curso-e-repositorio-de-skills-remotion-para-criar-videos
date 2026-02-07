# Skill: A Fotografia do Instante (Thumbnails)

## 📸 A Captura da Essência
Em um fluxo contínuo de tempo (vídeo), existem momentos que merecem ser eternizados.
O Remotion não apenas cria movimentos, ele também sabe pausar o tempo para criar a imagem perfeita (Thumbnail).

*   **Still:** É o instante congelado, a fotografia de alta resolução extraída do movimento.

## 🎬 O Código da Pausa

```tsx
import { Still } from 'remotion';
import { ExemploAmanhecer } from './FadeIn'; // O movimento original

export const Cartaz = () => {
  return (
    <Still
      id="CapaDoYoutube"
      component={ExemploAmanhecer} // A fonte da imagem
      width={1280}
      height={720}
    />
  );
};
```
