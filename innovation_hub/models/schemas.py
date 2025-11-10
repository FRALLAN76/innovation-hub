from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum

class IdeaTypeEnum(str, Enum):
    IDEA = "idé"
    PROBLEM = "problem"
    NEED = "behov"
    IMPROVEMENT = "förbättring"

class IdeaStatusEnum(str, Enum):
    NEW = "ny"
    REVIEWING = "granskning"
    APPROVED = "godkänd"
    IN_DEVELOPMENT = "utveckling"
    IMPLEMENTED = "implementerad"
    REJECTED = "avvisad"

class PriorityEnum(str, Enum):
    LOW = "låg"
    MEDIUM = "medel"
    HIGH = "hög"

class TargetGroupEnum(str, Enum):
    CITIZENS = "medborgare"
    BUSINESSES = "företag"
    EMPLOYEES = "medarbetare"
    OTHER_ORGS = "andra organisationer"

# Base schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    color: str = Field(default="#3498db", pattern=r"^#[0-9a-fA-F]{6}$")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class IdeaBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    type: IdeaTypeEnum
    target_group: TargetGroupEnum

class IdeaCreate(IdeaBase):
    submitter_email: str = Field(..., description="Email of the person submitting the idea")
    tags: List[str] = Field(default=[], description="List of tag names")

class IdeaUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    type: Optional[IdeaTypeEnum] = None
    status: Optional[IdeaStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    target_group: Optional[TargetGroupEnum] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None

class IdeaResponse(IdeaBase):
    id: int
    status: IdeaStatusEnum
    priority: PriorityEnum
    submitter: UserResponse
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    comments: List['CommentResponse'] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Engagement metrics
    vote_count: int = 0

    # AI Analysis results (optional for transparency)
    ai_sentiment: Optional[str] = None
    ai_confidence: Optional[float] = None
    ai_analysis_notes: Optional[str] = None
    service_recommendation: Optional[str] = None
    service_confidence: Optional[float] = None
    service_reasoning: Optional[str] = None
    matching_services: Optional[List[dict]] = None
    development_impact: Optional[str] = None

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str = Field(..., min_length=3, max_length=1000)

class CommentCreate(CommentBase):
    author_id: int = Field(..., description="ID of the comment author")

class CommentResponse(CommentBase):
    id: int
    author: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True

# Statistics schemas
class StatusCount(BaseModel):
    status: IdeaStatusEnum
    count: int

class TypeCount(BaseModel):
    type: IdeaTypeEnum
    count: int

class IdeaStats(BaseModel):
    total_ideas: int
    status_distribution: List[StatusCount]
    type_distribution: List[TypeCount]
    recent_ideas: List[IdeaResponse]

# Filter schemas
class IdeaFilter(BaseModel):
    status: Optional[IdeaStatusEnum] = None
    type: Optional[IdeaTypeEnum] = None
    priority: Optional[PriorityEnum] = None
    target_group: Optional[TargetGroupEnum] = None
    category_id: Optional[int] = None
    submitter_id: Optional[int] = None
    tag: Optional[str] = None
    search: Optional[str] = Field(None, description="Search in title and description")

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)

# Analysis schemas
class ServiceMappingOverview(BaseModel):
    """Overview of how ideas map to existing services"""
    existing_service_count: int = Field(..., description="Ideas that can use existing services")
    develop_existing_count: int = Field(..., description="Ideas requiring development of existing services")
    new_service_count: int = Field(..., description="Ideas requiring completely new services")
    total_ideas_analyzed: int

class ServiceMatch(BaseModel):
    """Service that matches ideas"""
    service_name: str
    service_category: Optional[str]
    idea_count: int
    avg_match_score: float
    ideas: List[dict] = Field(default=[])

class DevelopmentNeed(BaseModel):
    """Idea with its development needs"""
    idea_id: int
    title: str
    priority: PriorityEnum
    service_recommendation: str  # existing_service, develop_existing, new_service
    match_score: float
    impact: str  # low, medium, high

class GapAnalysis(BaseModel):
    """Areas with many ideas but no matching services"""
    area_keywords: List[str]
    idea_count: int
    sample_ideas: List[dict]

class AnalysisStats(BaseModel):
    """Complete analysis statistics"""
    overview: ServiceMappingOverview
    top_matched_services: List[ServiceMatch]
    development_needs: List[DevelopmentNeed]
    gaps: List[GapAnalysis]
    ai_confidence_avg: float