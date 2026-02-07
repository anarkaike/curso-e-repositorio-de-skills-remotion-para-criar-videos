import os
import requests

photos_dir = "/Users/junio/Documents/PROJETOS/videos-programaticos/projects/disk_uniformes/photos"
os.makedirs(photos_dir, exist_ok=True)

# Define keywords for each scene
images = [
    ("1.jpg", "https://loremflickr.com/1080/1920/school,building"),
    ("2.jpg", "https://loremflickr.com/1080/1920/mother,child,school"),
    ("3.jpg", "https://loremflickr.com/1080/1920/children,running"),
    ("4.jpg", "https://loremflickr.com/1080/1920/embroidery,sewing"),
    ("5.jpg", "https://loremflickr.com/1080/1920/student,happy"),
]

for filename, url in images:
    path = os.path.join(photos_dir, filename)
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Saved {filename}")
        else:
            print(f"Failed to download {filename}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
