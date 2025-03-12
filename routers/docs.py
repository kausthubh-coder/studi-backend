from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import os
import markdown
from .auth import get_current_active_user, User

# Create router
router = APIRouter()

# Models
class DocCategory(BaseModel):
    id: str
    name: str
    description: str
    icon: str

class DocItem(BaseModel):
    id: str
    category_id: str
    title: str
    path: str
    summary: Optional[str] = None

class DocContent(BaseModel):
    id: str
    title: str
    content: str
    toc: List[dict]
    last_updated: str

# Mock database - in a real app, this would be a database
doc_categories = [
    {
        "id": "architecture",
        "name": "Architecture",
        "description": "System architecture and design documentation",
        "icon": "cube"
    },
    {
        "id": "user-guides",
        "name": "User Guides",
        "description": "Guides for using the Studi platform",
        "icon": "book-open"
    },
    {
        "id": "development",
        "name": "Development",
        "description": "Documentation for developers",
        "icon": "code"
    },
    {
        "id": "api",
        "name": "API Documentation",
        "description": "API reference and usage examples",
        "icon": "server"
    },
    {
        "id": "deployment",
        "name": "Deployment & Operations",
        "description": "Deployment guides and operational procedures",
        "icon": "cloud"
    },
    {
        "id": "security",
        "name": "Security & Compliance",
        "description": "Security documentation and compliance information",
        "icon": "shield-check"
    }
]

doc_items = [
    {
        "id": "architecture-overview",
        "category_id": "architecture",
        "title": "Architecture Overview",
        "path": "/docs/ARCHITECTURE.md",
        "summary": "Overview of the Studi system architecture"
    },
    {
        "id": "agent-architecture",
        "category_id": "architecture",
        "title": "Agent Architecture",
        "path": "/docs/AGENT_ARCHITECTURE.md",
        "summary": "Details of the multi-agent AI system"
    },
    {
        "id": "memory-system",
        "category_id": "architecture",
        "title": "Memory System",
        "path": "/docs/MEMORY_SYSTEM.md",
        "summary": "Documentation of the multi-layered memory system"
    },
    {
        "id": "web-architecture",
        "category_id": "architecture",
        "title": "Web Architecture",
        "path": "/docs/WEB_ARCHITECTURE.md",
        "summary": "Web application architecture and components"
    },
    {
        "id": "getting-started",
        "category_id": "user-guides",
        "title": "Getting Started",
        "path": "/docs/user-guides/GETTING_STARTED.md",
        "summary": "Guide for new users to get started with Studi"
    },
    {
        "id": "canvas-integration",
        "category_id": "user-guides",
        "title": "Canvas LMS Integration",
        "path": "/docs/user-guides/CANVAS_INTEGRATION.md",
        "summary": "How to connect Studi with Canvas LMS"
    },
    {
        "id": "study-guide-creation",
        "category_id": "user-guides",
        "title": "Creating Study Guides",
        "path": "/docs/user-guides/STUDY_GUIDES.md",
        "summary": "How to create and use personalized study guides"
    },
    {
        "id": "api-overview",
        "category_id": "api",
        "title": "API Overview",
        "path": "/docs/api/OVERVIEW.md",
        "summary": "Overview of the Studi API"
    },
    {
        "id": "authentication",
        "category_id": "api",
        "title": "Authentication",
        "path": "/docs/api/AUTHENTICATION.md",
        "summary": "API authentication methods and examples"
    },
    {
        "id": "deployment-guide",
        "category_id": "deployment",
        "title": "Deployment Guide",
        "path": "/docs/DEPLOYMENT.md",
        "summary": "Guide for deploying Studi in production"
    }
]

# Mock document content - in a real app, this would be read from files
doc_content = {
    "architecture-overview": {
        "id": "architecture-overview",
        "title": "Architecture Overview",
        "content": """
# Architecture Overview

Studi is built on a modern, scalable architecture designed to provide a seamless learning experience.

## Core Components

- **Multi-Agent AI System**: Specialized AI agents for planning, knowledge creation, and task execution
- **Memory System**: Multi-layered memory for context retention and knowledge creation
- **Web Application**: React frontend with FastAPI backend
- **Canvas LMS Integration**: Seamless connection to Canvas courses and assignments

## System Diagram

```
User <-> Web App <-> API Gateway <-> Agent System <-> Memory System
                                  <-> Canvas API
```

## Data Flow

1. User interacts with the web application
2. Requests are processed by the API Gateway
3. The Agent System handles complex tasks using specialized agents
4. The Memory System stores and retrieves relevant information
5. Canvas API integration provides access to course materials and assignments
""",
        "toc": [
            {"level": 1, "title": "Architecture Overview", "id": "architecture-overview"},
            {"level": 2, "title": "Core Components", "id": "core-components"},
            {"level": 2, "title": "System Diagram", "id": "system-diagram"},
            {"level": 2, "title": "Data Flow", "id": "data-flow"}
        ],
        "last_updated": "2023-06-15"
    }
}

# Routes
@router.get("/categories", response_model=List[DocCategory])
async def get_doc_categories():
    """
    Get all documentation categories.
    """
    return doc_categories

@router.get("/items", response_model=List[DocItem])
async def get_doc_items(category_id: Optional[str] = None):
    """
    Get documentation items, optionally filtered by category.
    """
    if category_id:
        return [item for item in doc_items if item["category_id"] == category_id]
    return doc_items

@router.get("/content/{doc_id}", response_model=DocContent)
async def get_doc_content(doc_id: str):
    """
    Get the content of a specific documentation item.
    """
    if doc_id not in doc_content:
        # In a real app, this would read from a file or database
        # For now, return a 404 if the document is not in our mock data
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {doc_id} not found"
        )
    
    return doc_content[doc_id]

@router.get("/search")
async def search_docs(query: str):
    """
    Search documentation content.
    """
    # In a real app, this would perform a full-text search
    # For now, just do a simple string match on titles and summaries
    results = []
    
    for item in doc_items:
        if (
            query.lower() in item["title"].lower() or 
            (item.get("summary") and query.lower() in item["summary"].lower())
        ):
            results.append(item)
    
    return results 