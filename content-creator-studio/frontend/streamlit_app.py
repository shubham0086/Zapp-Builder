import streamlit as st
import httpx
import asyncio
import json
from datetime import datetime
import os
import sys

# Add the current directory to the path so we can import components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.input_panel import InputPanel
from components.results_dashboard import ResultsDashboard
from components.auth import AuthManager
from utils.session_manager import SessionManager

# Page config
st.set_page_config(
    page_title="Content Creator Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 2rem;
    font-weight: 600;
}

.success-box {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.status-indicator {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.status-ready {
    background: #d4edda;
    color: #155724;
}

.status-working {
    background: #fff3cd;
    color: #856404;
}

.status-error {
    background: #f8d7da;
    color: #721c24;
}
</style>
""", unsafe_allow_html=True)

class ContentCreatorStudio:
    def __init__(self):
        # Get backend URL from environment or use default
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        # Initialize components
        self.auth_manager = AuthManager()
        self.session_manager = SessionManager()
        self.input_panel = InputPanel()
        self.results_dashboard = ResultsDashboard()
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = True  # Simplified for demo
        
        if 'backend_status' not in st.session_state:
            st.session_state.backend_status = None
        
    def run(self):
        """Main application entry point"""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🎨 Content Creator Studio</h1>
            <p>AI-Powered Research, Lead Generation & Content Creation with CrewAI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check backend status
        self.check_backend_status()
        
        # Authentication check (simplified for demo)
        if not st.session_state.get('authenticated', False):
            self.render_auth()
            return
            
        # Sidebar
        with st.sidebar:
            self.render_sidebar()
        
        # Main content
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.header("📝 Content Generation")
            inputs = self.input_panel.render()
            
            # Generation button
            if inputs:
                if st.button("🚀 Generate Content", type="primary", use_container_width=True):
                    self.generate_content(inputs)
            
        with col2:
            st.header("📊 Results & Analytics")
            
            # Display backend status
            self.render_backend_status()
            
            # Display results if available
            if 'results' in st.session_state:
                self.results_dashboard.render(st.session_state.results)
            else:
                st.info("🤖 Results will appear here after content generation")
                
                # Show example results button
                if st.button("👀 Show Example Results"):
                    st.session_state.results = self.get_example_results()
                    st.rerun()
    
    def check_backend_status(self):
        """Check if backend is available"""
        try:
            response = httpx.get(f"{self.backend_url}/health", timeout=5.0)
            if response.status_code == 200:
                st.session_state.backend_status = response.json()
            else:
                st.session_state.backend_status = {"status": "error", "message": "Backend unavailable"}
        except Exception as e:
            st.session_state.backend_status = {"status": "error", "message": str(e)}
    
    def render_backend_status(self):
        """Render backend status indicator"""
        status = st.session_state.get('backend_status', {})
        
        if status.get('status') == 'healthy':
            st.markdown("""
            <div class="status-indicator status-ready">
                ✅ Backend Ready - CrewAI Agents Online
            </div>
            """, unsafe_allow_html=True)
            
            # Show agent capabilities
            agents = status.get('agent_capabilities', 0)
            if agents:
                st.caption(f"🤖 {agents} AI agents ready for content creation")
        else:
            st.markdown("""
            <div class="status-indicator status-error">
                ❌ Backend Offline - Using Demo Mode
            </div>
            """, unsafe_allow_html=True)
            st.caption("⚠️ Connect to backend for full CrewAI functionality")
    
    def render_auth(self):
        """Simple authentication for demo"""
        st.header("🔐 Welcome to Content Creator Studio")
        
        with st.form("auth_form"):
            email = st.text_input("Email", value="demo@example.com")
            password = st.text_input("Password", type="password", value="demo")
            
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("Login", type="primary")
            with col2:
                demo_btn = st.form_submit_button("Demo Mode")
            
            if login_btn or demo_btn:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.rerun()
    
    def render_sidebar(self):
        """Render sidebar with user info and settings"""
        st.header("👤 Dashboard")
        
        # User info
        user_email = st.session_state.get('user_email', 'demo@example.com')
        st.write(f"**Email:** {user_email}")
        st.write(f"**Plan:** Free")
        st.write(f"**Credits:** 100")
        
        st.divider()
        
        # Backend info
        st.header("🔧 System Status")
        status = st.session_state.get('backend_status', {})
        
        if status.get('status') == 'healthy':
            st.success("✅ All systems operational")
            st.write(f"**Agents:** {status.get('agent_capabilities', 'N/A')}")
            st.write(f"**Version:** {status.get('version', 'N/A')}")
        else:
            st.warning("⚠️ Backend unavailable")
            st.write("**Mode:** Demo only")
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        default_tone = st.selectbox("Default Tone", 
                                  ["Professional", "Casual", "Educational", "Inspirational"])
        max_results = st.slider("Max Results", 5, 50, 20)
        
        st.divider()
        
        # Quick actions
        st.header("⚡ Quick Actions")
        if st.button("🔄 Refresh Status"):
            self.check_backend_status()
            st.rerun()
        
        if st.button("🗑️ Clear Session"):
            for key in list(st.session_state.keys()):
                if key not in ['authenticated', 'user_email']:
                    del st.session_state[key]
            st.rerun()
        
        if st.button("📤 Export Results"):
            if 'results' in st.session_state:
                self.export_results()
            else:
                st.warning("No results to export")
    
    def generate_content(self, inputs):
        """Generate content using backend API or demo mode"""
        with st.spinner("🤖 CrewAI agents are working on your content..."):
            try:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Initializing agents...")
                progress_bar.progress(10)
                
                # Check if backend is available
                backend_status = st.session_state.get('backend_status', {})
                
                if backend_status.get('status') == 'healthy':
                    # Use real backend
                    status_text.text("📡 Connecting to CrewAI backend...")
                    progress_bar.progress(20)
                    
                    response = httpx.post(
                        f"{self.backend_url}/api/v1/generate-content",
                        json=inputs,
                        timeout=180.0  # 3 minutes timeout for agent processing
                    )
                    
                    status_text.text("🤖 Agents processing request...")
                    progress_bar.progress(60)
                    
                    if response.status_code == 200:
                        results = response.json()
                        st.session_state.results = results
                        
                        status_text.text("✅ Content generation complete!")
                        progress_bar.progress(100)
                        
                        st.success("🎉 CrewAI agents completed your request!")
                        st.rerun()
                    else:
                        st.error(f"❌ Backend error: {response.text}")
                        
                else:
                    # Use demo mode
                    status_text.text("⚠️ Backend unavailable - using demo mode...")
                    progress_bar.progress(30)
                    
                    # Simulate processing time
                    import time
                    time.sleep(2)
                    
                    status_text.text("🎭 Generating demo content...")
                    progress_bar.progress(70)
                    
                    time.sleep(1)
                    
                    # Generate demo results
                    demo_results = self.get_demo_results(inputs)
                    st.session_state.results = demo_results
                    
                    status_text.text("✅ Demo content ready!")
                    progress_bar.progress(100)
                    
                    st.warning("🎭 Demo mode - Connect backend for full CrewAI functionality")
                    st.rerun()
                    
            except httpx.ConnectError:
                # Fallback to demo mode
                st.warning("🔧 Backend not available - showing demo content")
                demo_results = self.get_demo_results(inputs)
                st.session_state.results = demo_results
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    
    def get_demo_results(self, inputs):
        """Generate demo results based on inputs"""
        return {
            "request_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "success": True,
            "topic": inputs['topic'],
            "platforms": inputs['platforms'],
            "research_brief": f"""
# Research Brief: {inputs['topic']}

## Executive Summary
Based on comprehensive analysis, **{inputs['topic']}** presents significant opportunities for content creation across {', '.join(inputs['platforms'])}.

## Key Insights
- **Trending Status**: High interest with 45% growth in related searches
- **Audience Engagement**: {inputs['tone']} tone shows 85% positive response rate
- **Content Performance**: {inputs.get('content_length', 'medium')} format optimal for target platforms
- **Market Opportunity**: Growing demand in target demographics

## Strategic Recommendations
1. Focus on practical applications and real-world examples
2. Include interactive elements to boost engagement
3. Cross-promote content across selected platforms
4. Leverage trending hashtags and keywords

## Content Angles
- How-to guides and tutorials
- Industry insights and predictions
- Case studies and success stories
- Expert interviews and opinions

*This research brief was generated by CrewAI research agents*
            """.strip(),
            "leads": [
                {
                    "id": "lead_1",
                    "name": f"{inputs['topic'].title()}Expert",
                    "platform": inputs['platforms'][0] if inputs['platforms'] else "LinkedIn",
                    "follower_count": 45000,
                    "engagement_rate": 0.042,
                    "relevance_score": 0.92,
                    "profile_url": "https://example.com/expert1",
                    "bio": f"Leading expert in {inputs['topic']} with 10+ years experience",
                    "tags": [inputs['topic'], "Expert", "Influencer"]
                },
                {
                    "id": "lead_2", 
                    "name": f"{inputs['topic'].title()}Guru",
                    "platform": inputs['platforms'][1] if len(inputs['platforms']) > 1 else "YouTube",
                    "follower_count": 128000,
                    "engagement_rate": 0.035,
                    "relevance_score": 0.88,
                    "profile_url": "https://example.com/guru1",
                    "bio": f"Content creator specializing in {inputs['topic']}",
                    "tags": [inputs['topic'], "Creator", "Thought Leader"]
                }
            ] if inputs.get('lead_gen_mode') else None,
            "content": {
                platform: self.generate_demo_content(inputs['topic'], inputs['tone'], platform)
                for platform in inputs['platforms']
            },
            "sources": [
                "https://example.com/research-source-1",
                "https://example.com/research-source-2",
                "https://example.com/research-source-3"
            ],
            "workflow_steps": ["research", "content_creation"] + (["lead_generation"] if inputs.get('lead_gen_mode') else []),
            "total_duration": "0:02:15",
            "created_at": datetime.now().isoformat()
        }
    
    def generate_demo_content(self, topic: str, tone: str, platform: str) -> str:
        """Generate demo content for a specific platform"""
        content_templates = {
            "LinkedIn": f"""
🚀 The Future of {topic}: What Professionals Need to Know

{topic} is transforming how we work and think. Here are the key insights every professional should understand:

🔍 **Current Landscape:**
The field is evolving rapidly, with new developments emerging weekly. Organizations that adapt quickly are seeing significant competitive advantages.

📈 **Key Trends:**
• Increased adoption across industries
• Growing investment in related technologies  
• Shift in required skill sets
• New opportunities for innovation

💡 **Practical Applications:**
Smart companies are implementing {topic.lower()} solutions to:
- Streamline operations
- Enhance decision-making
- Improve customer experiences
- Drive competitive advantage

🎯 **What This Means for You:**
Understanding {topic.lower()} is becoming essential for career growth. The time to start learning is now.

What's your experience with {topic.lower()}? Share your thoughts in the comments! 👇

#Innovation #{topic.replace(' ', '')} #ProfessionalDevelopment #FutureOfWork
            """.strip(),
            
            "X (Twitter)": f"""
🧵 Thread: Why {topic} is bigger than you think

1/ {topic} isn't just a buzzword - it's reshaping entire industries. Here's what you need to know 👇

2/ The stats are mind-blowing: Companies using {topic.lower()} are seeing 40% faster growth and 25% higher efficiency.

3/ But here's the thing - it's not just about the technology. It's about how we adapt and evolve with it.

4/ Three areas where {topic.lower()} is making the biggest impact:
• Decision making
• Customer experience  
• Operational efficiency

5/ The question isn't IF this will affect your industry, but WHEN. Smart professionals are already preparing.

6/ My advice? Start learning now. The future belongs to those who embrace change.

What's your take on {topic.lower()}? Drop your thoughts below! 👇

#{topic.replace(' ', '')} #Innovation #TechTrends
            """.strip(),
            
            "Instagram": f"""
✨ Let's talk about {topic} ✨

This is changing everything, and I'm here for it! 🙌

{topic} isn't just tech talk - it's the future of how we work, create, and connect. And honestly? The possibilities are endless.

🌟 What's got me excited:
• New opportunities we never imagined
• Tools that actually make life easier  
• A future that's more connected than ever
• Innovation happening at lightning speed

💭 I used to think {topic.lower()} was just for experts, but I was so wrong. It's for creators, entrepreneurs, students - literally everyone.

The coolest part? We're just getting started. What we'll see in the next few years is going to be incredible 🤯

🔥 Ready to dive deeper? Check my stories for resources!

What questions do you have about {topic.lower()}? Drop them below! 👇✨

#{topic.replace(' ', '')} #Innovation #FutureTech #ContentCreator #TechTalk #Inspiration
            """.strip(),
            
            "YouTube": f"""
🎬 The Complete Guide to {topic}: Everything You Need to Know in 2024

Welcome back! Today we're diving deep into {topic} - one of your most requested topics.

📋 What We'll Cover:
• What {topic.lower()} actually means (in simple terms!)
• Why it matters for your career/business
• Real-world examples and case studies
• How to get started today
• Common mistakes to avoid
• Future predictions and trends

🚀 Why This Matters Now:
The landscape is changing faster than ever. Companies that understand {topic.lower()} are pulling ahead, while others are getting left behind.

💡 Perfect For:
• Professionals looking to future-proof careers
• Business owners wanting to stay competitive  
• Students preparing for the job market
• Anyone curious about emerging trends

By the end of this video, you'll have a clear roadmap for leveraging {topic.lower()} in your field.

Don't forget to subscribe and hit that notification bell! 🔔

Let's jump right in...

#{topic.replace(' ', '')} #Education #TechExplained #CareerGrowth #Innovation
            """.strip(),
            
            "Newsletter": f"""
📧 Subject: The {topic} Revolution: Your Weekly Insight

Dear Subscriber,

This week, I want to discuss something that's been on everyone's mind - {topic}.

🔍 **THE BIG PICTURE**

{topic} isn't just another trend. It's fundamentally changing how we approach problems, make decisions, and create value.

📊 **BY THE NUMBERS**

Recent studies show:
• 73% of executives consider {topic.lower()} a strategic priority
• Companies implementing solutions see 35% faster growth
• Job postings requiring related skills increased 150% this year

💡 **REAL-WORLD IMPACT**

I've been talking to professionals across industries, and the pattern is clear: those who embrace {topic.lower()} aren't just surviving change - they're thriving.

Take Sarah, a marketing manager who integrated {topic.lower()} into her campaigns. Result? 40% higher engagement and a promotion within six months.

🎯 **WHAT THIS MEANS FOR YOU**

Three immediate actions you can take:

1. **Educate yourself**: Spend 30 minutes this week learning about {topic.lower()}
2. **Identify opportunities**: Where could {topic.lower()} add value in your role?
3. **Start small**: Pick one area to experiment with

🚀 **LOOKING AHEAD**

Next week, I'll share a detailed case study of how a Fortune 500 company transformed their operations using {topic.lower()}.

Until then, keep innovating!

Best regards,
[Your Name]

P.S. What's your biggest question about {topic.lower()}? Hit reply - I read every email!
            """.strip(),
            
            "Blog": f"""
# The Complete Guide to {topic}: Transforming Industries in 2024

*Reading time: 8 minutes | Last updated: January 2024*

## Introduction

In today's rapidly evolving landscape, {topic.lower()} has emerged as a transformative force reshaping industries and redefining how we approach complex challenges.

## What is {topic}?

{topic} represents a fundamental shift in how we process information, make decisions, and create value. At its core, it's about leveraging advanced capabilities to augment human intelligence.

### Key Characteristics:
- **Scalability**: Solutions that grow with your needs
- **Efficiency**: Dramatic improvements in speed and accuracy  
- **Adaptability**: Systems that learn and improve
- **Integration**: Seamless workflow connection

## Current Market Landscape

### Growth Metrics
- **Market Size**: Projected to reach $X billion by 2025
- **Adoption Rate**: 60% of Fortune 500 companies now use solutions
- **Investment**: VC funding increased 200% year-over-year
- **Job Market**: 100,000+ new positions created

### Industry Applications

**Healthcare**: Revolutionizing diagnosis and treatment
**Finance**: Enhancing fraud detection and risk assessment
**Manufacturing**: Optimizing supply chains and maintenance
**Education**: Personalizing learning experiences

## Getting Started: A Practical Roadmap

### Phase 1: Assessment (Weeks 1-2)
- Audit current processes
- Identify opportunities
- Define success metrics

### Phase 2: Planning (Weeks 3-4)  
- Develop strategy
- Select tools
- Create timeline

### Phase 3: Implementation (Months 2-6)
- Start with pilots
- Train team
- Monitor progress

## Future Outlook

The next 2-3 years will see:
- Increased automation across industries
- More sophisticated capabilities
- Enhanced accessibility

## Conclusion

{topic} represents more than technological advancement - it's a fundamental shift in how we work and create value. Organizations that embrace this change early will have significant advantages.

The key is to start now, even small. Begin with education, identify opportunities, and gradually build expertise.

---

*Ready to explore {topic} further? Subscribe for weekly insights or contact our team for consultation.*
            """.strip()
        }
        
        return content_templates.get(platform, content_templates["LinkedIn"])
    
    def get_example_results(self):
        """Get example results for demonstration"""
        return {
            "request_id": "example_12345",
            "status": "completed", 
            "success": True,
            "topic": "AI-powered content creation tools",
            "platforms": ["LinkedIn", "YouTube"],
            "research_brief": "Comprehensive analysis of AI content creation trends...",
            "content": {
                "LinkedIn": "Professional post about AI content tools...",
                "YouTube": "Video description for AI tools tutorial..."
            },
            "sources": ["https://example1.com", "https://example2.com"],
            "workflow_steps": ["research", "content_creation"],
            "created_at": datetime.now().isoformat()
        }
    
    def export_results(self):
        """Export results to various formats"""
        results = st.session_state.get('results', {})
        
        # Create export data
        export_data = {
            "request_id": results.get('request_id', 'unknown'),
            "topic": results.get('topic', 'Unknown'),
            "generated_at": results.get('created_at', datetime.now().isoformat()),
            "research_brief": results.get('research_brief', ''),
            "leads": results.get('leads', []),
            "content": results.get('content', {}),
            "sources": results.get('sources', [])
        }
        
        # Convert to JSON for download
        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"content_studio_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    app = ContentCreatorStudio()
    app.run()