import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from "remotion";

export const AnimatedChart: React.FC<{
  data: number[];
  labels: string[];
  barColor: string;
  textColor: string;
}> = ({
  data = [30, 50, 80, 40, 90],
  labels = ["Jan", "Feb", "Mar", "Apr", "May"],
  barColor = "#00d2ff",
  textColor = "#ffffff",
}) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  const maxValue = Math.max(...data);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1e1e1e",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "row",
        gap: "40px",
        padding: "50px",
      }}
    >
      {data.map((value, index) => {
        const progress = spring({
          frame: frame - index * 5, // Stagger effect
          fps,
          config: {
            damping: 10,
          },
        });

        const height = (value / maxValue) * 600; // Max height 600px

        return (
          <div
            key={index}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "flex-end",
              height: "700px",
            }}
          >
            <div
              style={{
                width: "80px",
                height: `${height * progress}px`,
                backgroundColor: barColor,
                borderRadius: "10px 10px 0 0",
                marginBottom: "20px",
              }}
            />
            <span
              style={{
                color: textColor,
                fontSize: "30px",
                fontFamily: "Arial, sans-serif",
                opacity: progress,
              }}
            >
              {labels[index]}
            </span>
            <span
              style={{
                color: textColor,
                fontSize: "24px",
                fontFamily: "Arial, sans-serif",
                opacity: progress,
                marginTop: "10px",
              }}
            >
              {Math.round(value * progress)}
            </span>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
