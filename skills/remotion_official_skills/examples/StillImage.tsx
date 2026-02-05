import { Still } from 'remotion';
import { DynamicTitle } from './DynamicProps';

/**
 * EXEMPLO 5: Still Images (Thumbnails)
 * 
 * O QUE A SKILL ENSINOU:
 * 1. Usar <Still> para gerar imagens estáticas (PNG/JPEG).
 * 2. Não precisa de durationInFrames ou fps.
 * 3. Ótimo para gerar thumbnails de YouTube programaticamente.
 */

export const ThumbnailRoot = () => {
  return (
    <Still
      id="YouTubeThumbnail"
      component={DynamicTitle}
      width={1280}
      height={720}
      defaultProps={{
        title: "COMO APRENDER REMOTION",
        color: "#ff0000",
        size: 100,
      }}
    />
  );
};
