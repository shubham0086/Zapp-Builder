from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from typing import Dict, List, Any, Optional
import json
from ..core.config import settings

class ContentCreatorAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        ) if settings.OPENAI_API_KEY else None
        
        # Platform specifications
        self.platform_specs = {
            "LinkedIn": {
                "max_length": 3000,
                "style": "professional",
                "hashtags": 3-5,
                "format": "paragraph"
            },
            "X (Twitter)": {
                "max_length": 280,
                "style": "conversational",
                "hashtags": 1-3,
                "format": "thread"
            },
            "Instagram": {
                "max_length": 2200,
                "style": "visual",
                "hashtags": 5-10,
                "format": "caption"
            },
            "YouTube": {
                "max_length": 5000,
                "style": "engaging",
                "hashtags": 3-7,
                "format": "description"
            },
            "Newsletter": {
                "max_length": 10000,
                "style": "informative",
                "hashtags": 0,
                "format": "article"
            },
            "Blog": {
                "max_length": 15000,
                "style": "comprehensive",
                "hashtags": 3-8,
                "format": "article"
            }
        }
        
        # Initialize tools
        self.tools = self._setup_tools()
        
        # Create the agent
        self.agent = Agent(
            role="Content Creation Specialist",
            goal="Create engaging, platform-optimized content that resonates with target audiences and drives engagement",
            backstory="""You are a master content creator with expertise across all major social media platforms and content formats. 
            You understand the nuances of each platform - from LinkedIn's professional tone to TikTok's viral trends. 
            You craft content that not only informs but also engages, entertains, and inspires action. Your content consistently 
            achieves high engagement rates because you understand what makes people stop scrolling and start engaging.""",
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def _setup_tools(self) -> List[Tool]:
        """Setup content creation tools"""
        tools = []
        
        # Platform optimizer tool
        optimizer_tool = Tool(
            name="optimize_for_platform",
            description="Optimize content for specific social media platforms",
            func=self._optimize_for_platform
        )
        tools.append(optimizer_tool)
        
        # Hashtag generator tool
        hashtag_tool = Tool(
            name="generate_hashtags",
            description="Generate relevant hashtags for content",
            func=self._generate_hashtags
        )
        tools.append(hashtag_tool)
        
        # Engagement enhancer tool
        engagement_tool = Tool(
            name="enhance_engagement",
            description="Add engagement elements like questions, CTAs, and hooks",
            func=self._enhance_engagement
        )
        tools.append(engagement_tool)
        
        # Content formatter tool
        formatter_tool = Tool(
            name="format_content",
            description="Format content with proper structure, emojis, and visual elements",
            func=self._format_content
        )
        tools.append(formatter_tool)
        
        return tools
    
    def _optimize_for_platform(self, content_data: str) -> str:
        """Optimize content for specific platform"""
        try:
            data = json.loads(content_data)
            platform = data.get('platform', 'LinkedIn')
            content = data.get('content', '')
            
            specs = self.platform_specs.get(platform, self.platform_specs['LinkedIn'])
            
            # Truncate if too long
            if len(content) > specs['max_length']:
                content = content[:specs['max_length']-3] + "..."
            
            # Apply platform-specific styling
            if platform == "X (Twitter)" and len(content) > 280:
                # Convert to thread format
                content = self._create_twitter_thread(content)
            elif platform == "LinkedIn":
                content = self._add_linkedin_formatting(content)
            elif platform == "Instagram":
                content = self._add_instagram_formatting(content)
            
            return content
        except Exception as e:
            return f"Optimization failed: {str(e)}"
    
    def _generate_hashtags(self, topic: str) -> str:
        """Generate relevant hashtags for a topic"""
        # This would use hashtag research APIs in production
        base_hashtags = {
            "ai": ["#AI", "#ArtificialIntelligence", "#MachineLearning", "#Tech", "#Innovation"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#SocialMedia", "#Branding"],
            "business": ["#Business", "#Entrepreneurship", "#Leadership", "#Strategy", "#Growth"],
            "technology": ["#Technology", "#Tech", "#Innovation", "#Digital", "#Future"],
            "productivity": ["#Productivity", "#Efficiency", "#WorkSmart", "#TimeManagement", "#Success"]
        }
        
        # Find relevant hashtags based on topic keywords
        hashtags = []
        topic_lower = topic.lower()
        
        for key, tags in base_hashtags.items():
            if key in topic_lower:
                hashtags.extend(tags)
        
        # Add topic-specific hashtags
        topic_words = topic.replace(" ", "").title()
        hashtags.append(f"#{topic_words}")
        
        return " ".join(hashtags[:8])  # Limit to 8 hashtags
    
    def _enhance_engagement(self, content: str) -> str:
        """Add engagement elements to content"""
        engagement_elements = [
            "What are your thoughts on this?",
            "Have you experienced this too?",
            "Share your experience in the comments!",
            "What would you add to this list?",
            "Tag someone who needs to see this!",
            "Double-tap if you agree! 👍",
            "What's your take on this topic?"
        ]
        
        import random
        cta = random.choice(engagement_elements)
        
        return f"{content}\n\n{cta}"
    
    def _format_content(self, content_data: str) -> str:
        """Format content with structure and visual elements"""
        try:
            data = json.loads(content_data)
            content = data.get('content', '')
            platform = data.get('platform', 'LinkedIn')
            
            # Add emojis and formatting based on platform
            if platform in ["LinkedIn", "Instagram"]:
                # Add bullet points and emojis
                content = self._add_visual_elements(content)
            
            return content
        except Exception as e:
            return content
    
    def _add_visual_elements(self, content: str) -> str:
        """Add visual elements like emojis and formatting"""
        # Add some emojis to key points
        emoji_map = {
            "key": "🔑",
            "important": "⚠️",
            "tip": "💡",
            "success": "✅",
            "growth": "📈",
            "strategy": "🎯",
            "innovation": "🚀",
            "future": "🔮"
        }
        
        for word, emoji in emoji_map.items():
            if word in content.lower():
                content = content.replace(word, f"{emoji} {word}")
                break  # Add only one emoji to avoid clutter
        
        return content
    
    def _create_twitter_thread(self, content: str) -> str:
        """Convert long content into Twitter thread format"""
        sentences = content.split('. ')
        thread = []
        current_tweet = ""
        
        for sentence in sentences:
            if len(current_tweet + sentence) < 250:  # Leave room for thread numbering
                current_tweet += sentence + ". "
            else:
                if current_tweet:
                    thread.append(current_tweet.strip())
                current_tweet = sentence + ". "
        
        if current_tweet:
            thread.append(current_tweet.strip())
        
        # Number the tweets
        numbered_thread = []
        for i, tweet in enumerate(thread, 1):
            numbered_thread.append(f"{i}/{len(thread)} {tweet}")
        
        return "\n\n---THREAD BREAK---\n\n".join(numbered_thread)
    
    def _add_linkedin_formatting(self, content: str) -> str:
        """Add LinkedIn-specific formatting"""
        # LinkedIn performs well with line breaks and bullet points
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            if len(para) > 200:  # Break long paragraphs
                formatted_paragraphs.append(para[:200] + "...")
                formatted_paragraphs.append(para[200:])
            else:
                formatted_paragraphs.append(para)
        
        return "\n\n".join(formatted_paragraphs)
    
    def _add_instagram_formatting(self, content: str) -> str:
        """Add Instagram-specific formatting"""
        # Instagram likes visual breaks and emojis
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                formatted_lines.append(f"✨ {line}")
            else:
                formatted_lines.append(line)
        
        return "\n".join(formatted_lines)
    
    def create_content_task(self, topic: str, tone: str, platforms: List[str], research_brief: str = "", **kwargs) -> Task:
        """Create a content creation task"""
        platform_list = ', '.join(platforms)
        content_length = kwargs.get('content_length', 'medium')
        target_audience = kwargs.get('target_audience', 'general audience')
        include_hashtags = kwargs.get('include_hashtags', True)
        include_cta = kwargs.get('include_cta', True)
        custom_instructions = kwargs.get('custom_instructions', '')
        
        task = Task(
            description=f"""
            Create engaging content about "{topic}" for the following platforms: {platform_list}
            
            Content Requirements:
            - Tone: {tone}
            - Length: {content_length}
            - Target Audience: {target_audience}
            - Include hashtags: {include_hashtags}
            - Include call-to-action: {include_cta}
            
            Research Context:
            {research_brief[:1000] if research_brief else "No research brief provided"}
            
            Custom Instructions:
            {custom_instructions if custom_instructions else "None"}
            
            For each platform, create:
            1. Platform-optimized content that follows best practices
            2. Appropriate hashtags (if requested)
            3. Engaging hooks and CTAs (if requested)
            4. Proper formatting for the platform
            
            Platform-Specific Guidelines:
            - LinkedIn: Professional, thought-leadership style with industry insights
            - X (Twitter): Concise, conversational, thread-friendly if needed
            - Instagram: Visual, lifestyle-focused with strong visual appeal
            - YouTube: Detailed, educational with clear value proposition
            - Newsletter: Comprehensive, well-structured with clear sections
            - Blog: In-depth, SEO-friendly with proper headings
            
            Ensure each piece of content:
            - Provides genuine value to the audience
            - Is authentic and engaging
            - Includes relevant keywords naturally
            - Follows platform character limits and best practices
            - Encourages meaningful engagement
            """,
            agent=self.agent,
            expected_output="Platform-specific content for each requested platform in JSON format with content, hashtags, and metadata"
        )
        
        return task
    
    def execute_content_creation(self, topic: str, tone: str, platforms: List[str], research_brief: str = "", **kwargs) -> Dict[str, Any]:
        """Execute content creation and return results"""
        try:
            task = self.create_content_task(topic, tone, platforms, research_brief, **kwargs)
            result = task.execute()
            
            # Parse and structure the results
            content_dict = self._parse_content_result(result, topic, tone, platforms, **kwargs)
            
            return {
                "success": True,
                "content": content_dict,
                "topic": topic,
                "tone": tone,
                "platforms": platforms
            }
        except Exception as e:
            # Return mock content if execution fails
            mock_content = self._generate_mock_content(topic, tone, platforms, **kwargs)
            return {
                "success": False,
                "error": str(e),
                "content": mock_content,
                "topic": topic,
                "tone": tone,
                "platforms": platforms
            }
    
    def _parse_content_result(self, result: str, topic: str, tone: str, platforms: List[str], **kwargs) -> Dict[str, str]:
        """Parse the agent's result into structured content data"""
        # This would parse the actual agent output
        # For now, return mock structured data
        return self._generate_mock_content(topic, tone, platforms, **kwargs)
    
    def _generate_mock_content(self, topic: str, tone: str, platforms: List[str], **kwargs) -> Dict[str, str]:
        """Generate mock content for testing"""
        content_dict = {}
        
        include_hashtags = kwargs.get('include_hashtags', True)
        include_cta = kwargs.get('include_cta', True)
        target_audience = kwargs.get('target_audience', 'professionals')
        
        for platform in platforms:
            content = self._create_platform_content(topic, tone, platform, target_audience)
            
            if include_hashtags:
                hashtags = self._generate_hashtags(topic)
                content += f"\n\n{hashtags}"
            
            if include_cta:
                content = self._enhance_engagement(content)
            
            content_dict[platform] = content
        
        return content_dict
    
    def _create_platform_content(self, topic: str, tone: str, platform: str, audience: str) -> str:
        """Create platform-specific content"""
        base_content = {
            "LinkedIn": f"""
🚀 The Future of {topic}: What {audience.title()} Need to Know

{topic} is revolutionizing how we work and think. Here are the key insights every professional should understand:

🔍 Current State:
The landscape is evolving rapidly, with new developments emerging weekly. Organizations that adapt quickly are seeing significant advantages.

📈 Key Trends:
• Increased adoption across industries
• Growing investment in related technologies  
• Shift in required skill sets
• New opportunities for innovation

💡 Practical Applications:
Smart companies are already implementing {topic.lower()} solutions to:
- Streamline operations
- Enhance decision-making
- Improve customer experiences
- Drive competitive advantage

🎯 What This Means for You:
Whether you're a seasoned professional or just starting your career, understanding {topic.lower()} is becoming essential. The time to start learning is now.

The organizations that embrace this change will lead the future. Are you ready to be part of it?
            """.strip(),
            
            "X (Twitter)": f"""
🧵 Thread: Why {topic} matters more than you think

1/ {topic} isn't just a buzzword - it's reshaping entire industries. Here's what you need to know 👇

2/ The stats are staggering: Companies using {topic.lower()} are seeing 40% faster growth and 25% higher efficiency rates.

3/ But here's the thing - it's not just about the technology. It's about how we adapt and evolve with it.

4/ Three key areas where {topic.lower()} is making the biggest impact:
• Decision making
• Customer experience  
• Operational efficiency

5/ The question isn't IF this will affect your industry, but WHEN. Smart professionals are already preparing.

6/ My advice? Start learning now. The future belongs to those who embrace change, not resist it.

What's your experience with {topic.lower()}? Share in the replies! 👇
            """.strip(),
            
            "Instagram": f"""
✨ Let's talk about {topic} ✨

Swipe left to see why this is changing everything! 👉

{topic} isn't just tech talk - it's the future of how we work, create, and connect. And honestly? It's pretty amazing what's possible now.

🌟 Here's what's got me excited:
• New possibilities we never imagined
• Tools that actually make life easier
• Opportunities for everyone to grow
• A future that's more connected than ever

💭 I used to think {topic.lower()} was just for tech experts, but I was so wrong. It's for creators, entrepreneurs, students - literally everyone.

The coolest part? We're just getting started. What we'll see in the next few years is going to blow our minds 🤯

🔥 Ready to dive deeper? Check out my stories for resources to get started!

What questions do you have about {topic.lower()}? Drop them below! 👇✨
            """.strip(),
            
            "YouTube": f"""
🎬 The Complete Guide to {topic}: Everything You Need to Know in 2024

Welcome back to the channel! Today we're diving deep into {topic} - a topic that's been requested by so many of you, and for good reason.

📋 What We'll Cover:
• What {topic.lower()} actually is (in simple terms!)
• Why it matters for your career/business
• Real-world examples and case studies
• How to get started today
• Common mistakes to avoid
• Future predictions and trends

🚀 Why This Matters Now:
The landscape is changing faster than ever. Companies that understand and implement {topic.lower()} are pulling ahead, while others are getting left behind. This isn't just theory - I'll show you real data and examples.

💡 Key Takeaways You'll Get:
By the end of this video, you'll have a clear understanding of how {topic.lower()} can impact your industry and what steps you can take immediately to stay ahead of the curve.

🎯 Perfect For:
• Professionals looking to future-proof their careers
• Business owners wanting to stay competitive
• Students preparing for the job market
• Anyone curious about emerging trends

Don't forget to hit that subscribe button and ring the notification bell so you never miss our latest insights on technology and business trends!

Let's jump right in...
            """.strip(),
            
            "Newsletter": f"""
📧 Subject: The {topic} Revolution: Your Weekly Insight

Dear Subscriber,

This week, I want to talk about something that's been on my mind - and probably yours too - {topic}.

🔍 THE BIG PICTURE

{topic} isn't just another trend. It's fundamentally changing how we approach problems, make decisions, and create value. The organizations that understand this early are positioning themselves for unprecedented growth.

📊 BY THE NUMBERS

Recent studies show:
• 73% of executives consider {topic.lower()} a strategic priority
• Companies implementing {topic.lower()} see 35% faster growth
• Job postings requiring {topic.lower()} skills have increased 150% this year

But here's what the numbers don't tell you...

💡 THE REAL STORY

Behind every statistic is a human story. I've been talking to professionals across industries, and the pattern is clear: those who embrace {topic.lower()} aren't just surviving change - they're thriving in it.

Take Sarah, a marketing manager who integrated {topic.lower()} into her campaigns. Result? 40% higher engagement and a promotion within six months.

Or consider TechCorp (name changed), a mid-size company that was struggling with efficiency. After implementing {topic.lower()} solutions, they reduced costs by 25% while improving customer satisfaction.

🎯 WHAT THIS MEANS FOR YOU

Whether you're an individual professional or leading a team, the question isn't whether {topic.lower()} will impact your work - it's how quickly you can adapt and leverage it.

Here are three immediate actions you can take:

1. Educate yourself: Spend 30 minutes this week learning about {topic.lower()}
2. Identify opportunities: Where in your current role could {topic.lower()} add value?
3. Start small: Pick one area to experiment with - don't try to revolutionize everything at once

🚀 LOOKING AHEAD

Next week, I'll be sharing a detailed case study of how a Fortune 500 company completely transformed their operations using {topic.lower()}. The results will surprise you.

Until then, keep innovating!

Best regards,
[Your Name]

P.S. What's your biggest question about {topic.lower()}? Hit reply - I read every email and often use your questions for future newsletters.
            """.strip(),
            
            "Blog": f"""
# The Complete Guide to {topic}: Transforming Industries and Careers in 2024

*Last updated: January 2024 | Reading time: 8 minutes*

## Introduction

In the rapidly evolving landscape of modern business and technology, few topics have generated as much excitement and transformation as {topic.lower()}. What started as a niche concept has evolved into a fundamental force reshaping industries, careers, and the very way we approach problem-solving.

This comprehensive guide will explore everything you need to know about {topic.lower()}, from its practical applications to its future implications for professionals and organizations worldwide.

## What is {topic}?

{topic} represents a paradigm shift in how we process information, make decisions, and create value. At its core, it's about leveraging advanced capabilities to augment human intelligence and automate complex processes.

### Key Characteristics:
- **Scalability**: Solutions that grow with your needs
- **Efficiency**: Dramatic improvements in speed and accuracy
- **Adaptability**: Systems that learn and improve over time
- **Integration**: Seamless connection with existing workflows

## The Current Landscape

### Market Growth and Adoption

The {topic.lower()} market has experienced unprecedented growth:

- **Market Size**: Projected to reach $X billion by 2025
- **Adoption Rate**: 60% of Fortune 500 companies now use {topic.lower()} solutions
- **Investment**: Venture capital funding has increased 200% year-over-year
- **Job Market**: Over 100,000 new positions created in the last 12 months

### Industry Applications

**Healthcare**: Revolutionizing diagnosis and treatment planning
**Finance**: Enhancing fraud detection and risk assessment  
**Manufacturing**: Optimizing supply chains and predictive maintenance
**Education**: Personalizing learning experiences and outcomes
**Retail**: Improving customer experience and inventory management

## Real-World Case Studies

### Case Study 1: Global Manufacturing Company

**Challenge**: Inefficient production processes leading to 15% waste
**Solution**: Implemented {topic.lower()} for predictive analytics
**Results**: 
- 25% reduction in waste
- 30% improvement in efficiency
- $2.3M annual cost savings

### Case Study 2: Healthcare Network

**Challenge**: Delayed diagnosis affecting patient outcomes
**Solution**: {topic.lower()}-powered diagnostic assistance
**Results**:
- 40% faster diagnosis times
- 95% accuracy improvement
- Enhanced patient satisfaction scores

## Getting Started: A Practical Roadmap

### Phase 1: Assessment (Weeks 1-2)
- Audit current processes and identify opportunities
- Assess team readiness and skill gaps
- Define success metrics and goals

### Phase 2: Planning (Weeks 3-4)
- Develop implementation strategy
- Select appropriate tools and platforms
- Create timeline and budget

### Phase 3: Implementation (Months 2-6)
- Start with pilot projects
- Train team members
- Monitor progress and adjust

### Phase 4: Scale (Months 6+)
- Expand successful initiatives
- Integrate across departments
- Measure ROI and optimize

## Skills and Career Implications

### In-Demand Skills
1. **Technical Skills**
   - Data analysis and interpretation
   - Platform-specific knowledge
   - Integration capabilities

2. **Soft Skills**
   - Strategic thinking
   - Change management
   - Cross-functional collaboration

### Career Opportunities
- {topic} Specialist
- Implementation Manager
- Strategy Consultant
- Data Analyst
- Solution Architect

## Common Challenges and Solutions

### Challenge 1: Resistance to Change
**Solution**: Focus on education and demonstrate quick wins

### Challenge 2: Technical Complexity
**Solution**: Start with user-friendly platforms and build expertise gradually

### Challenge 3: ROI Concerns
**Solution**: Begin with high-impact, low-risk projects

## Future Trends and Predictions

### Next 2-3 Years
- Increased automation across industries
- More sophisticated integration capabilities
- Enhanced user interfaces and accessibility

### 5-Year Outlook
- Mainstream adoption across all business sizes
- New job categories and career paths
- Fundamental changes in business models

## Conclusion

{topic} represents more than just technological advancement - it's a fundamental shift in how we approach work, problem-solving, and value creation. Organizations and professionals who embrace this change early will have significant advantages in the competitive landscape ahead.

The key is to start now, even if small. Begin with education, identify opportunities in your current role, and gradually build expertise. The future belongs to those who adapt and evolve with these emerging technologies.

### Key Takeaways:
- {topic} is reshaping industries at an unprecedented pace
- Early adoption provides significant competitive advantages
- Success requires both technical and strategic understanding
- The time to start is now - begin with small, manageable projects

---

*Ready to dive deeper into {topic}? Subscribe to our newsletter for weekly insights and practical tips, or contact our team for personalized consultation on your {topic.lower()} journey.*
            """.strip()
        }
        
        return base_content.get(platform, base_content["LinkedIn"])