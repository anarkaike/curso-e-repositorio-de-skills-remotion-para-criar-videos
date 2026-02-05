import { Composition } from 'remotion';
import { FadeInExample } from './FadeIn';

/**
 * EXEMPLO 2: Root e Compositions
 * 
 * O QUE A SKILL ENSINOU:
 * 1. Composition define os metadados do vídeo (fps, duração, dimensões).
 * 2. Deve ser exportado em um componente Root (geralmente src/Root.tsx).
 * 3. IDs devem ser únicos.
 */

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="MyFirstVideo"
        component={FadeInExample}
        durationInFrames={150} // 5 segundos a 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
            // Se o componente tivesse props, elas iriam aqui
        }}
      />
    </>
  );
};
