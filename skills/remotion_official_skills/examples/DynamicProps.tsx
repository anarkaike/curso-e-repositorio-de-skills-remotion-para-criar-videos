import { z } from "zod";
import { useCurrentFrame, interpolate } from "remotion";

/**
 * EXEMPLO 3: Tipagem e Props Dinâmicas
 * 
 * O QUE A SKILL ENSINOU:
 * 1. Usar Zod para validar as props (essencial para renderização parametrizada).
 * 2. Usar 'type' para props.
 * 3. Assegurar que defaultProps satisfazem o tipo.
 */

// 1. Definição do Schema com Zod
export const myCompSchema = z.object({
  title: z.string(),
  color: z.string(),
  size: z.number().min(10).max(200),
});

// 2. Inferência do Tipo TypeScript
export type MyCompProps = z.infer<typeof myCompSchema>;

export const DynamicTitle = ({ title, color, size }: MyCompProps) => {
  const frame = useCurrentFrame();
  
  const y = interpolate(frame, [0, 30], [50, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ flex: 1, backgroundColor: 'black', justifyContent: 'center', alignItems: 'center' }}>
      <h1
        style={{
          color,
          fontSize: size,
          transform: `translateY(${y}px)`,
          fontFamily: 'Helvetica',
        }}
      >
        {title}
      </h1>
    </div>
  );
};
