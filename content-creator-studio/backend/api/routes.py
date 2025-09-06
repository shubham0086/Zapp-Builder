from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from datetime import datetime
import json

router = APIRouter()

@router.get("/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "operational",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": [
            "/generate-content",
            "/research-only", 
            "/content-only",
            "/workflow-status/{request_id}",
            "/agent-capabilities"
        ]
    }

@router.get("/version")
async def api_version():
    """API version information"""
    return {
        "version": "0.1.0",
        "release_date": "2024-01-15",
        "features": [
            "CrewAI agent orchestration",
            "Multi-platform content generation",
            "Research and lead generation",
            "Personalized outreach"
        ]
    }

@router.get("/platforms")
async def supported_platforms():
    """Get list of supported platforms"""
    return {
        "platforms": [
            {
                "name": "LinkedIn",
                "type": "professional",
                "max_length": 3000,
                "supports_hashtags": True,
                "supports_images": True
            },
            {
                "name": "X (Twitter)",
                "type": "social",
                "max_length": 280,
                "supports_hashtags": True,
                "supports_threads": True
            },
            {
                "name": "Instagram",
                "type": "visual",
                "max_length": 2200,
                "supports_hashtags": True,
                "supports_images": True
            },
            {
                "name": "YouTube",
                "type": "video",
                "max_length": 5000,
                "supports_hashtags": True,
                "supports_thumbnails": True
            },
            {
                "name": "Newsletter",
                "type": "email",
                "max_length": 10000,
                "supports_html": True,
                "supports_images": True
            },
            {
                "name": "Blog",
                "type": "long-form",
                "max_length": 15000,
                "supports_seo": True,
                "supports_images": True
            }
        ]
    }

@router.get("/tones")
async def supported_tones():
    """Get list of supported content tones"""
    return {
        "tones": [
            {
                "name": "Professional",
                "description": "Formal business language, industry expertise focus",
                "best_for": ["LinkedIn", "Newsletter", "Blog"]
            },
            {
                "name": "Casual",
                "description": "Conversational, friendly, approachable tone",
                "best_for": ["Instagram", "X (Twitter)", "YouTube"]
            },
            {
                "name": "Educational",
                "description": "Informative, teaching-focused, expert guidance",
                "best_for": ["YouTube", "Blog", "Newsletter"]
            },
            {
                "name": "Entertaining",
                "description": "Fun, engaging, personality-driven content",
                "best_for": ["Instagram", "X (Twitter)", "YouTube"]
            },
            {
                "name": "Inspirational",
                "description": "Motivational, uplifting, aspirational messaging",
                "best_for": ["LinkedIn", "Instagram", "Newsletter"]
            },
            {
                "name": "Conversational",
                "description": "Direct, personal, like talking to a friend",
                "best_for": ["X (Twitter)", "Instagram", "YouTube"]
            }
        ]
    }

@router.post("/validate-request")
async def validate_content_request(request_data: Dict):
    """Validate a content generation request"""
    required_fields = ["topic", "platforms"]
    missing_fields = []
    
    for field in required_fields:
        if field not in request_data or not request_data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            "valid": False,
            "errors": [f"Missing required field: {field}" for field in missing_fields]
        }
    
    # Validate platforms
    supported_platforms = [
        "LinkedIn", "X (Twitter)", "Instagram", "YouTube", "Newsletter", "Blog"
    ]
    invalid_platforms = []
    
    for platform in request_data["platforms"]:
        if platform not in supported_platforms:
            invalid_platforms.append(platform)
    
    if invalid_platforms:
        return {
            "valid": False,
            "errors": [f"Unsupported platform: {platform}" for platform in invalid_platforms]
        }
    
    return {
        "valid": True,
        "message": "Request validation passed"
    }

@router.get("/examples")
async def get_examples():
    """Get example requests and responses"""
    return {
        "examples": [
            {
                "name": "Basic Content Generation",
                "request": {
                    "topic": "AI productivity tools for remote teams",
                    "tone": "professional",
                    "platforms": ["LinkedIn", "Newsletter"],
                    "research_mode": True,
                    "lead_gen_mode": False
                },
                "description": "Generate professional content with research for LinkedIn and Newsletter"
            },
            {
                "name": "Complete Workflow",
                "request": {
                    "topic": "Sustainable technology trends",
                    "tone": "educational",
                    "platforms": ["YouTube", "Blog"],
                    "research_mode": True,
                    "lead_gen_mode": True,
                    "outreach_mode": True,
                    "target_audience": "Tech professionals and sustainability advocates"
                },
                "description": "Full workflow with research, leads, content, and outreach"
            },
            {
                "name": "Social Media Focus",
                "request": {
                    "topic": "Personal branding for entrepreneurs",
                    "tone": "inspirational",
                    "platforms": ["Instagram", "X (Twitter)"],
                    "include_hashtags": True,
                    "include_cta": True
                },
                "description": "Social media content with hashtags and CTAs"
            }
        ]
    }