import { Composition, Folder } from 'remotion';
import { FadeInExample } from './FadeIn';
import { DynamicTitle, myCompSchema } from './DynamicProps';

/**
 * EXEMPLO 4: Organização com Pastas
 * 
 * O QUE A SKILL ENSINOU:
 * 1. Usar <Folder> para agrupar composições no player do Remotion.
 * 2. Facilita a navegação em projetos grandes.
 * 3. Mostra como passar props validadas pelo Zod na Composition.
 */

export const OrganizedRoot = () => {
  return (
    <>
      <Folder name="Marketing">
        <Composition
          id="PromoInstagram"
          component={FadeInExample}
          durationInFrames={300}
          fps={30}
          width={1080}
          height={1920} // Vertical
        />
      </Folder>

      <Folder name="Templates">
        <Composition
          id="DynamicHeader"
          component={DynamicTitle}
          durationInFrames={60}
          fps={30}
          width={1920}
          height={1080}
          schema={myCompSchema} // Vincula o schema Zod
          defaultProps={{
            title: "Texto Dinâmico",
            color: "#00ccff",
            size: 120,
          }}
        />
      </Folder>
    </>
  );
};
