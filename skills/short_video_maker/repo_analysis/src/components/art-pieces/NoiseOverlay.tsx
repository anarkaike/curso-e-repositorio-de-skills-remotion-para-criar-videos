import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, random } from "remotion";

export const NoiseOverlay: React.FC<{
  text: string;
  noiseOpacity: number;
}> = ({ text = "VINTAGE VIBES", noiseOpacity = 0.15 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  
  // Generate a random seed for every frame to animate the noise
  const seed = useMemo(() => random(frame), [frame]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a1a",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          color: "#f0f0f0",
          fontSize: "120px",
          fontFamily: "Courier New, monospace",
          letterSpacing: "5px",
          zIndex: 1,
        }}
      >
        {text}
      </h1>
      
      {/* SVG Noise Layer */}
      <AbsoluteFill style={{ opacity: noiseOpacity, pointerEvents: 'none' }}>
        <svg width="100%" height="100%">
          <filter id="noiseFilter">
            <feTurbulence 
              type="fractalNoise" 
              baseFrequency="0.8" 
              numOctaves="3" 
              stitchTiles="stitch" 
              seed={Math.floor(seed * 100)} 
            />
            <feColorMatrix type="saturate" values="0" />
          </filter>
          <rect width="100%" height="100%" filter="url(#noiseFilter)" />
        </svg>
      </AbsoluteFill>
      
      {/* Old TV Line Effect */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06))",
          backgroundSize: "100% 2px, 3px 100%",
          pointerEvents: "none",
          zIndex: 2,
        }}
      />
    </AbsoluteFill>
  );
};
