import os
import json
import re
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip 
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ColorClip
import math
import gc
import tracemalloc
from multiprocessing import Pool
import subprocess
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import shutil
import logging

from pathlib import Path


logging.basicConfig(level=logging.DEBUG, filename='video_processing.log')


output_width, output_height = 1080, 1920
font_size = 80
tracemalloc.start()

def find_files_with_extension(directory: Path, extension: str) -> list[Path]:
    """
    Finds all files with the specified extension in the given directory.

    :param directory: Directory to search in.
    :param extension: File extension to search for.
    :return: List of Path objects for matching files.
    """
    return sorted(file for file in directory.glob(f'*{extension}') if file.is_file())


def find_directory_path(base_directory, target_dir_name):
    """
    Recursively finds a directory by name starting from the base directory.

    :param base_directory: The root directory to start searching from (Path or str).
    :param target_dir_name: The directory name to search for.
    :return: Path object of the target directory.
    :raises FileNotFoundError: If the target directory is not found.
    """
    base_directory = Path(base_directory)  # Ensure base_directory is a Path object
    for path in base_directory.rglob("*"):
        if path.is_dir() and path.name == target_dir_name:
            return path
    raise FileNotFoundError(f"Directory '{target_dir_name}' not found in '{base_directory}'")




def clean_and_split(text):
    """Remove punctuation and split into words for case-insensitive comparison."""
    return re.findall(r'\b\w+\b', text.lower())

def find_file_in_directory(directory: Path, file_name: str) -> Path:
    """
    Recursively finds a specific file by name in a directory.

    :param directory: Directory to search in.
    :param file_name: Name of the file to locate.
    :return: Path object of the found file.
    :raises FileNotFoundError: If the file is not found.
    """
    for path in directory.rglob(file_name):
        if path.is_file():
            return path
    raise FileNotFoundError(f"File '{file_name}' not found in '{directory}'")


def add_audio_to_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(str(video_path))
    audio_clip = AudioFileClip(str(audio_path))
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(str(output_path), codec="libx264", audio_codec="aac")
    audio_clip.close()
    video_clip.close()
    final_clip.close()


def cleanup_temp_files(directory, exclude_files):
    """
    Cleans up all files in a directory except those explicitly excluded.

    :param directory: The directory to clean up (Path or str).
    :param exclude_files: List of filenames to exclude from deletion.
    """
    directory = Path(directory)  # Ensure the directory is a Path object
    for file in directory.iterdir():
        if file.is_file() and file.name not in exclude_files:
            file.unlink()  # Deletes the file
            logging.debug(f"Deleted temporary file: {file}")



# video_directory = 'video'
# exclude_files = ['final_video_with_audio.mp4']
# cleanup_temp_files(video_directory, exclude_files)


# current_directory = os.getcwd()

# # Discover JSON file
# aligned_scripts_directory = find_directory_path(current_directory, 'aligned_script_with_timestamps')
# if not aligned_scripts_directory:
#     raise FileNotFoundError("The 'aligned_script_with_timestamps' directory was not found in the current directory.")

# json_files = find_files_with_extension(aligned_scripts_directory, '.json')
# if not json_files:
#     raise FileNotFoundError("No JSON file found in the 'aligned_script_with_timestamps' directory.")
# json_path = json_files[0]  # Assuming the first found JSON file is the one we want

# # Proceed as before with reading the JSON file
# with open(json_path, 'r') as f:
#     data = json.load(f)

# # Discover directories for photos and audio
# photos_directory = find_directory_path(current_directory, 'photos')
# audio_directory = find_directory_path(current_directory, 'audio')

# if not photos_directory:
#     raise FileNotFoundError("Photos directory not found.")
# if not audio_directory:
#     raise FileNotFoundError("Audio directory not found.")

# # List and sort photo files
# photo_paths = [os.path.join(photos_directory, photo) for photo in sorted(os.listdir(photos_directory)) if photo.lower().endswith(('.webp', '.png', '.jpg', '.jpeg'))]

# # Handling multiple audio files by selecting the most recently modified one
# audio_files = [os.path.join(audio_directory, f) for f in os.listdir(audio_directory) if f.endswith('.mp3')]
# audio_path = max(audio_files, key=os.path.getmtime) if audio_files else None

# if not audio_path:
#     raise FileNotFoundError("No audio file found in the audio directory.")




def load_color_coding(colors_file_path: Path):
    """Load color coding from a file. Supports both complex 'word, color' lists and simple key-value pairs."""
    color_coding = {}
    with colors_file_path.open('r') as color_file:
        for line in color_file:
            line = line.strip()
            if not line:
                continue
            
            # Try parsing legacy complex format: Key: "word, color; word2, color2"
            if '"' in line:
                try:
                    color_definitions = line.split('"')[1].split('; ')
                    for color_definition in color_definitions:
                        if ', ' in color_definition:
                            word, color = color_definition.split(', ')
                            color_coding[word.lower()] = color
                except IndexError:
                    logging.warning(f"Could not parse line in complex format: {line}")
            
            # Try parsing simple format: word: color or key: color
            elif ':' in line:
                try:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    # If the key is 'primary' or 'secondary', we might want to map it differently
                    # But for now, let's just add it to the map so if a word matches 'primary', it gets that color.
                    # Ideally, we want to apply primary color to keywords.
                    color_coding[key] = value
                except ValueError:
                    logging.warning(f"Could not parse line in simple format: {line}")
                    
    return color_coding

# # Use the function to load the color coding
# colors_directory = find_directory_path(current_directory, 'colors')
# if not colors_directory:
#     raise FileNotFoundError("Colors directory not found.")

# colors_file_path = find_file_in_directory(colors_directory, 'colors.txt')
# if not colors_file_path:
#     raise FileNotFoundError("colors.txt file not found in the colors directory.")

# color_coding = load_color_coding(colors_file_path)





def zoom_photo_to_fit(photo, output_width=1080, output_height=1920):
    """
    Zoom and crop the photo to fit a 9:16 aspect ratio.

    :param photo: PIL Image object.
    :param output_width: Target width.
    :param output_height: Target height.
    :return: Resized and cropped PIL Image.
    """
    target_ratio = output_width / output_height
    photo_ratio = photo.width / photo.height

    if photo_ratio > target_ratio:
        new_width = int(photo.height * target_ratio)
        left = (photo.width - new_width) / 2
        right = left + new_width
        top, bottom = 0, photo.height
    else:
        new_height = int(photo.width / target_ratio)
        top = (photo.height - new_height) / 2
        bottom = top + new_height
        left, right = 0, photo.width

    return photo.crop((left, top, right, bottom)).resize((output_width, output_height), Image.Resampling.LANCZOS)



def create_subtitle_image(text, color_coding, font_size, output_width, output_height, font_path):
    image = Image.new("RGBA", (output_width, output_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(font_path), size=font_size)

    words = text.split()
    word_details = [(word, draw.textbbox((0, 0), word, font), color_coding.get(word.lower(), "white")) for word in words]

    max_ascent = max(box[3] - box[1] for _, box, _ in word_details)
    max_descent = max(box[3] for _, box, _ in word_details)
    baseline = (output_height - max_ascent + max_descent) / 2

    total_width = sum(box[2] - box[0] for _, box, _ in word_details) + (len(words) - 1) * 10
    current_x = (output_width - total_width) / 2

    outline_thickness = 10

    for word, box, color in word_details:
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                if dx**2 + dy**2 <= outline_thickness**2:
                    draw.text((current_x + dx, baseline - max_descent + dy), word, font=font, fill="black")
        
        draw.text((current_x, baseline - max_descent), word, font=font, fill=color)
        current_x += box[2] - box[0] + 10

    del draw
    return image


def adjust_video_duration(video_clip, expected_duration, fps=30):
    # Calculate the number of frames that should ideally be present
    ideal_frame_count = int(round(expected_duration * fps))
    
    # Calculate the new duration that fits exactly the number of whole frames
    new_duration = ideal_frame_count / fps
    
    # Set the duration to exactly fit the number of frames
    return video_clip.set_duration(new_duration)


def create_overlay_image(output_width, output_height, branding, font_path):
    if not branding:
        return None
        
    image = Image.new("RGBA", (output_width, output_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(str(font_path), size=40)
    except:
        font = ImageFont.load_default()
    
    template = branding.get("template", "simple")
    header_text = branding.get("header_text", "")
    footer_text = branding.get("footer_text", "")
    
    if template == "corporate":
        # Footer Bar
        draw.rectangle([(0, output_height - 150), (output_width, output_height)], fill=(0, 0, 0, 200))
        if footer_text:
             bbox = draw.textbbox((0, 0), footer_text, font=font)
             w = bbox[2] - bbox[0]
             draw.text(((output_width - w)/2, output_height - 100), footer_text, font=font, fill="white")
             
        # Header Bar
        if header_text:
             draw.rectangle([(0, 0), (output_width, 150)], fill=(0, 0, 0, 200))
             bbox = draw.textbbox((0, 0), header_text, font=font)
             w = bbox[2] - bbox[0]
             draw.text(((output_width - w)/2, 50), header_text, font=font, fill="white")
             
    elif template == "bold":
        # Thick Border
        border_w = 40
        draw.rectangle([(0,0), (output_width, output_height)], outline="yellow", width=border_w)
        if footer_text:
             draw.rectangle([(0, output_height - 200), (output_width, output_height)], fill="yellow")
             try:
                font_bold = ImageFont.truetype(str(font_path), size=60)
             except:
                font_bold = font
             bbox = draw.textbbox((0, 0), footer_text, font=font_bold)
             w = bbox[2] - bbox[0]
             draw.text(((output_width - w)/2, output_height - 140), footer_text, font=font_bold, fill="black")

    return image


def generate_subtitle_clips_with_audio(fragment, photo_path: Path, audio_path: Path, color_coding, font_size, font_path: Path, output_width, output_height, output_directory: Path, index, branding=None):
    """
    Generates video clips with subtitles and audio.
    """
    line = fragment['lines'][0].strip()
    start_time = float(fragment['begin'])
    end_time = float(fragment['end'])
    duration = end_time - start_time

    if not photo_path.exists():
        print(f"Warning: Image not found {photo_path}. Using placeholder.")
        # Create a placeholder image
        temp_photo_path = output_directory / f"placeholder_{index}.jpg"
        img = Image.new('RGB', (output_width, output_height), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), "Image Missing", fill=(255,255,0))
        img.save(temp_photo_path)
    else:
        # Preprocess the photo with PIL to ensure compatibility
        temp_photo_path = output_directory / f"temp_photo_{index}.jpg"
        try:
            with Image.open(photo_path) as img:
                img = img.convert("RGB")  # Ensure compatibility with ImageClip
                img = zoom_photo_to_fit(img, output_width, output_height)  # Adjust image to match aspect ratio
                img.save(temp_photo_path, format="JPEG")  # Save as JPEG to ensure compatibility
        except Exception as e:
            print(f"Error processing image {photo_path}: {e}. Using placeholder.")
            img = Image.new('RGB', (output_width, output_height), color=(100, 100, 100))
            d = ImageDraw.Draw(img)
            d.text((50, output_height//2), "Image Error", fill=(255,255,255))
            img.save(temp_photo_path)

    # Verify the temporary photo path exists
    if not temp_photo_path.exists():
        raise FileNotFoundError(f"Temporary photo file not created: {temp_photo_path}")

    # Use the preprocessed photo in ImageClip
    photo_clip = ImageClip(str(temp_photo_path)).set_duration(duration).set_position("center")

    words = clean_and_split(line)
    word_groups = [' '.join(words[i:i + 3]) for i in range(0, len(words), 3)]
    group_duration = duration / max(len(word_groups), 1)

    video_clips = [photo_clip]
    
    # Add Overlay if branding exists
    if branding:
        overlay_img = create_overlay_image(output_width, output_height, branding, font_path)
        if overlay_img:
            overlay_path = output_directory / f"overlay_{index}.png"
            overlay_img.save(overlay_path)
            overlay_clip = ImageClip(str(overlay_path)).set_duration(duration).set_position("center")
            video_clips.append(overlay_clip)

    for i, group in enumerate(word_groups):
        subtitle_image = create_subtitle_image(group, color_coding, font_size, output_width, 300, font_path)
        subtitle_image_path = output_directory / f"subtitle_{index}_{i}.png"
        subtitle_image.save(subtitle_image_path, format="PNG")

        group_start_time = start_time + i * group_duration
        
        # Position at the bottom with some padding (e.g., 100 pixels from bottom)
        # Using a tuple for (x, y) position
        subtitle_clip = ImageClip(str(subtitle_image_path))\
            .set_duration(group_duration)\
            .set_position(('center', 0.85), relative=True)\
            .set_start(group_start_time - start_time)
            
        video_clips.append(subtitle_clip)

    # Get the audio for the entire fragment duration
    fragment_audio_clip = AudioFileClip(str(audio_path)).subclip(start_time, end_time)
    
    final_video_clip = CompositeVideoClip(video_clips).set_audio(fragment_audio_clip)
    segment_path = output_directory / f"segment_{index}.mp4"
    final_video_clip.write_videofile(str(segment_path), fps=30, codec='libx264', audio_codec='aac')

    # Cleanup temporary files
    temp_photo_path.unlink(missing_ok=True)
    if branding:
        Path(output_directory / f"overlay_{index}.png").unlink(missing_ok=True)
    for subtitle_path in output_directory.glob(f"subtitle_{index}_*.png"):
        subtitle_path.unlink(missing_ok=True)

    return [segment_path]





def adjust_audio_sample_rate(audio_clip, target_sample_rate=48000):
    current_sample_rate = audio_clip.fps
    if current_sample_rate != target_sample_rate:
        return audio_clip.set_fps(target_sample_rate)
    return audio_clip


def verify_segment_duration(segment, expected_duration):
    actual_duration = segment.duration
    if not math.isclose(actual_duration, expected_duration, abs_tol=0.001):
        print(f"Duration mismatch detected: Expected {expected_duration}, got {actual_duration}")

def concatenate_segments(segment_paths: list[Path], output_path: Path):
    """
    Concatenates video segments into a single video.

    :param segment_paths: List of Path objects for video segments.
    :param output_path: Path for the concatenated output video.
    """
    filelist_path = output_path.parent / 'filelist.txt'
    try:
        with filelist_path.open('w') as filelist:
            for path in segment_paths:
                filelist.write(f"file '{path}'\n")
                logging.debug(f"Added {path} to filelist for concatenation.")
        ffmpeg_command = [
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', str(filelist_path),
            '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', str(output_path)
        ]
        logging.info(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")
        subprocess.run(ffmpeg_command, check=True)
        logging.info(f"Concatenated video created at: {output_path}")
    except Exception as e:
        logging.error(f"Failed during concatenation: {e}", exc_info=True)
        raise


# output_directory = '/home/idontloveyou/Desktop/AiVideoAutomation/code/test/video'
# os.makedirs(output_directory, exist_ok=True)

# # Define paths for concatenated video and final output video
# concatenated_video_path = os.path.join(output_directory, 'final_video.mp4')
# final_output_path_with_audio = os.path.join(output_directory, 'final_video_with_audio.mp4')

# # Initialize memory tracking before processing fragments
# snapshot_before = tracemalloc.take_snapshot()
# print("[Memory Usage - Before processing fragments]")

# all_segment_paths = []  # Store all segment paths for concatenation

# args_list = []
# for index, fragment in enumerate(data['fragments']):
#     if fragment['lines'] and fragment['lines'][0].strip():
#         line = fragment['lines'][0].strip()
#         photo_path = photo_paths[index % len(photo_paths)]
#         args = (fragment, photo_path, audio_path, color_coding, font_size, "/home/idontloveyou/Desktop/AiVideoAutomation/code/test/font/NeueHaasDisplayBold.ttf", output_width, output_height, output_directory, index)
#         args_list.append(args)

def process_fragment(args):
    return generate_subtitle_clips_with_audio(*args)


if __name__ == '__main__':
    current_directory = Path.cwd()  # Use Path instead of os.getcwd()

    # Dynamically find directories and files
    aligned_scripts_directory = find_directory_path(current_directory, 'aligned_script_with_timestamps')
    json_files = find_files_with_extension(aligned_scripts_directory, '.json')
    json_path = json_files[0]  # First JSON file
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    photos_directory = find_directory_path(current_directory, 'photos')
    audio_directory = find_directory_path(current_directory, 'audio')
    colors_directory = find_directory_path(current_directory, 'colors')
    
    try:
        font_directory = find_directory_path(current_directory, 'font')
        font_path = find_file_in_directory(font_directory, 'NeueHaasDisplayBold.ttf')
    except FileNotFoundError:
        font_path = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
        if not font_path.exists():
             font_path = Path("/System/Library/Fonts/Helvetica.ttc")

    photo_paths = sorted([
        p for p in photos_directory.iterdir() 
        if p.suffix.lower() in ('.webp', '.png', '.jpg', '.jpeg')
    ])
    
    audio_files = sorted(audio_directory.glob('*.mp3'))
    audio_path = max(audio_files, key=lambda f: f.stat().st_mtime)

    colors_file_path = find_file_in_directory(colors_directory, 'colors.txt')
    
    color_coding = load_color_coding(colors_file_path)

    branding = {}
    branding_path = current_directory / 'branding.json'
    if branding_path.exists():
        with open(branding_path, 'r') as f:
            branding = json.load(f)

    output_directory = current_directory / 'video_output'
    output_directory.mkdir(parents=True, exist_ok=True)

    concatenated_video_path = output_directory / 'final_video.mp4'
    final_output_path_with_audio = output_directory / 'final_video_with_audio.mp4'

    args_list = [
        (fragment, photo_paths[index % len(photo_paths)], audio_path, color_coding, font_size, str(font_path), output_width, output_height, output_directory, index, branding)
        for index, fragment in enumerate(data['fragments'])
        if fragment['lines'] and fragment['lines'][0].strip()
    ]

    with Pool() as pool:
        results = pool.map(process_fragment, args_list)

    all_segment_paths = [path for sublist in results for path in sublist]
    concatenate_segments(all_segment_paths, concatenated_video_path)
    add_audio_to_video(concatenated_video_path, audio_path, final_output_path_with_audio)
    cleanup_temp_files(output_directory, exclude_files=[final_output_path_with_audio.name])

