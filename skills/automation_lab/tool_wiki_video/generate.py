import cv2
import numpy as np
from PIL import ImageEnhance
from PIL import Image
import glob
from moviepy.editor import *
import imageio
import requests
import wikipedia
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from gtts import gTTS
import os

output_name = ''

def save_image(image_url, im_name):
    try:
        img_data = requests.get(image_url).content
        if not os.path.exists('./images'):
            os.makedirs('./images')
        with open('./images/'+im_name, 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(f"Error saving image: {e}")

def random_page(lang):
   global output_name
   wikipedia.set_lang(lang)
   # Fetch random page title first
   try:
       random_title = wikipedia.random(1)
       print(f"Random title fetched: {random_title}")
       page = wikipedia.page(random_title)
       if len(page.images) < 4:
           print(f"Not enough images ({len(page.images)}), retrying...")
           return random_page(lang)
       else:
           images = page.images
           output_name = page.title.replace(':', '', 10)
           print(f"Processing: {output_name}")
           
           # Ensure images dir exists
           if not os.path.exists('./images'):
               os.makedirs('./images')
               
           for image in images:
               filename = image.split('/')[-1]
               if not filename: continue
               save_image(image, filename)
               if 'svg' in image:
                   try:
                       drawing = svg2rlg('./images/'+filename)
                       renderPM.drawToFile(drawing, './images/'+filename + ".jpg", fmt="JPG")
                   except:
                       pass

           return page.summary
   except Exception as e:
       print(f"Error fetching page: {e}, retrying...")
       return random_page(lang)

def generate(lang):
    global output_name
    text = random_page(lang)
    if not text:
        print("Failed to get text")
        return

    print("Generating audio...")
    tts = gTTS(text, lang=lang)
    tts.save('audio.mp3')

    RESOLUTION = (800, 600) # Tuple, not set
    images = []
    for filename in glob.glob('./images/*.jpg'):
        images.append(filename)
    
    # Fallback if no jpgs
    if not images:
         for filename in glob.glob('./images/*'):
             if filename.lower().endswith(('.png', '.jpeg', '.bmp')):
                 images.append(filename)

    if not images:
        print("No images found!")
        return

    IMAGE_NUMBER = len(images)
    
    try:
        audioclip = AudioFileClip("audio.mp3")
        duration = audioclip.duration
        seconds = duration
        fps = 30
        
        total_frames = int(seconds * fps)
        FRAMES_PER_IMAGE = total_frames / IMAGE_NUMBER
        
        if not os.path.exists('output'):
            os.makedirs('output')
            
        write_to = 'output/{}.mp4'.format(output_name.replace(' ', '_'))
        writer = imageio.get_writer(write_to, format='mp4', mode='I', fps=fps)

        current_image = 0
        next_change = FRAMES_PER_IMAGE
        
        for i in range(total_frames):
            if current_image >= len(images):
                current_image = 0
                
            im = Image.open(images[current_image])
            im = im.resize(RESOLUTION)
            
            if i >= next_change:
                current_image += 1
                next_change += FRAMES_PER_IMAGE
                if current_image >= len(images):
                    current_image = 0
            
            im_np = np.array(im)
            writer.append_data(im_np)
            
        writer.close()
        
        # Add audio using MoviePy
        final_clip = VideoFileClip(write_to)
        final_clip = final_clip.set_audio(audioclip)
        final_clip.write_videofile(write_to.replace('.mp4', '_audio.mp4'), codec='libx264', audio_codec='aac')
        
    except Exception as e:
        print(f"Error generating video: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='O Professor Infinito - Gerador de Vídeos Wiki')
    parser.add_argument('--lang', type=str, default='pt', help='Idioma da Wikipedia (ex: pt, en)')
    parser.add_argument('--auto', action='store_true', help='Executa automaticamente sem perguntar')
    
    args = parser.parse_args()
    
    print(f"🎓 O Professor Infinito: Inicializando em '{args.lang}'...")
    
    # Se a flag --auto for passada ou se o usuário estiver apenas testando
    if args.auto:
        generate(args.lang)
    else:
        # Modo interativo simples se rodado direto
        print("Para gerar um vídeo, use: python3 generate.py --auto --lang pt")
        confirm = input("Deseja gerar um vídeo aleatório agora? (s/n): ")
        if confirm.lower() == 's':
            generate(args.lang)
