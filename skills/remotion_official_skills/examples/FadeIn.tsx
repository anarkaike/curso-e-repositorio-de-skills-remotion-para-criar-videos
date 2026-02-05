import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

/**
 * EXEMPLO 1: Animação Básica (FadeIn)
 * 
 * O QUE A SKILL ENSINOU:
 * 1. Usar useCurrentFrame() para obter o quadro atual.
 * 2. Usar interpolate() para mapear frames em valores (0 a 1).
 * 3. Definir a duração em segundos * fps.
 * 4. PROIBIDO: Usar CSS transitions (transition: opacity 1s).
 */

export const FadeInExample = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animação de 1 segundo (0 -> fps)
  const opacity = interpolate(frame, [0, fps], [0, 1], {
    extrapolateRight: 'clamp', // Mantém opacidade 1 após o fim da animação
  });

  const scale = interpolate(frame, [0, fps], [0.8, 1], {
    extrapolateRight: 'clamp',
    easing: (t) => t * (2 - t), // Easing simples (Ease Out Quad)
  });

  return (
    <div
      style={{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white',
        opacity, // Aplicando a animação
        transform: `scale(${scale})`, // Aplicando a escala
      }}
    >
      <h1 style={{ fontFamily: 'sans-serif', fontSize: 80 }}>
        Hello Remotion!
      </h1>
    </div>
  );
};
