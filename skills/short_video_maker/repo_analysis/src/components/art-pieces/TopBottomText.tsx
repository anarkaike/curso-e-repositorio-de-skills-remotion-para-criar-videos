import React from "react";
import { AbsoluteFill, Img } from "remotion";
import { z } from "zod";

export const topBottomTextSchema = z.object({
  imageSrc: z.string(),
  topText: z.string(),
  bottomText: z.string(),
  textColor: z.string().optional(),
  textStrokeColor: z.string().optional(),
});

export type TopBottomTextProps = z.infer<typeof topBottomTextSchema>;

export const TopBottomText: React.FC<TopBottomTextProps> = ({
  imageSrc,
  topText,
  bottomText,
  textColor = "white",
  textStrokeColor = "black",
}) => {
  const textStyle: React.CSSProperties = {
    fontFamily: "Impact, sans-serif",
    fontSize: "80px",
    textTransform: "uppercase",
    color: textColor,
    WebkitTextStroke: `3px ${textStrokeColor}`,
    textAlign: "center",
    width: "100%",
    position: "absolute",
    lineHeight: 1.1,
    textShadow: "2px 2px 5px rgba(0,0,0,0.5)",
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Img
        src={imageSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
        }}
      />
      <div style={{ ...textStyle, top: 20 }}>{topText}</div>
      <div style={{ ...textStyle, bottom: 20 }}>{bottomText}</div>
    </AbsoluteFill>
  );
};
