from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from typing import Dict, List, Any, Optional
import json
import random
from ..core.config import settings

class OutreachAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.6,
            api_key=settings.OPENAI_API_KEY
        ) if settings.OPENAI_API_KEY else None
        
        # Initialize tools
        self.tools = self._setup_tools()
        
        # Create the agent
        self.agent = Agent(
            role="Outreach Specialist",
            goal="Craft personalized, effective outreach messages that build genuine connections and drive meaningful engagement",
            backstory="""You are a master of authentic relationship building and persuasive communication. 
            With years of experience in influencer marketing, partnership development, and community building, 
            you know how to craft messages that feel personal, valuable, and genuine - never spammy or pushy. 
            You understand that great outreach is about providing value first and building long-term relationships, 
            not just immediate conversions.""",
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def _setup_tools(self) -> List[Tool]:
        """Setup outreach tools"""
        tools = []
        
        # Personalization tool
        personalization_tool = Tool(
            name="personalize_message",
            description="Personalize outreach messages based on recipient profile and context",
            func=self._personalize_message
        )
        tools.append(personalization_tool)
        
        # Template generator tool
        template_tool = Tool(
            name="generate_template",
            description="Generate outreach message templates for different scenarios",
            func=self._generate_template
        )
        tools.append(template_tool)
        
        # Tone matcher tool
        tone_tool = Tool(
            name="match_tone",
            description="Match message tone to recipient's communication style and platform",
            func=self._match_tone
        )
        tools.append(tone_tool)
        
        # Value proposition tool
        value_tool = Tool(
            name="create_value_proposition",
            description="Create compelling value propositions for different types of outreach",
            func=self._create_value_proposition
        )
        tools.append(value_tool)
        
        return tools
    
    def _personalize_message(self, data: str) -> str:
        """Personalize message based on recipient data"""
        try:
            recipient_data = json.loads(data)
            name = recipient_data.get('name', 'there')
            platform = recipient_data.get('platform', 'LinkedIn')
            niche = recipient_data.get('niche', 'content creation')
            follower_count = recipient_data.get('follower_count', 0)
            
            # Create personalized elements
            personalization = {
                "greeting": f"Hi {name}," if name != 'there' else "Hello!",
                "platform_reference": f"I came across your {platform} profile",
                "niche_mention": f"your work in {niche}",
                "social_proof": f"with your {follower_count:,} followers" if follower_count > 1000 else "and your engaged community"
            }
            
            return json.dumps(personalization)
        except Exception as e:
            return f"Personalization failed: {str(e)}"
    
    def _generate_template(self, template_type: str) -> str:
        """Generate outreach message template"""
        templates = {
            "collaboration": """
            Subject: Collaboration Opportunity - [Topic]
            
            {greeting}
            
            {platform_reference} and was impressed by {niche_mention}. Your recent content on [specific topic] really resonated with me, especially your insight about [specific point].
            
            I'm reaching out because I believe we could create something valuable together. I'm working on [brief description of your project/content] and think your perspective would add tremendous value.
            
            Here's what I have in mind:
            • [Specific collaboration idea]
            • [Mutual benefit 1]
            • [Mutual benefit 2]
            
            I'd love to explore this further if you're interested. Would you be open to a brief 15-minute call this week to discuss?
            
            Best regards,
            [Your name]
            
            P.S. [Genuine compliment or shared connection]
            """,
            
            "guest_post": """
            Subject: Guest Content Opportunity for [Platform/Publication]
            
            {greeting}
            
            I've been following {niche_mention} for a while now, and your insights on [specific topic] have been incredibly valuable. {social_proof} clearly appreciate the depth and authenticity you bring to the conversation.
            
            I'm reaching out with a content collaboration idea that I think could provide real value to your audience:
            
            **Proposed Topic**: [Specific, valuable topic]
            **Why Now**: [Relevance/timing]
            **Value for Your Audience**: [Specific benefits]
            
            I'd handle all the content creation and ensure it aligns perfectly with your brand voice and audience preferences. Plus, I'm happy to promote it across my channels to maximize reach.
            
            Would you be interested in seeing a detailed outline? I can have something ready within 48 hours.
            
            Looking forward to potentially collaborating!
            
            [Your name]
            """,
            
            "partnership": """
            Subject: Strategic Partnership Opportunity
            
            {greeting}
            
            I hope this message finds you well. I've been impressed by your work in {niche_mention} and the authentic way you connect with your community.
            
            I'm reaching out because I see a natural synergy between what we're both building. Here's a brief overview of what I have in mind:
            
            **The Opportunity**: [Clear, specific partnership idea]
            **Mutual Benefits**: 
            • For you: [Specific benefit 1]
            • For you: [Specific benefit 2]
            • For both: [Shared benefit]
            
            **Next Steps**: If this resonates with you, I'd love to schedule a brief call to explore the details and see if there's a good fit.
            
            I've attached a one-page overview with more details. No pressure at all - just wanted to put the idea on your radar.
            
            Best,
            [Your name]
            """,
            
            "interview_request": """
            Subject: Interview Request - [Specific Topic]
            
            {greeting}
            
            Your expertise in {niche_mention} and unique perspective on [specific area] would be incredibly valuable to share with a wider audience.
            
            I'm currently working on [content format - podcast/article/video series] focused on [specific topic], and I believe your insights would provide tremendous value to our audience of [target audience description].
            
            **What I'm Looking For**:
            • [Specific topic/angle 1]
            • [Specific topic/angle 2]
            • [Specific topic/angle 3]
            
            **Time Commitment**: [Specific duration]
            **Format**: [Interview format]
            **Promotion**: I'll handle all promotion and share the final content across multiple channels
            
            Would you be interested in participating? I'm flexible on timing and format to work with your schedule.
            
            Thanks for considering!
            
            [Your name]
            """
        }
        
        return templates.get(template_type, templates["collaboration"])
    
    def _match_tone(self, tone_data: str) -> str:
        """Match tone to recipient and platform"""
        try:
            data = json.loads(tone_data)
            platform = data.get('platform', 'LinkedIn')
            recipient_style = data.get('style', 'professional')
            
            tone_guidelines = {
                "LinkedIn": {
                    "professional": "Formal but warm, focus on business value and mutual benefit",
                    "casual": "Professional yet approachable, use industry terminology appropriately",
                    "creative": "Professional with creative flair, acknowledge their unique style"
                },
                "Instagram": {
                    "professional": "Warm and authentic, visual-friendly language",
                    "casual": "Friendly and conversational, use emojis sparingly",
                    "creative": "Match their creative energy while staying professional"
                },
                "YouTube": {
                    "professional": "Enthusiastic yet professional, acknowledge their content format",
                    "casual": "Energetic and friendly, reference specific videos if possible",
                    "creative": "Match their creative style, show genuine appreciation for their work"
                },
                "X (Twitter)": {
                    "professional": "Concise and direct, respect the platform's brevity",
                    "casual": "Conversational and quick, use platform conventions",
                    "creative": "Creative but brief, engage with their tweet style"
                }
            }
            
            guidance = tone_guidelines.get(platform, tone_guidelines["LinkedIn"])
            return guidance.get(recipient_style, guidance["professional"])
        except Exception as e:
            return "Use a professional yet warm tone, focusing on mutual value and authentic connection."
    
    def _create_value_proposition(self, context: str) -> str:
        """Create compelling value proposition"""
        value_props = {
            "collaboration": "Mutual audience growth, shared expertise, and content amplification",
            "guest_post": "High-quality content for your audience, fresh perspective, and cross-promotion",
            "partnership": "Strategic alliance, resource sharing, and expanded market reach",
            "interview": "Thought leadership positioning, audience expansion, and content creation"
        }
        
        return value_props.get(context.lower(), "Mutual benefit and authentic value creation")
    
    def create_outreach_task(self, topic: str, tone: str, leads: List[Dict], outreach_type: str = "collaboration") -> Task:
        """Create an outreach task for the given leads"""
        
        task = Task(
            description=f"""
            Create personalized outreach messages for the following leads related to the topic: "{topic}"
            
            Outreach Type: {outreach_type}
            Brand Tone: {tone}
            
            For each lead, create:
            1. A personalized subject line
            2. A compelling outreach message that:
               - Acknowledges their specific work and expertise
               - Provides clear value proposition
               - Includes specific collaboration ideas
               - Maintains authentic, non-salesy tone
               - Includes appropriate call-to-action
            3. Follow-up message template (if needed)
            
            Personalization Requirements:
            - Reference their specific platform and content style
            - Acknowledge their follower count and engagement appropriately
            - Mention specific aspects of their work (if available)
            - Match the communication style of their platform
            - Ensure the message feels genuine and valuable
            
            Message Guidelines:
            - Keep initial messages concise but comprehensive
            - Lead with value, not what you want
            - Be specific about collaboration ideas
            - Include social proof where appropriate
            - End with a clear, low-pressure call-to-action
            
            Platform-Specific Considerations:
            - LinkedIn: Professional tone, business-focused value
            - Instagram: Visual-friendly, lifestyle-oriented approach
            - YouTube: Content collaboration focus, video-specific opportunities
            - X (Twitter): Brief, conversational, respect platform conventions
            
            Return a JSON object with outreach messages for each lead, including:
            - lead_id
            - subject_line
            - message_body
            - follow_up_template
            - platform_specific_notes
            """,
            agent=self.agent,
            expected_output="JSON object containing personalized outreach messages for each lead with subject lines, message bodies, and follow-up templates"
        )
        
        return task
    
    def execute_outreach_generation(self, topic: str, tone: str, leads: List[Dict], outreach_type: str = "collaboration") -> Dict[str, Any]:
        """Execute outreach generation and return results"""
        try:
            task = self.create_outreach_task(topic, tone, leads, outreach_type)
            result = task.execute()
            
            # Parse and structure the results
            outreach_messages = self._parse_outreach_result(result, topic, tone, leads, outreach_type)
            
            return {
                "success": True,
                "outreach_messages": outreach_messages,
                "total_messages": len(outreach_messages),
                "topic": topic,
                "outreach_type": outreach_type
            }
        except Exception as e:
            # Return mock outreach data if execution fails
            mock_messages = self._generate_mock_outreach(topic, tone, leads, outreach_type)
            return {
                "success": False,
                "error": str(e),
                "outreach_messages": mock_messages,
                "total_messages": len(mock_messages),
                "topic": topic,
                "outreach_type": outreach_type
            }
    
    def _parse_outreach_result(self, result: str, topic: str, tone: str, leads: List[Dict], outreach_type: str) -> List[Dict]:
        """Parse the agent's result into structured outreach data"""
        # This would parse the actual agent output
        # For now, return mock structured data
        return self._generate_mock_outreach(topic, tone, leads, outreach_type)
    
    def _generate_mock_outreach(self, topic: str, tone: str, leads: List[Dict], outreach_type: str) -> List[Dict]:
        """Generate mock outreach messages for testing"""
        outreach_messages = []
        
        for lead in leads[:5]:  # Limit to first 5 leads
            lead_id = lead.get('id', f"lead_{random.randint(1, 1000)}")
            name = lead.get('name', 'Content Creator')
            platform = lead.get('platform', 'LinkedIn')
            niche = lead.get('niche', topic)
            
            # Generate personalized message based on outreach type and platform
            message_data = self._create_personalized_message(
                name, platform, niche, topic, tone, outreach_type, lead
            )
            
            outreach_message = {
                "lead_id": lead_id,
                "recipient_name": name,
                "platform": platform,
                "subject_line": message_data["subject"],
                "message_body": message_data["body"],
                "follow_up_template": message_data["follow_up"],
                "estimated_response_rate": round(random.uniform(0.15, 0.35), 2),
                "best_send_time": self._get_best_send_time(platform),
                "personalization_score": round(random.uniform(0.7, 0.95), 2),
                "platform_specific_notes": message_data["notes"]
            }
            
            outreach_messages.append(outreach_message)
        
        return outreach_messages
    
    def _create_personalized_message(self, name: str, platform: str, niche: str, topic: str, tone: str, outreach_type: str, lead: Dict) -> Dict[str, str]:
        """Create a personalized message for a specific lead"""
        follower_count = lead.get('follower_count', 0)
        engagement_rate = lead.get('engagement_rate', 0)
        
        # Subject line templates
        subjects = {
            "collaboration": f"Collaboration idea for {name} - {topic}",
            "guest_post": f"Guest content opportunity - {topic}",
            "partnership": f"Partnership opportunity in {niche}",
            "interview": f"Interview request - {topic} expertise"
        }
        
        # Personalized greeting and context
        greeting = f"Hi {name},"
        social_proof = f"your {follower_count:,} followers" if follower_count > 1000 else "your engaged community"
        
        # Platform-specific message body
        if platform == "LinkedIn":
            body = f"""
{greeting}

I came across your LinkedIn profile and was impressed by your expertise in {niche}. Your insights on {topic.lower()} have been particularly valuable, and {social_proof} clearly appreciate the depth you bring to professional discussions.

I'm reaching out because I believe we could create something valuable together around {topic.lower()}. I'm working on content that explores the practical applications of {topic.lower()} for {niche} professionals, and I think your perspective would add tremendous value.

Here's what I have in mind:
• A collaborative piece exploring {topic.lower()} trends in {niche}
• Cross-promotion to both our professional networks
• Potential for ongoing content partnership

I'd love to explore this further if you're interested. Would you be open to a brief 15-minute call this week to discuss the possibilities?

Best regards,
[Your name]

P.S. Your recent post about {niche} really resonated with me - especially your point about staying authentic in professional content.
            """.strip()
        
        elif platform == "Instagram":
            body = f"""
{greeting}

I've been following your Instagram content and absolutely love how you share insights about {niche}! Your authentic approach to {topic.lower()} content really stands out in a crowded space.

I'm reaching out with a collaboration idea that I think could provide real value to both our communities. I'm creating content around {topic.lower()} and would love to explore how we might work together.

Some ideas I'm excited about:
✨ Joint content series on {topic.lower()} trends
✨ Cross-promotion to expand our reach
✨ Authentic storytelling that provides real value

Your visual storytelling style would be perfect for this type of content. Would you be interested in hearing more details?

Looking forward to potentially creating something amazing together!

[Your name]

P.S. {social_proof} are lucky to have such authentic content in their feed! 📸
            """.strip()
        
        elif platform == "YouTube":
            body = f"""
{greeting}

I've been a subscriber to your YouTube channel and really appreciate the quality content you create about {niche}. Your video on [related topic] was incredibly insightful and got me thinking about potential collaboration opportunities.

I'm working on content focused on {topic.lower()} and believe your expertise would add tremendous value. Here's what I'm thinking:

🎥 Potential collaboration formats:
• Guest appearance on each other's channels
• Joint series exploring {topic.lower()} in depth
• Cross-promotion to grow both our audiences

Your production quality and authentic presentation style would be perfect for this type of content collaboration. Plus, I think our audiences would really benefit from the combined perspectives.

Would you be interested in a quick call to discuss this further? I'm flexible on timing and format to work with your content schedule.

Thanks for considering!

[Your name]

P.S. Keep up the amazing work - your content consistently provides real value to the {niche} community! 🚀
            """.strip()
        
        else:  # Default to LinkedIn format
            body = f"""
{greeting}

I came across your {platform} profile and was impressed by your work in {niche}. Your insights on {topic.lower()} have been particularly valuable.

I'm reaching out because I believe we could create something valuable together. I'm working on {topic.lower()} content and think your perspective would add tremendous value.

Would you be interested in exploring a collaboration opportunity?

Best regards,
[Your name]
            """.strip()
        
        # Follow-up template
        follow_up = f"""
Subject: Following up - {topic} collaboration

Hi {name},

I wanted to follow up on my message about the {topic.lower()} collaboration opportunity. I understand you're busy, so no worries if the timing isn't right.

If you're interested but need more details, I'm happy to send over a brief outline of what I have in mind.

Thanks for your time!

[Your name]
        """.strip()
        
        # Platform-specific notes
        notes = {
            "LinkedIn": "Best sent Tuesday-Thursday, 9-11 AM. Include professional achievements in connection request.",
            "Instagram": "Best sent as DM after engaging with recent posts. Keep tone casual and visual.",
            "YouTube": "Consider commenting on recent videos first to establish connection.",
            "X (Twitter)": "Keep initial message brief. Consider public tweet engagement first."
        }.get(platform, "Standard business communication guidelines apply.")
        
        return {
            "subject": subjects.get(outreach_type, subjects["collaboration"]),
            "body": body,
            "follow_up": follow_up,
            "notes": notes
        }
    
    def _get_best_send_time(self, platform: str) -> str:
        """Get best send time for platform"""
        times = {
            "LinkedIn": "Tuesday-Thursday, 9-11 AM",
            "Instagram": "Monday-Friday, 11 AM-1 PM",
            "YouTube": "Tuesday-Thursday, 2-4 PM",
            "X (Twitter)": "Monday-Friday, 12-3 PM"
        }
        return times.get(platform, "Business hours, Tuesday-Thursday")