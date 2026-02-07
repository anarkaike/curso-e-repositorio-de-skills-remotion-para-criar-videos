export enum AvailableComponentsEnum {
  PortraitVideo = "ShortVideo",
  LandscapeVideo = "LandscapeVideo",
  TopBottomText = "TopBottomText",
  AnimatedTitle = "AnimatedTitle",
  AnimatedChart = "AnimatedChart",
  AudioWaveform = "AudioWaveform",
  LottiePlayer = "LottiePlayer",
  ThreeDScene = "ThreeDScene",
  MotionBlurTitle = "MotionBlurTitle",
  GifScene = "GifScene",
  NoiseOverlay = "NoiseOverlay",
  PathDrawing = "PathDrawing",
}
export type OrientationConfig = {
  width: number;
  height: number;
  component: AvailableComponentsEnum;
};
