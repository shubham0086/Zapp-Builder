from crewai import Crew, Process, Task
from typing import Dict, List, Any, Optional
import asyncio
import json
from datetime import datetime
from loguru import logger

from .research_agent import ResearchAgent
from .lead_generation_agent import LeadGenerationAgent
from .content_creator_agent import ContentCreatorAgent
from .outreach_agent import OutreachAgent
from ..core.config import settings

class ContentCreationCrew:
    def __init__(self):
        """Initialize the Content Creation Crew with all agents"""
        logger.info("🤖 Initializing Content Creation Crew...")
        
        # Initialize individual agents
        self.research_agent = ResearchAgent()
        self.lead_gen_agent = LeadGenerationAgent()
        self.content_agent = ContentCreatorAgent()
        self.outreach_agent = OutreachAgent()
        
        logger.info("✅ All agents initialized successfully")
    
    def create_crew(self, agents: List, tasks: List) -> Crew:
        """Create a Crew with specified agents and tasks"""
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            max_rpm=10,  # Rate limiting
            share_crew=False
        )
    
    async def execute_complete_workflow(
        self,
        topic: str,
        tone: str,
        platforms: List[str],
        research_mode: bool = True,
        lead_gen_mode: bool = False,
        outreach_mode: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute the complete content creation workflow"""
        
        logger.info(f"🚀 Starting complete workflow for topic: '{topic}'")
        start_time = datetime.utcnow()
        
        results = {
            "request_id": f"crew_{start_time.strftime('%Y%m%d_%H%M%S')}",
            "topic": topic,
            "tone": tone,
            "platforms": platforms,
            "started_at": start_time.isoformat(),
            "workflow_steps": []
        }
        
        try:
            # Step 1: Research Phase
            if research_mode:
                logger.info("📚 Executing research phase...")
                research_results = await self._execute_research_phase(topic, platforms)
                results["research"] = research_results
                results["workflow_steps"].append("research")
                logger.info("✅ Research phase completed")
            
            # Step 2: Lead Generation Phase
            if lead_gen_mode:
                logger.info("🎯 Executing lead generation phase...")
                lead_results = await self._execute_lead_generation_phase(topic, platforms)
                results["leads"] = lead_results
                results["workflow_steps"].append("lead_generation")
                logger.info("✅ Lead generation phase completed")
            
            # Step 3: Content Creation Phase
            logger.info("📝 Executing content creation phase...")
            research_brief = results.get("research", {}).get("research_brief", "")
            content_results = await self._execute_content_creation_phase(
                topic, tone, platforms, research_brief, **kwargs
            )
            results["content"] = content_results
            results["workflow_steps"].append("content_creation")
            logger.info("✅ Content creation phase completed")
            
            # Step 4: Outreach Phase (if leads were generated)
            if outreach_mode and lead_gen_mode and results.get("leads", {}).get("leads"):
                logger.info("📧 Executing outreach phase...")
                outreach_results = await self._execute_outreach_phase(
                    topic, tone, results["leads"]["leads"]
                )
                results["outreach"] = outreach_results
                results["workflow_steps"].append("outreach")
                logger.info("✅ Outreach phase completed")
            
            # Finalize results
            end_time = datetime.utcnow()
            results["completed_at"] = end_time.isoformat()
            results["total_duration"] = str(end_time - start_time)
            results["success"] = True
            
            logger.info(f"🎉 Complete workflow finished successfully in {end_time - start_time}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {str(e)}")
            end_time = datetime.utcnow()
            results["error"] = str(e)
            results["completed_at"] = end_time.isoformat()
            results["total_duration"] = str(end_time - start_time)
            results["success"] = False
            
            return results
    
    async def _execute_research_phase(self, topic: str, platforms: List[str]) -> Dict[str, Any]:
        """Execute the research phase"""
        try:
            # Run research in a thread to avoid blocking
            research_result = await asyncio.to_thread(
                self.research_agent.execute_research, topic, platforms
            )
            
            return {
                "success": research_result.get("success", False),
                "research_brief": research_result.get("research_brief", ""),
                "sources": research_result.get("sources", []),
                "error": research_result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Research phase failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "research_brief": f"Research phase failed for topic: {topic}",
                "sources": []
            }
    
    async def _execute_lead_generation_phase(self, topic: str, platforms: List[str]) -> Dict[str, Any]:
        """Execute the lead generation phase"""
        try:
            # Run lead generation in a thread to avoid blocking
            lead_result = await asyncio.to_thread(
                self.lead_gen_agent.execute_lead_generation, topic, platforms
            )
            
            return {
                "success": lead_result.get("success", False),
                "leads": lead_result.get("leads", []),
                "total_found": lead_result.get("total_found", 0),
                "error": lead_result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Lead generation phase failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "leads": [],
                "total_found": 0
            }
    
    async def _execute_content_creation_phase(
        self, 
        topic: str, 
        tone: str, 
        platforms: List[str], 
        research_brief: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Execute the content creation phase"""
        try:
            # Run content creation in a thread to avoid blocking
            content_result = await asyncio.to_thread(
                self.content_agent.execute_content_creation,
                topic, tone, platforms, research_brief, **kwargs
            )
            
            return {
                "success": content_result.get("success", False),
                "content": content_result.get("content", {}),
                "platforms": content_result.get("platforms", []),
                "error": content_result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Content creation phase failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": {},
                "platforms": platforms
            }
    
    async def _execute_outreach_phase(self, topic: str, tone: str, leads: List[Dict]) -> Dict[str, Any]:
        """Execute the outreach phase"""
        try:
            # Run outreach generation in a thread to avoid blocking
            outreach_result = await asyncio.to_thread(
                self.outreach_agent.execute_outreach_generation,
                topic, tone, leads, "collaboration"
            )
            
            return {
                "success": outreach_result.get("success", False),
                "outreach_messages": outreach_result.get("outreach_messages", []),
                "total_messages": outreach_result.get("total_messages", 0),
                "error": outreach_result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Outreach phase failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "outreach_messages": [],
                "total_messages": 0
            }
    
    async def execute_research_only(self, topic: str, platforms: List[str] = None) -> Dict[str, Any]:
        """Execute only the research workflow"""
        logger.info(f"🔍 Starting research-only workflow for: '{topic}'")
        
        try:
            research_results = await self._execute_research_phase(topic, platforms or [])
            
            return {
                "request_id": f"research_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "success": True,
                "research_brief": research_results.get("research_brief", ""),
                "sources": research_results.get("sources", []),
                "topic": topic,
                "platforms": platforms or [],
                "created_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Research-only workflow failed: {str(e)}")
            return {
                "request_id": f"research_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "success": False,
                "error": str(e),
                "research_brief": "",
                "sources": [],
                "topic": topic,
                "platforms": platforms or [],
                "created_at": datetime.utcnow().isoformat()
            }
    
    async def execute_content_only(
        self, 
        topic: str, 
        tone: str, 
        platforms: List[str],
        research_brief: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Execute only the content creation workflow"""
        logger.info(f"📝 Starting content-only workflow for: '{topic}'")
        
        try:
            content_results = await self._execute_content_creation_phase(
                topic, tone, platforms, research_brief, **kwargs
            )
            
            return {
                "request_id": f"content_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "success": True,
                "content": content_results.get("content", {}),
                "topic": topic,
                "tone": tone,
                "platforms": platforms,
                "created_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content-only workflow failed: {str(e)}")
            return {
                "request_id": f"content_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "success": False,
                "error": str(e),
                "content": {},
                "topic": topic,
                "tone": tone,
                "platforms": platforms,
                "created_at": datetime.utcnow().isoformat()
            }
    
    def get_workflow_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of a workflow execution (for future async implementation)"""
        # This would integrate with a task queue like Celery in production
        return {
            "request_id": request_id,
            "status": "completed",  # Mock status
            "progress": 100,
            "message": "Workflow completed successfully"
        }
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get information about agent capabilities"""
        return {
            "research_agent": {
                "capabilities": [
                    "Web search and analysis",
                    "Trend analysis", 
                    "Content analysis",
                    "Source citation"
                ],
                "tools": ["web_search", "analyze_content", "trend_analysis"]
            },
            "lead_generation_agent": {
                "capabilities": [
                    "Social media profile search",
                    "Influencer analysis",
                    "Community discovery",
                    "Brand identification"
                ],
                "tools": ["social_media_search", "analyze_influencer", "find_communities", "identify_brands"]
            },
            "content_creator_agent": {
                "capabilities": [
                    "Platform-optimized content creation",
                    "Hashtag generation",
                    "Engagement enhancement",
                    "Content formatting"
                ],
                "tools": ["optimize_for_platform", "generate_hashtags", "enhance_engagement", "format_content"]
            },
            "outreach_agent": {
                "capabilities": [
                    "Personalized message creation",
                    "Template generation",
                    "Tone matching",
                    "Value proposition creation"
                ],
                "tools": ["personalize_message", "generate_template", "match_tone", "create_value_proposition"]
            }
        }