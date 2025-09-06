from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from typing import Dict, List, Any, Optional
import json
import random
from ..core.config import settings

class LeadGenerationAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.2,
            api_key=settings.OPENAI_API_KEY
        ) if settings.OPENAI_API_KEY else None
        
        # Initialize tools
        self.tools = self._setup_tools()
        
        # Create the agent
        self.agent = Agent(
            role="Lead Generation Specialist",
            goal="Identify high-quality leads including influencers, content creators, brands, and communities relevant to specific topics",
            backstory="""You are a seasoned lead generation expert with deep knowledge of social media platforms, 
            influencer marketing, and community building. You excel at identifying the right people and organizations 
            that would be interested in specific topics. You understand engagement metrics, audience quality, and 
            can spot authentic influencers from fake ones. Your leads always result in meaningful connections.""",
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def _setup_tools(self) -> List[Tool]:
        """Setup lead generation tools"""
        tools = []
        
        # Social media search tool
        social_search_tool = Tool(
            name="social_media_search",
            description="Search for influencers and creators on social media platforms",
            func=self._search_social_media
        )
        tools.append(social_search_tool)
        
        # Influencer analyzer tool
        analyzer_tool = Tool(
            name="analyze_influencer",
            description="Analyze influencer profiles for relevance and engagement quality",
            func=self._analyze_influencer
        )
        tools.append(analyzer_tool)
        
        # Community finder tool
        community_tool = Tool(
            name="find_communities",
            description="Find relevant communities and groups for a topic",
            func=self._find_communities
        )
        tools.append(community_tool)
        
        # Brand identifier tool
        brand_tool = Tool(
            name="identify_brands",
            description="Identify brands and companies active in a specific topic area",
            func=self._identify_brands
        )
        tools.append(brand_tool)
        
        return tools
    
    def _search_social_media(self, query: str) -> str:
        """Search for social media profiles (mock implementation)"""
        # In production, this would integrate with social media APIs
        mock_profiles = [
            {
                "name": f"TechExpert_{random.randint(1, 100)}",
                "platform": "LinkedIn",
                "followers": random.randint(10000, 100000),
                "engagement_rate": round(random.uniform(0.02, 0.08), 3),
                "niche": "Technology"
            },
            {
                "name": f"ContentCreator_{random.randint(1, 100)}",
                "platform": "YouTube",
                "followers": random.randint(50000, 500000),
                "engagement_rate": round(random.uniform(0.01, 0.05), 3),
                "niche": "Content Creation"
            },
            {
                "name": f"Influencer_{random.randint(1, 100)}",
                "platform": "Instagram",
                "followers": random.randint(25000, 250000),
                "engagement_rate": round(random.uniform(0.015, 0.06), 3),
                "niche": "Lifestyle"
            }
        ]
        
        return json.dumps(mock_profiles[:2])  # Return top 2 results
    
    def _analyze_influencer(self, profile_data: str) -> str:
        """Analyze influencer profile for quality"""
        try:
            profile = json.loads(profile_data)
            
            # Calculate relevance score based on multiple factors
            engagement_score = min(profile.get('engagement_rate', 0) * 20, 1.0)
            follower_score = min(profile.get('followers', 0) / 100000, 1.0)
            relevance_score = round((engagement_score + follower_score) / 2, 2)
            
            analysis = {
                "relevance_score": relevance_score,
                "quality": "High" if relevance_score > 0.7 else "Medium" if relevance_score > 0.4 else "Low",
                "recommendation": "Highly recommended" if relevance_score > 0.7 else "Consider for outreach" if relevance_score > 0.4 else "Low priority"
            }
            
            return json.dumps(analysis)
        except Exception as e:
            return f"Analysis failed: {str(e)}"
    
    def _find_communities(self, topic: str) -> str:
        """Find relevant communities for a topic"""
        # Mock community data - would integrate with Reddit API, Discord, etc.
        mock_communities = [
            {
                "name": f"r/{topic.lower().replace(' ', '')}",
                "platform": "Reddit",
                "members": random.randint(5000, 50000),
                "activity": "High"
            },
            {
                "name": f"{topic} Professionals",
                "platform": "LinkedIn",
                "members": random.randint(10000, 100000),
                "activity": "Medium"
            },
            {
                "name": f"{topic} Discord",
                "platform": "Discord",
                "members": random.randint(1000, 10000),
                "activity": "High"
            }
        ]
        
        return json.dumps(mock_communities)
    
    def _identify_brands(self, topic: str) -> str:
        """Identify relevant brands for a topic"""
        # Mock brand data - would integrate with brand databases
        mock_brands = [
            {
                "name": f"{topic} Solutions Inc",
                "industry": topic,
                "size": "Medium",
                "social_presence": "Active"
            },
            {
                "name": f"Global {topic} Corp",
                "industry": topic,
                "size": "Large",
                "social_presence": "Very Active"
            }
        ]
        
        return json.dumps(mock_brands)
    
    def create_lead_generation_task(self, topic: str, platforms: List[str], max_leads: int = 20) -> Task:
        """Create a lead generation task"""
        platform_filter = f" Focus on {', '.join(platforms)} platforms" if platforms else ""
        
        task = Task(
            description=f"""
            Generate high-quality leads related to the topic: "{topic}"{platform_filter}
            
            Find and analyze:
            1. Influencers and content creators who discuss this topic
            2. Brands and companies active in this space
            3. Communities and groups focused on this topic
            4. Thought leaders and experts
            
            For each lead, provide:
            - Name and platform
            - Follower/member count
            - Engagement metrics
            - Relevance score (0-1)
            - Contact information (if available)
            - Outreach recommendation
            
            Prioritize leads with:
            - High engagement rates (not just follower count)
            - Authentic audiences
            - Regular posting activity
            - Strong topic relevance
            
            Return up to {max_leads} leads ranked by potential value.
            """,
            agent=self.agent,
            expected_output="A JSON list of qualified leads with detailed analysis and scoring"
        )
        
        return task
    
    def execute_lead_generation(self, topic: str, platforms: List[str], max_leads: int = 20) -> Dict[str, Any]:
        """Execute lead generation and return results"""
        try:
            task = self.create_lead_generation_task(topic, platforms, max_leads)
            result = task.execute()
            
            # Parse and structure the results
            leads = self._parse_leads_result(result, topic, platforms)
            
            return {
                "success": True,
                "leads": leads,
                "total_found": len(leads),
                "topic": topic,
                "platforms": platforms
            }
        except Exception as e:
            # Return mock data if execution fails
            mock_leads = self._generate_mock_leads(topic, platforms, max_leads)
            return {
                "success": False,
                "error": str(e),
                "leads": mock_leads,
                "total_found": len(mock_leads),
                "topic": topic,
                "platforms": platforms
            }
    
    def _parse_leads_result(self, result: str, topic: str, platforms: List[str]) -> List[Dict]:
        """Parse the agent's result into structured lead data"""
        # This would parse the actual agent output
        # For now, return mock structured data
        return self._generate_mock_leads(topic, platforms, 10)
    
    def _generate_mock_leads(self, topic: str, platforms: List[str], count: int) -> List[Dict]:
        """Generate mock lead data for testing"""
        mock_leads = []
        
        for i in range(min(count, 10)):
            platform = random.choice(platforms) if platforms else random.choice(["LinkedIn", "YouTube", "Instagram", "Twitter"])
            
            lead = {
                "id": f"lead_{i+1}",
                "name": f"{topic.title()}Expert{i+1}",
                "platform": platform,
                "profile_url": f"https://{platform.lower()}.com/{topic.lower()}expert{i+1}",
                "follower_count": random.randint(5000, 100000),
                "engagement_rate": round(random.uniform(0.01, 0.08), 3),
                "relevance_score": round(random.uniform(0.6, 0.95), 2),
                "last_active": "2024-01-15",
                "niche": topic,
                "bio": f"Expert in {topic} with {random.randint(5, 15)} years of experience",
                "contact_email": f"{topic.lower()}expert{i+1}@example.com",
                "tags": [topic, platform, "Influencer"],
                "outreach_priority": "High" if random.random() > 0.5 else "Medium"
            }
            
            mock_leads.append(lead)
        
        # Sort by relevance score
        mock_leads.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return mock_leads