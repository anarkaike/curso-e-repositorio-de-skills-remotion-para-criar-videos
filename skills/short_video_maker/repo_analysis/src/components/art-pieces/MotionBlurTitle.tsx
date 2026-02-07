import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from "remotion";
import { Trail } from "@remotion/motion-blur";

export const MotionBlurTitle: React.FC<{
  text: string;
  color: string;
}> = ({ text = "SPEED", color = "#ffcc00" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animate position from left to right quickly
  const progress = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 100,
    },
  });

  // Map progress (0 to 1) to X position (-500 to 0)
  const x = -1000 + progress * 1000;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Trail layers={4} lagInFrames={2}>
        <h1
          style={{
            color: color,
            fontSize: "180px",
            fontFamily: "Impact, sans-serif",
            transform: `translateX(${x}px)`,
            margin: 0,
            textTransform: "uppercase",
            letterSpacing: "10px",
          }}
        >
          {text}
        </h1>
      </Trail>
      <div style={{ position: "absolute", bottom: 100, color: "#666" }}>
        Motion Blur Trail Effect
      </div>
    </AbsoluteFill>
  );
};
