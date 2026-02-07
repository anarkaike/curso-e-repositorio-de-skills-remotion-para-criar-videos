import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Gif } from "@remotion/gif";

export const GifScene: React.FC<{
  gifUrl: string;
  caption: string;
}> = ({
  gifUrl = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzM0eDk1dm55eDV3ZnJ5eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyM/giphy.gif",
  caption = "WHEN IT WORKS",
}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#222",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          border: "10px solid white",
          borderRadius: "20px",
          overflow: "hidden",
          width: "600px",
          height: "600px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#000",
        }}
      >
        <Gif
          src={gifUrl}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
          fit="cover"
        />
      </div>
      <h1
        style={{
          color: "white",
          marginTop: "50px",
          fontFamily: "Impact, sans-serif",
          fontSize: "80px",
          textAlign: "center",
          textShadow: "4px 4px 0px #000",
        }}
      >
        {caption}
      </h1>
    </AbsoluteFill>
  );
};
