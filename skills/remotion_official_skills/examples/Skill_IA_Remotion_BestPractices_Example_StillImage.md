# Skill: Só a Foto (Thumbnails)

## 📘 Traduzindo para o "Mamanês"
As vezes a gente não quer o filme inteiro, quer só o porta-retrato.
Sabe aquela "capinha" do vídeo no YouTube que faz a gente clicar? É a **Thumbnail**.
No Remotion, a gente chama de **Still** (Estático). É um vídeo que não se mexe, perfeito para tirar uma foto e usar de capa.

1.  **Still:** É a câmera fotográfica.
2.  **Vantagem:** Você usa o mesmo código do vídeo para fazer a capa. Assim a letra e a cor ficam iguazinhas!

## 💻 Como fica o código

```tsx
import { Still } from 'remotion';
import { MeuTitulo } from './MeuTitulo';

export const CapaDoVideo = () => {
  return (
    <Still
      id="CapaParaYouTube"
      component={MeuTitulo}
      width={1280}
      height={720}
      defaultProps={{
        titulo: "COMO NÃO DORMIR LENDO CÓDIGO",
      }}
    />
  );
};
```
