import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender } from "remotion";
import { Lottie } from "@remotion/lottie";

export const LottiePlayer: React.FC<{
  animationUrl: string;
}> = ({
  animationUrl = "https://assets9.lottiefiles.com/packages/lf20_5njp3vgg.json", // Reliable URL
}) => {
  const [handle] = useState(() => delayRender());
  const [animationData, setAnimationData] = useState<object | null>(null);

  useEffect(() => {
    fetch(animationUrl)
      .then((data) => data.json())
      .then((json) => {
        setAnimationData(json);
        continueRender(handle);
      })
      .catch((err) => {
        console.error("Error loading animation:", err);
        continueRender(handle);
      });
  }, [handle, animationUrl]);

  if (!animationData) {
    return null;
  }

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#ffffff",
      }}
    >
      <Lottie animationData={animationData as any} />
    </AbsoluteFill>
  );
};
