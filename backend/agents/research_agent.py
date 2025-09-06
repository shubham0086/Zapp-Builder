from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
import json
from ..core.config import settings

class ResearchAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.3,
            api_key=settings.OPENAI_API_KEY
        ) if settings.OPENAI_API_KEY else None
        
        # Initialize tools
        self.search_tool = DuckDuckGoSearchRun()
        self.tools = self._setup_tools()
        
        # Create the agent
        self.agent = Agent(
            role="Research Specialist",
            goal="Conduct comprehensive research on given topics and provide well-sourced, actionable insights",
            backstory="""You are an expert researcher with years of experience in content strategy and market analysis. 
            You excel at finding the most relevant and up-to-date information on any topic, synthesizing multiple sources, 
            and presenting insights that content creators can immediately use. You always cite your sources and focus on 
            practical, actionable information.""",
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def _setup_tools(self) -> List[Tool]:
        """Setup research tools"""
        tools = []
        
        # Web search tool
        search_tool = Tool(
            name="web_search",
            description="Search the web for current information on any topic",
            func=self._web_search
        )
        tools.append(search_tool)
        
        # Content analyzer tool
        content_tool = Tool(
            name="analyze_content",
            description="Analyze web content for key insights and trends",
            func=self._analyze_content
        )
        tools.append(content_tool)
        
        # Trend analysis tool
        trend_tool = Tool(
            name="trend_analysis",
            description="Analyze trends and popularity of topics",
            func=self._analyze_trends
        )
        tools.append(trend_tool)
        
        return tools
    
    def _web_search(self, query: str) -> str:
        """Perform web search"""
        try:
            results = self.search_tool.run(query)
            return results
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def _analyze_content(self, url: str) -> str:
        """Analyze content from a URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract key information
            title = soup.find('title').text if soup.find('title') else "No title"
            paragraphs = soup.find_all('p')[:5]  # First 5 paragraphs
            content = ' '.join([p.text for p in paragraphs])
            
            return f"Title: {title}\n\nContent Summary: {content[:500]}..."
        except Exception as e:
            return f"Content analysis failed: {str(e)}"
    
    def _analyze_trends(self, topic: str) -> str:
        """Analyze trends for a topic"""
        # This would integrate with Google Trends API or similar
        # For now, return mock trend data
        return f"Trend analysis for '{topic}': Currently showing high interest with 85% growth in searches over the past month. Peak interest in technology and business sectors."
    
    def create_research_task(self, topic: str, platforms: List[str] = None) -> Task:
        """Create a research task for the given topic"""
        platform_context = f" Focus on content suitable for {', '.join(platforms)}" if platforms else ""
        
        task = Task(
            description=f"""
            Conduct comprehensive research on the topic: "{topic}"{platform_context}
            
            Your research should include:
            1. Current trends and developments related to this topic
            2. Key statistics and data points
            3. Expert opinions and industry insights
            4. Practical applications and real-world examples
            5. Audience interests and engagement patterns
            6. Content opportunities and angles
            
            Provide a detailed research brief with:
            - Executive summary
            - Key findings with sources
            - Content recommendations
            - Trending subtopics
            - Target audience insights
            
            Always cite your sources and ensure information is current and accurate.
            """,
            agent=self.agent,
            expected_output="A comprehensive research brief in markdown format with cited sources and actionable insights"
        )
        
        return task
    
    def execute_research(self, topic: str, platforms: List[str] = None) -> Dict[str, Any]:
        """Execute research task and return results"""
        try:
            task = self.create_research_task(topic, platforms)
            result = task.execute()
            
            return {
                "success": True,
                "research_brief": result,
                "sources": self._extract_sources(result),
                "topic": topic,
                "platforms": platforms or []
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "research_brief": f"Research failed for topic: {topic}",
                "sources": [],
                "topic": topic,
                "platforms": platforms or []
            }
    
    def _extract_sources(self, research_text: str) -> List[str]:
        """Extract sources from research text"""
        # Simple source extraction - would be more sophisticated in production
        sources = []
        lines = research_text.split('\n')
        for line in lines:
            if 'http' in line or 'www.' in line:
                # Extract URLs from the line
                words = line.split()
                for word in words:
                    if word.startswith('http') or word.startswith('www.'):
                        sources.append(word.strip('.,)]}'))
        return sources[:10]  # Limit to 10 sources