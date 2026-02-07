
import os
import sys
import logging
from gtts import gTTS

# Setup logging
logging.basicConfig(level=logging.INFO)

def generate_mock_audio(text_file, output_file):
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        logging.info(f"Generating mock audio for text length: {len(text)}")
        
        # Use gTTS (Google Text-to-Speech)
        tts = gTTS(text=text, lang='pt')
        tts.save(output_file)
        
        logging.info(f"Mock audio saved to {output_file}")
        
    except Exception as e:
        logging.error(f"Failed to generate mock audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mock_audio_generator.py <text_file> <output_file>")
        sys.exit(1)
        
    text_file = sys.argv[1]
    output_file = sys.argv[2]
    
    generate_mock_audio(text_file, output_file)
