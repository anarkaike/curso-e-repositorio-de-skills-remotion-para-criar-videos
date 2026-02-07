from typing import List, Optional, Dict, Any
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
    selected_component: str = "PortraitVideo"
    output_video_url: Optional[str] = None

class Project(ProjectBase, table=True):
    id: str = Field(primary_key=True)
    keywords_json: str = "[]" # Store as JSON string since SQLite/SQLModel simple handling
    emotions_json: str = "[]"
    context_photos_json: str = "[]"
    component_props_json: str = "{}"
    
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

    @property
    def component_props(self):
        import json
        return json.loads(self.component_props_json)

    @component_props.setter
    def component_props(self, value):
        import json
        self.component_props_json = json.dumps(value)

# Pydantic models for API (to handle lists correctly without manual JSON conversion in endpoints)
class ProjectCreate(ProjectBase):
    id: Optional[str] = None
    keywords: List[str] = []
    emotions: List[str] = []
    component_props: Dict[str, Any] = {}

class ProjectUpdate(ProjectBase):
    keywords: List[str] = []
    emotions: List[str] = []
    context_photos: List[str] = []
    references: List[ReferenceBase] = []
    component_props: Dict[str, Any] = {}

class ProjectRead(ProjectBase):
    id: str
    keywords: List[str] = []
    emotions: List[str] = []
    context_photos: List[str] = []
    references: List[ReferenceBase] = []
    component_props: Dict[str, Any] = {}

class ImageSuggestion(BaseModel):
    url: str
    source: str
    description: str

class VideoGenerationRequest(BaseModel):
    project_id: str
    selected_images: List[str]
    script_text: Optional[str] = None

class KnowledgeEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query_text: str = Field(index=True)
    suggestion_type: str = Field(index=True)
    response_json: str
    embedding_json: str # Store as JSON list of floats
    created_at: float
