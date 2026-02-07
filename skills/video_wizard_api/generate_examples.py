from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Project
import json
import uuid

def create_examples():
    create_db_and_tables()
    
    examples = [
        {
            "name": "Tech Future Intro",
            "selected_component": "ThreeDScene",
            "component_props": {"primaryColor": "#00d2ff", "text": "FUTURE TECH"},
            "theme": "Technology",
            "product_name": "CyberDeck",
            "primary_color": "#00d2ff",
            "secondary_color": "#000000",
            "output_video_url": "http://localhost:35000/uploads/sample_video.mp4"
        },
        {
            "name": "Morning Vibes",
            "selected_component": "TopBottomText",
            "component_props": {
                "topText": "WHEN THE COFFEE", 
                "bottomText": "FINALLY HITS", 
                "imageSrc": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60"
            },
            "theme": "Lifestyle",
            "product_name": "Morning Brew",
            "primary_color": "#6f4e37",
            "secondary_color": "#ffffff",
            "output_video_url": "http://localhost:35000/uploads/sample_video.mp4"
        },
        {
            "name": "Speed Demon",
            "selected_component": "MotionBlurTitle",
            "component_props": {"text": "FAST", "color": "#ff3300"},
            "theme": "Automotive",
            "product_name": "TurboX",
            "primary_color": "#ff3300",
            "secondary_color": "#000000"
        },
        {
            "name": "Retro Gaming",
            "selected_component": "NoiseOverlay",
            "component_props": {"text": "GAME OVER", "noiseOpacity": 0.2},
            "theme": "Retro",
            "product_name": "Arcade Stick",
            "primary_color": "#00ff00",
            "secondary_color": "#000000"
        },
        {
            "name": "Reaction GIF",
            "selected_component": "GifScene",
            "component_props": {
                "gifUrl": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzM0eDk1dm55eDV3ZnJ5eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyM/giphy.gif", 
                "caption": "CODE DEPLOYED"
            },
            "theme": "Developer",
            "product_name": "DevTools",
            "primary_color": "#333333",
            "secondary_color": "#ffffff"
        }
    ]

    with Session(engine) as session:
        for ex in examples:
            project_id = str(uuid.uuid4())
            project = Project(
                id=project_id,
                name=ex["name"],
                theme=ex["theme"],
                product_name=ex["product_name"],
                primary_color=ex["primary_color"],
                secondary_color=ex["secondary_color"],
                selected_component=ex["selected_component"],
                component_props_json=json.dumps(ex["component_props"])
            )
            session.add(project)
            print(f"Created project: {ex['name']} ({project_id})")
        
        session.commit()

if __name__ == "__main__":
    create_examples()
