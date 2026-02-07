from sqlmodel import Session, select
from database import get_session, create_db_and_tables
from models import Project

def update_examples():
    # Use context manager for session
    session_generator = get_session()
    session = next(session_generator)
    
    try:
        projects = session.exec(select(Project)).all()
        print(f"Found {len(projects)} projects.")
        
        for p in projects:
            if not p.output_video_url:
                print(f"Updating project {p.name} with sample video...")
                p.output_video_url = "http://localhost:35000/uploads/sample_video.mp4"
                session.add(p)
        
        session.commit()
        print("Projects updated successfully.")
        
    finally:
        session.close()

if __name__ == "__main__":
    update_examples()
