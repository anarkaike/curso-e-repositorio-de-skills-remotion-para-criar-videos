import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";

export const PathDrawing: React.FC<{
  color: string;
}> = ({ color = "#00d2ff" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // A simple heart shape path
  const path = "M 10,30 A 20,20 0,0,1 50,30 A 20,20 0,0,1 90,30 Q 90,60 50,90 Q 10,60 10,30 z";
  
  // Scale it up
  const scale = 8;
  
  const evolution = evolvePath(frame / (fps * 2), path); // Draw over 2 seconds

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#222",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <svg width="800" height="800" viewBox="0 0 400 400">
        <g transform={`scale(${scale}) translate(-20, 0)`}>
            <path
            d={path}
            stroke={color}
            strokeWidth="2"
            fill="none"
            strokeDasharray={evolution.strokeDasharray}
            strokeDashoffset={evolution.strokeDashoffset}
            strokeLinecap="round"
            />
        </g>
      </svg>
      
      <div style={{ position: "absolute", bottom: 100, color: "white", fontSize: 24 }}>
        SVG Path Evolution
      </div>
    </AbsoluteFill>
  );
};
