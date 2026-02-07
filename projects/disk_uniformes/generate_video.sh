#!/bin/bash
set -e

# Base directories
PROJECT_ROOT="$(pwd)"
REPO_ROOT="$(dirname "$(dirname "$PROJECT_ROOT")")"
SKILLS_DIR="$REPO_ROOT/skills/automation_lab"
VENV_PATH="$SKILLS_DIR/.venv"
SRC_PATH="$SKILLS_DIR/tool_ecommerce_video/src"

# Activate virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Load .env file if exists
if [ -f "$REPO_ROOT/.env" ]; then
    source "$REPO_ROOT/.env"
    export ELEVENLABS_API_KEY
fi

# Set PYTHONPATH to include the src directory
export PYTHONPATH="$SRC_PATH"

# Paths
SPOKEN_SCRIPT="$PROJECT_ROOT/spoken_script/spoken_script.txt"
AUDIO_OUTPUT="$PROJECT_ROOT/audio/spoken_script.mp3"
ALIGNMENT_OUTPUT="$PROJECT_ROOT/aligned_script_with_timestamps/spoken_script.json"

# 1. Generate Audio
echo "Generating Audio..."
if [ -n "$ELEVENLABS_API_KEY" ]; then
    python3 "$SRC_PATH/generate_audio_elevenlabs.py" "$SPOKEN_SCRIPT" "$AUDIO_OUTPUT"
else
    echo "Warning: ELEVENLABS_API_KEY not found. Skipping audio generation (using existing audio)."
fi

# 2. Get Audio Duration
echo "Calculating Audio Duration..."
if [ -f "$AUDIO_OUTPUT" ]; then
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_OUTPUT")
    echo "Audio Duration: $DURATION seconds"
else
    echo "Error: Audio file not found at $AUDIO_OUTPUT"
    exit 1
fi

# 3. Generate Alignment
echo "Generating Alignment..."
python3 "$SRC_PATH/generate_simple_alignment.py" "$SPOKEN_SCRIPT" "$DURATION" "$ALIGNMENT_OUTPUT"

# 4. Create Video
echo "Generating video for Disk Uniformes..."
cd "$PROJECT_ROOT" && python3 "$SRC_PATH/create_video.py"

echo "Done! Check video_output/final_video_with_audio.mp4"
