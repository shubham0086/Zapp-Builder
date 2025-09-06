from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import asyncio
from loguru import logger

from api.routes import router
from core.config import settings
from core.database import create_tables
from agents.crew_manager import ContentCreationCrew

# Configure logger
logger.add("logs/app.log", rotation="1 day", retention="7 days", level="INFO")

# Request/Response Models
class ContentGenerationRequest(BaseModel):
    topic: str = Field(..., description="The topic for content generation")
    tone: str = Field("professional", description="Tone of the content")
    platforms: List[str] = Field(..., description="Target platforms for content")
    content_length: str = Field("medium", description="Length of content (short/medium/long)")
    research_mode: bool = Field(True, description="Whether to include research phase")
    lead_gen_mode: bool = Field(False, description="Whether to include lead generation")
    outreach_mode: bool = Field(False, description="Whether to include outreach generation")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    include_hashtags: bool = Field(True, description="Include hashtags in content")
    include_cta: bool = Field(True, description="Include call-to-action")
    include_sources: bool = Field(True, description="Include source citations")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for agents")

class ContentGenerationResponse(BaseModel):
    request_id: str
    status: str
    success: bool
    topic: str
    platforms: List[str]
    research_brief: Optional[str] = None
    leads: Optional[List[Dict]] = None
    content: Optional[Dict[str, str]] = None
    outreach_messages: Optional[List[Dict]] = None
    sources: Optional[List[str]] = None
    workflow_steps: List[str] = []
    total_duration: Optional[str] = None
    error: Optional[str] = None
    created_at: str

class WorkflowStatusResponse(BaseModel):
    request_id: str
    status: str
    progress: int
    message: str
    results: Optional[Dict] = None

# Global crew manager
crew_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global crew_manager
    
    logger.info("🚀 Starting Content Creator Studio API...")
    
    try:
        # Initialize database
        await create_tables()
        logger.info("📊 Database initialized")
        
        # Initialize CrewAI manager
        crew_manager = ContentCreationCrew()
        logger.info("🤖 CrewAI agents initialized")
        
        logger.info("✅ Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Application startup failed: {str(e)}")
        raise e
    
    yield
    
    logger.info("👋 Shutting down Content Creator Studio API...")

# FastAPI app
app = FastAPI(
    title="Content Creator Studio API",
    description="AI-powered content creation and lead generation platform with CrewAI agents",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Content Creator Studio API",
        "version": "0.1.0",
        "status": "operational",
        "features": [
            "AI-powered research",
            "Lead generation",
            "Multi-platform content creation",
            "Personalized outreach"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    global crew_manager
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "database": "connected",
        "agents": "ready" if crew_manager else "not initialized"
    }
    
    # Check agent capabilities
    if crew_manager:
        try:
            capabilities = crew_manager.get_agent_capabilities()
            health_status["agent_capabilities"] = len(capabilities)
        except Exception as e:
            health_status["agents"] = f"error: {str(e)}"
            health_status["status"] = "degraded"
    
    return health_status

@app.post("/api/v1/generate-content", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Main content generation endpoint using CrewAI agents
    Orchestrates research, lead generation, content creation, and outreach
    """
    global crew_manager
    
    if not crew_manager:
        raise HTTPException(
            status_code=503, 
            detail="CrewAI agents not initialized. Please try again later."
        )
    
    logger.info(f"📝 New content generation request: {request.topic}")
    
    try:
        # Execute the complete workflow
        results = await crew_manager.execute_complete_workflow(
            topic=request.topic,
            tone=request.tone,
            platforms=request.platforms,
            research_mode=request.research_mode,
            lead_gen_mode=request.lead_gen_mode,
            outreach_mode=request.outreach_mode,
            content_length=request.content_length,
            target_audience=request.target_audience,
            include_hashtags=request.include_hashtags,
            include_cta=request.include_cta,
            include_sources=request.include_sources,
            custom_instructions=request.custom_instructions
        )
        
        # Structure the response
        response = ContentGenerationResponse(
            request_id=results.get("request_id", f"req_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"),
            status="completed" if results.get("success") else "failed",
            success=results.get("success", False),
            topic=request.topic,
            platforms=request.platforms,
            research_brief=results.get("research", {}).get("research_brief"),
            leads=results.get("leads", {}).get("leads"),
            content=results.get("content", {}).get("content", {}),
            outreach_messages=results.get("outreach", {}).get("outreach_messages"),
            sources=results.get("research", {}).get("sources", []),
            workflow_steps=results.get("workflow_steps", []),
            total_duration=results.get("total_duration"),
            error=results.get("error"),
            created_at=results.get("started_at", datetime.utcnow().isoformat())
        )
        
        logger.info(f"✅ Content generation completed: {response.request_id}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Content generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Content generation failed: {str(e)}"
        )

@app.post("/api/v1/research-only")
async def research_only(topic: str, platforms: Optional[List[str]] = None):
    """Execute only the research workflow"""
    global crew_manager
    
    if not crew_manager:
        raise HTTPException(status_code=503, detail="CrewAI agents not initialized")
    
    try:
        logger.info(f"🔍 Research-only request: {topic}")
        
        results = await crew_manager.execute_research_only(topic, platforms)
        
        logger.info(f"✅ Research completed: {results.get('request_id')}")
        return results
        
    except Exception as e:
        logger.error(f"❌ Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

@app.post("/api/v1/content-only")
async def content_only(
    topic: str,
    tone: str,
    platforms: List[str],
    research_brief: Optional[str] = None,
    **kwargs
):
    """Execute only the content creation workflow"""
    global crew_manager
    
    if not crew_manager:
        raise HTTPException(status_code=503, detail="CrewAI agents not initialized")
    
    try:
        logger.info(f"📝 Content-only request: {topic}")
        
        results = await crew_manager.execute_content_only(
            topic, tone, platforms, research_brief or "", **kwargs
        )
        
        logger.info(f"✅ Content creation completed: {results.get('request_id')}")
        return results
        
    except Exception as e:
        logger.error(f"❌ Content creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Content creation failed: {str(e)}")

@app.get("/api/v1/workflow-status/{request_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(request_id: str):
    """Get the status of a workflow execution"""
    global crew_manager
    
    if not crew_manager:
        raise HTTPException(status_code=503, detail="CrewAI agents not initialized")
    
    try:
        status = crew_manager.get_workflow_status(request_id)
        return WorkflowStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"❌ Status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.get("/api/v1/agent-capabilities")
async def get_agent_capabilities():
    """Get information about available agent capabilities"""
    global crew_manager
    
    if not crew_manager:
        raise HTTPException(status_code=503, detail="CrewAI agents not initialized")
    
    try:
        capabilities = crew_manager.get_agent_capabilities()
        return {
            "agents": capabilities,
            "total_agents": len(capabilities),
            "total_tools": sum(len(agent["tools"]) for agent in capabilities.values()),
            "status": "ready"
        }
        
    except Exception as e:
        logger.error(f"❌ Capabilities check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Capabilities check failed: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "path": str(request.url),
        "message": "The requested endpoint does not exist"
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred. Please try again later."
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )