import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from "remotion";
import { Star } from "@remotion/shapes";
import { z } from "zod";

export const animatedTitleSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  primaryColor: z.string().optional(),
  secondaryColor: z.string().optional(),
});

export type AnimatedTitleProps = z.infer<typeof animatedTitleSchema>;

export const AnimatedTitle: React.FC<AnimatedTitleProps> = ({
  title,
  subtitle,
  primaryColor = "#ff0055",
  secondaryColor = "white",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 200,
    },
  });

  const rotate = spring({
    frame: frame - 5,
    fps,
    config: {
      damping: 200, // Keep spinning slowly
      stiffness: 100,
    },
    durationInFrames: 300, 
  });
  
  // Continuous rotation logic
  const continuousRotation = (frame / 3);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#111",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden"
      }}
    >
      <div style={{ transform: `scale(${entrance})`, opacity: 0.6 }}>
        <Star
          points={12}
          outerRadius={600}
          innerRadius={300}
          fill={primaryColor}
          style={{
             transform: `rotate(${continuousRotation}deg)`,
          }}
        />
      </div>
      
      <div style={{ position: 'absolute', zIndex: 1, textAlign: 'center', width: '80%' }}>
        <h1
          style={{
            fontFamily: "Arial Black, sans-serif",
            fontSize: "100px",
            color: secondaryColor,
            textTransform: "uppercase",
            textShadow: "4px 4px 0px #000",
            margin: 0,
            transform: `scale(${entrance})`,
            opacity: entrance,
            lineHeight: 1.1,
          }}
        >
          {title}
        </h1>
        {subtitle && (
             <h2
            style={{
                fontFamily: "Arial, sans-serif",
                fontSize: "40px",
                fontWeight: "bold",
                color: secondaryColor,
                marginTop: "20px",
                opacity: Math.min(1, Math.max(0, (frame - 15) / 20)), // Fade in
                transform: `translateY(${(1 - Math.min(1, Math.max(0, (frame - 15) / 20))) * 20}px)`
            }}
            >
            {subtitle}
            </h2>
        )}
      </div>
    </AbsoluteFill>
  );
};
