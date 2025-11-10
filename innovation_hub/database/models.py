from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .connection import Base
import enum

class IdeaType(enum.Enum):
    IDEA = "idé"
    PROBLEM = "problem"
    NEED = "behov"
    IMPROVEMENT = "förbättring"

class IdeaStatus(enum.Enum):
    NEW = "ny"
    REVIEWING = "granskning"
    APPROVED = "godkänd"
    IN_DEVELOPMENT = "utveckling"
    IMPLEMENTED = "implementerad"
    REJECTED = "avvisad"

class Priority(enum.Enum):
    LOW = "låg"
    MEDIUM = "medel"
    HIGH = "hög"

class TargetGroup(enum.Enum):
    CITIZENS = "medborgare"
    BUSINESSES = "företag"
    EMPLOYEES = "medarbetare"
    OTHER_ORGS = "andra organisationer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ideas = relationship("Idea", back_populates="submitter")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    color = Column(String, default="#3498db")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ideas = relationship("Idea", back_populates="category")

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(IdeaType), nullable=False)
    status = Column(Enum(IdeaStatus), default=IdeaStatus.NEW)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    target_group = Column(Enum(TargetGroup), nullable=False)

    # AI Analysis results
    ai_sentiment = Column(String)
    ai_confidence = Column(Float)
    ai_analysis_notes = Column(Text)

    # Service Mapping results
    service_recommendation = Column(String)  # existing_service, develop_existing, new_service
    service_confidence = Column(Float)
    service_reasoning = Column(Text)
    matching_services = Column(JSON)  # Store matched services as JSON
    development_impact = Column(String)  # low, medium, high

    # Engagement metrics
    vote_count = Column(Integer, default=0)

    # Relationships
    submitter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    submitter = relationship("User", back_populates="ideas")
    category = relationship("Category", back_populates="ideas")
    tags = relationship("Tag", secondary="idea_tags", back_populates="ideas")
    comments = relationship("Comment", back_populates="idea")
    votes = relationship("Vote", back_populates="idea", cascade="all, delete-orphan")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ideas = relationship("Idea", secondary="idea_tags", back_populates="tags")

class IdeaTag(Base):
    __tablename__ = "idea_tags"

    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    # Relationships
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    idea = relationship("Idea", back_populates="comments")
    author = relationship("User")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    idea = relationship("Idea", back_populates="votes")
    user = relationship("User")

    created_at = Column(DateTime(timezone=True), server_default=func.now())