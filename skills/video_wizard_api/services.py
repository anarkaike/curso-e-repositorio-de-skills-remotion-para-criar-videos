
import os
import shutil
import uuid
import logging
import subprocess
import requests
import json
import httpx
import g4f
from pathlib import Path
from moviepy.editor import AudioFileClip

# Paths to tools
TOOLS_DIR = Path("../automation_lab/tool_ecommerce_video/src").resolve()

async def generate_suggestions(suggestion_type: str, context: str) -> list[str]:
    """
    Generates suggestions using g4f (Pollinations.ai wrapper) or fallbacks.
    suggestion_type: 'target_audience', 'keywords', 'colors', 'emotions'
    context: Input string (e.g., product name, theme)
    """
    try:
        # Prompt Engineering
        prompts = {
            'target_audience': f"List 5 specific target audiences for a product named '{context}'. Return ONLY the list items separated by commas, nothing else.",
            'keywords': f"List 8 relevant SEO keywords for '{context}'. Return ONLY the list items separated by commas, nothing else.",
            'colors': f"Suggest 3 color palette pairs (Primary, Secondary) for '{context}' in format 'Hex1,Hex2'. Return ONLY the list items separated by commas, nothing else.",
            'emotions': f"List 5 suitable emotions/tones for a video about '{context}'. Return ONLY the list items separated by commas, nothing else.",
            'niche': f"List 3 relevant industry niches for a product named '{context}'. Return ONLY the list items separated by commas, nothing else."
        }
        
        prompt = prompts.get(suggestion_type, "")
        if not prompt:
            return []

        # Attempt to use Pollinations.ai via g4f
        try:
            response = await g4f.ChatCompletion.create_async(
                model="openai",
                provider=g4f.Provider.PollinationsAI,
                messages=[{"role": "user", "content": prompt}],
            )
            
            text_response = str(response)
            logging.info(f"Pollinations response for {suggestion_type}: {text_response}")

            # Simple parsing (split by comma or newline)
            cleaned_text = text_response.replace('\n', ',')
            items = [item.strip().strip('-').strip('*').strip('1234567890.') for item in cleaned_text.split(',') if item.strip()]
            
            # Filter out empty strings and take top 10
            items = [i for i in items if i]
            return items[:10]
            
        except Exception as e:
            logging.warning(f"g4f Pollinations AI failed: {e}")
            # Fallback to simple heuristics
            if suggestion_type == 'colors':
                return ["#000000,#FFFFFF", "#FF0000,#FFFFFF", "#0000FF,#FFFFFF"]
            return [f"Sugestão {i} para {context}" for i in range(1, 6)]

    except Exception as e:
        logging.error(f"Suggestion generation error: {e}")
        return []

CREATE_VIDEO_SCRIPT = TOOLS_DIR / "create_video.py"
GENERATE_AUDIO_SCRIPT = TOOLS_DIR / "generate_audio_elevenlabs.py"
MOCK_AUDIO_SCRIPT = TOOLS_DIR / "mock_audio_generator.py"
ALIGNMENT_SCRIPT = TOOLS_DIR / "generate_simple_alignment.py"

async def run_video_generation(project_data: dict, selected_images: list[str], script_text: str, template: str = "simple", header_text: str = "", footer_text: str = ""):
    job_id = str(uuid.uuid4())
    job_dir = Path(f"jobs/{job_id}").resolve()
    job_dir.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Starting job {job_id} in {job_dir}")
    
    try:
        # 1. Setup Directories
        photos_dir = job_dir / "photos"
        audio_dir = job_dir / "audio"
        colors_dir = job_dir / "colors"
        aligned_dir = job_dir / "aligned_script_with_timestamps"
        font_dir = job_dir / "font"
        
        photos_dir.mkdir()
        audio_dir.mkdir()
        colors_dir.mkdir()
        aligned_dir.mkdir()
        font_dir.mkdir()
        
        # 1.5 Save Branding Info
        branding_info = {
            "template": template,
            "header_text": header_text,
            "footer_text": footer_text
        }
        with open(job_dir / "branding.json", "w") as f:
            json.dump(branding_info, f, indent=2)
        
        # 2. Save Colors
        with open(colors_dir / "colors.txt", "w") as f:
            f.write(f"primary: {project_data.get('primary_color', '#000000')}\n")
            f.write(f"secondary: {project_data.get('secondary_color', '#FFFFFF')}\n")
            f.write(f"text_color: #FFFFFF\n")
            f.write(f"background_color: #000000\n")

        # 3. Process Images
        for i, img_url in enumerate(selected_images):
            try:
                ext = "jpg"
                if "png" in img_url: ext = "png"
                elif "webp" in img_url: ext = "webp"
                
                filename = f"image_{i}.{ext}"
                dest_path = photos_dir / filename
                
                if img_url.startswith("http") and not "localhost" in img_url:
                    # Download
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Referer': 'https://www.google.com/'
                    }
                    response = requests.get(img_url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        with open(dest_path, "wb") as f:
                            f.write(response.content)
                    else:
                        logging.warning(f"Failed to download image {img_url}: Status {response.status_code}")
                elif "localhost" in img_url or img_url.startswith("/uploads/"):
                    # Local copy from uploads
                    # Extract filename from URL or path
                    basename = img_url.split("/")[-1]
                    src_path = Path("uploads") / basename
                    if src_path.exists():
                        shutil.copy(src_path, dest_path)
                    else:
                        logging.warning(f"Image source not found: {src_path}")
            except Exception as e:
                logging.error(f"Failed to process image {img_url}: {e}")

        # Check if we have any images
        valid_images = list(photos_dir.glob("*"))
        if not valid_images:
            logging.warning("No images successfully processed. Using fallback image.")
            fallback_url = "https://image.pollinations.ai/prompt/abstract%20modern%20corporate%20style?width=1080&height=1920"
            try:
                response = requests.get(fallback_url, timeout=10)
                if response.status_code == 200:
                    with open(photos_dir / "fallback.jpg", "wb") as f:
                        f.write(response.content)
                else:
                    logging.error("Failed to download fallback image.")
            except Exception as e:
                logging.error(f"Failed to download fallback image: {e}")

        # 4. Save Script
        script_path = job_dir / "script.txt"
        with open(script_path, "w") as f:
            f.write(script_text)
            
        # 5. Generate Audio (Eleven Labs or Mock)
        logging.info("Generating Audio...")
        audio_output = audio_dir / "narration.mp3"
        
        env = os.environ.copy()
        api_key = env.get("ELEVENLABS_API_KEY")
        
        use_mock = False
        if not api_key:
            logging.warning("ELEVENLABS_API_KEY not found. Using Mock Audio Generator (gTTS).")
            use_mock = True
        
        if not use_mock:
            cmd_audio = [
                "python", str(GENERATE_AUDIO_SCRIPT),
                str(script_path),
                str(audio_output)
            ]
            result_audio = subprocess.run(cmd_audio, capture_output=True, text=True, env=env)
            
            if result_audio.returncode != 0:
                logging.error(f"ElevenLabs generation failed: {result_audio.stderr}. Falling back to Mock Audio.")
                use_mock = True
        
        if use_mock:
            cmd_audio = [
                "python", str(MOCK_AUDIO_SCRIPT),
                str(script_path),
                str(audio_output)
            ]
            result_audio = subprocess.run(cmd_audio, capture_output=True, text=True, env=env)
            
            if result_audio.returncode != 0:
                 return {"status": "failed", "error": f"Audio generation failed (Mock): {result_audio.stderr}"}

        # 6. Get Duration & Generate Alignment
        try:
            audio_clip = AudioFileClip(str(audio_output))
            duration = audio_clip.duration
            audio_clip.close()
        except Exception as e:
            return {"status": "failed", "error": f"Failed to read audio duration: {e}"}
            
        alignment_output = aligned_dir / "aligned_output.json"
        cmd_align = [
            "python", str(ALIGNMENT_SCRIPT),
            str(script_path),
            str(duration),
            str(alignment_output)
        ]
        subprocess.run(cmd_align, check=True)
        
        # 7. Generate Video
        logging.info("Generating Video...")
        # create_video.py expects to run in the directory containing 'photos', 'audio', etc.
        # It uses Path.cwd()
        
        cmd_video = ["python", str(CREATE_VIDEO_SCRIPT)]
        
        # Capture output to log progress
        result_video = subprocess.run(cmd_video, cwd=job_dir, capture_output=True, text=True)
        
        if result_video.returncode != 0:
             logging.error(f"Video generation failed: {result_video.stderr}")
             return {"status": "failed", "error": f"Video generation failed: {result_video.stderr}"}
        
        # 8. Find Output
        output_video = job_dir / "video_output/final_video_with_audio.mp4"
        if output_video.exists():
            # Copy to public uploads or static dir so it can be accessed
            public_filename = f"video_{job_id}.mp4"
            public_path = Path("uploads") / public_filename
            shutil.copy(output_video, public_path)
            
            return {
                "status": "success", 
                "job_id": job_id, 
                "video_url": f"http://localhost:35000/uploads/{public_filename}",
                "debug_log": result_video.stdout
            }
        else:
            return {"status": "failed", "error": "Output video file not found", "log": result_video.stderr}
        
    except Exception as e:
        logging.error(f"Job failed: {e}")
        return {"status": "failed", "error": str(e)}
