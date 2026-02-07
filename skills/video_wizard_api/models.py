from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel

# Shared properties
class ReferenceBase(SQLModel):
    url: str
    type: str = "image"
    rating: Optional[str] = None
    comment: Optional[str] = None
    style_name: Optional[str] = None

class Reference(ReferenceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[str] = Field(default=None, foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="references")

class ProjectBase(SQLModel):
    name: str = ""
    theme: str = ""
    product_name: str = ""
    target_audience: str = ""
    primary_color: str = ""
    secondary_color: str = ""
    niche: str = ""
    logo_path: Optional[str] = None
    current_step: int = 1

class Project(ProjectBase, table=True):
    id: str = Field(primary_key=True)
    keywords_json: str = "[]" # Store as JSON string since SQLite/SQLModel simple handling
    emotions_json: str = "[]"
    context_photos_json: str = "[]"
    
    references: List["Reference"] = Relationship(back_populates="project")

    @property
    def keywords(self):
        import json
        return json.loads(self.keywords_json)
    
    @keywords.setter
    def keywords(self, value):
        import json
        self.keywords_json = json.dumps(value)

    @property
    def emotions(self):
        import json
        return json.loads(self.emotions_json)
    
    @emotions.setter
    def emotions(self, value):
        import json
        self.emotions_json = json.dumps(value)

    @property
    def context_photos(self):
        import json
        return json.loads(self.context_photos_json)
    
    @context_photos.setter
    def context_photos(self, value):
        import json
        self.context_photos_json = json.dumps(value)

# Pydantic models for API (to handle lists correctly without manual JSON conversion in endpoints)
class ProjectCreate(ProjectBase):
    id: Optional[str] = None
    keywords: List[str] = []
    emotions: List[str] = []

class ProjectUpdate(ProjectBase):
    keywords: List[str] = []
    emotions: List[str] = []
    context_photos: List[str] = []
    references: List[ReferenceBase] = []

class ProjectRead(ProjectBase):
    id: str
    keywords: List[str] = []
    emotions: List[str] = []
    context_photos: List[str] = []
    references: List[ReferenceBase] = []

class ImageSuggestion(BaseModel):
    url: str
    source: str
    description: str

class VideoGenerationRequest(BaseModel):
    project_id: str
    selected_images: List[str]
    script_text: Optional[str] = None
