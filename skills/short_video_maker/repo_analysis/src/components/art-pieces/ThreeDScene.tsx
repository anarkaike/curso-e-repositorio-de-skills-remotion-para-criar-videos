import { ThreeCanvas } from "@remotion/three";
import React, { useRef } from "react";
import { useVideoConfig, useCurrentFrame } from "remotion";
import { useFrame } from "@react-three/fiber";
import { Box, Environment, Text } from "@react-three/drei";
import * as THREE from "three";

const SpinningBox: React.FC<{ color: string }> = ({ color }) => {
  const mesh = useRef<THREE.Mesh>(null);
  const frame = useCurrentFrame();

  useFrame(() => {
    if (mesh.current) {
      mesh.current.rotation.x = frame * 0.02;
      mesh.current.rotation.y = frame * 0.03;
    }
  });

  return (
    <Box ref={mesh} args={[2.5, 2.5, 2.5]}>
      <meshStandardMaterial color={color} roughness={0.3} metalness={0.8} />
    </Box>
  );
};

const SceneContent: React.FC<{
  primaryColor: string;
  text: string;
}> = ({ primaryColor, text }) => {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <SpinningBox color={primaryColor} />
      <Environment preset="city" />
    </>
  );
};

export const ThreeDScene: React.FC<{
  primaryColor: string;
  text: string;
}> = ({ primaryColor = "#ff0055", text = "3D WORLD" }) => {
  const { width, height } = useVideoConfig();

  return (
    <ThreeCanvas width={width} height={height} style={{ backgroundColor: "#111" }}>
      <SceneContent primaryColor={primaryColor} text={text} />
    </ThreeCanvas>
  );
};
