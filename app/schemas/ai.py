from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ContentSource(str, Enum):
    """Supported data sources for scoping downstream AI generation requests."""
    raw_input = "raw_input"
    file = "file"
    document = "document"
    needs_assessment = "needs_assessment"
    curriculum_outline = "curriculum_outline"
    custom_content_1 = "custom_content_1"
    custom_content_2 = "custom_content_2"
    custom_content_3 = "custom_content_3"


class PriorKnowledgeLevel(str, Enum):
    """Target learner competency levels managed via the Analysis dashboard interface."""
    level1 = "level1"
    level2 = "level2"
    level3 = "level3"


class JobRole(str, Enum):
    """Target organizational roles mapped within the audience profile metadata selection."""
    HR = "HR"
    Finance = "Finance"
    IT = "IT"


class PrimaryLanguage(str, Enum):
    """Primary delivery languages supported across localized course execution nodes."""
    english = "english"
    french = "french"


class LearnerLocation(str, Enum):
    """Geographic distribution filters for localized instructional target parameters."""
    india = "india"
    usa = "usa"
    UK = "UK"


class AICurriculumRequest(BaseModel):
    """Unified payload model handling contextual data properties for structural parsing."""
    project_id: int
    title: str
    target_audience: str
    objectives: List[str]
    additional_context: Optional[str] = None


class ModuleItem(BaseModel):
    """Granular module node structure mapping topics and concrete objective points."""
    module_title: str
    duration_hours: float
    description: str
    topics: List[str]
    learning_objectives: List[str]


class AICurriculumResponse(BaseModel):
    """Outbound curriculum schema layout returned directly during structured generations."""
    title: str
    target_audience: str
    objectives: List[str]
    modules: List[ModuleItem]
    summary: str


class AIObjectivesRequest(BaseModel):
    """Payload targeting automated formulation of fine-grained target objectives."""
    project_id: int
    content_source: ContentSource
    content: str
    target_audience_description: str
    prior_knowledge_level: Optional[PriorKnowledgeLevel] = None
    job_roles: Optional[List[JobRole]] = None
    primary_language: Optional[PrimaryLanguage] = None
    learner_location: Optional[LearnerLocation] = None
    additional_context: Optional[str] = None


class AIObjectivesResponse(BaseModel):
    """Collection wrapper passing generated learning objective statement blocks back to client."""
    objectives: List[str]


class InteractivitySuggestion(BaseModel):
    """Structural configuration object tracking instructional presentation suggestions."""
    type: str  # Structural block types: e.g., "Knowledge Check (MCQ)", "Clickable Hotspot"
    description: str
    recommendation: str


class AIInteractivityRequest(BaseModel):
    """Configuration mapping criteria needed to extract interactivity recommendations."""
    project_id: int
    content_source: ContentSource
    content: Optional[str] = None


class AIInteractivityResponse(BaseModel):
    """Outbound collection enclosing structured layout interactive item data entries."""
    suggestions: List[InteractivitySuggestion]


class StoryboardSlide(BaseModel):
    """Data item detailing slide contents, vocal delivery cues, and layout mechanics."""
    slide_id: str
    title: str
    content: str
    narration: str
    duration: str  # Duration formatting string: e.g., "00:30 Sec"
    voiceover: str  # UI flag parameter value: e.g., "Yes" or "No"
    transition: str  # Presentation transition settings: e.g., "Fade"
    visual_prompt: Optional[str] = None


class AIStoryboardRequest(BaseModel):
    """Specifies active context targets and text contents for generating storyboards."""
    project_id: int
    topic_outline: str
    learning_goals: List[str]


class AIStoryboardResponse(BaseModel):
    """Array data payload wrapping output storyboard slide specifications."""
    slides: List[StoryboardSlide]


class ProjectContentSaveRequest(BaseModel):
    """Persists targeted updates against isolated sections within active workspaces."""
    content_key: ContentSource
    title: str
    text: str