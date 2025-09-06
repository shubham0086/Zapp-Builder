import streamlit as st
from typing import Dict, List, Optional

class InputPanel:
    def __init__(self):
        self.platforms = [
            "LinkedIn", 
            "X (Twitter)", 
            "YouTube", 
            "Instagram", 
            "Newsletter", 
            "Blog",
            "TikTok",
            "Facebook"
        ]
        
        self.tones = [
            "Professional", 
            "Casual", 
            "Educational", 
            "Entertaining", 
            "Inspirational", 
            "Conversational",
            "Authoritative",
            "Friendly"
        ]
        
        self.content_lengths = ["Short", "Medium", "Long"]
    
    def render(self) -> Optional[Dict]:
        """Render input panel and return user inputs"""
        
        # Topic input
        topic = st.text_area(
            "🎯 **What's your topic or idea?**",
            placeholder="e.g., 'AI productivity tools for content creators' or 'The future of remote work'",
            help="Describe what you want to create content about. Be specific for better results.",
            height=100,
            key="topic_input"
        )
        
        if not topic:
            st.info("👆 Start by entering your topic or content idea")
            return None
        
        # Tone and Platform selection
        col1, col2 = st.columns(2)
        
        with col1:
            tone = st.selectbox(
                "🎨 **Choose your tone:**",
                self.tones,
                index=0,
                help="This will influence how your content is written"
            )
        
        with col2:
            content_length = st.selectbox(
                "📏 **Content length:**",
                self.content_lengths,
                index=1,
                help="Short: Social posts, Medium: Articles, Long: Deep-dive content"
            )
        
        # Platform selection
        platforms = st.multiselect(
            "📱 **Select target platforms:**",
            self.platforms,
            default=["LinkedIn"],
            help="Choose where you want to publish this content"
        )
        
        if not platforms:
            st.warning("Please select at least one platform")
            return None
        
        # Mode selection
        st.markdown("### 🎯 CrewAI Workflow")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            research_mode = st.checkbox(
                "🔍 **Research**", 
                value=True,
                help="Generate comprehensive research brief with sources"
            )
        
        with col2:
            lead_gen_mode = st.checkbox(
                "🎯 **Lead Generation**", 
                value=False,
                help="Find relevant creators, brands, and communities"
            )
        
        with col3:
            outreach_mode = st.checkbox(
                "📧 **Outreach**",
                value=False,
                help="Generate personalized outreach messages"
            )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                target_audience = st.text_input(
                    "Target Audience",
                    placeholder="e.g., 'Marketing professionals, Small business owners'",
                    help="Who is your content for?"
                )
                
                include_hashtags = st.checkbox("Include hashtags", value=True)
                
            with col2:
                include_cta = st.checkbox("Include call-to-action", value=True)
                include_sources = st.checkbox("Cite sources", value=True)
            
            custom_instructions = st.text_area(
                "Custom instructions (optional)",
                placeholder="Any specific requirements, style preferences, or constraints...",
                height=80
            )
        
        # Validation
        if not research_mode and not lead_gen_mode:
            st.info("💡 Select at least Research or Lead Generation to activate CrewAI agents")
        
        return {
            "topic": topic,
            "tone": tone,
            "platforms": platforms,
            "content_length": content_length,
            "research_mode": research_mode,
            "lead_gen_mode": lead_gen_mode,
            "outreach_mode": outreach_mode,
            "target_audience": target_audience,
            "include_hashtags": include_hashtags,
            "include_cta": include_cta,
            "include_sources": include_sources,
            "custom_instructions": custom_instructions
        }