# 🎨 Content Creator Studio

> **AI-powered content creation and lead generation platform with CrewAI agents**

Transform your ideas into engaging content across multiple platforms using advanced AI agents that research, generate leads, create content, and craft personalized outreach messages.

## 🚀 Features

### 🤖 **CrewAI Agent Orchestration**
- **Research Agent**: Comprehensive topic research with source citations
- **Lead Generation Agent**: Find relevant creators, brands, and communities  
- **Content Creator Agent**: Generate platform-native content
- **Outreach Agent**: Personalized outreach messages

### 📱 **Multi-Platform Support**
- LinkedIn (Professional networking)
- X/Twitter (Social engagement)
- YouTube (Video descriptions)
- Instagram (Visual content)
- Newsletter (Email marketing)
- Blog (Long-form content)

### 🎯 **Intelligent Workflows**
- Research-only mode for market analysis
- Lead generation with relevance scoring
- Content creation with platform optimization
- Outreach automation with personalization

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   PostgreSQL    │
│   Frontend      │◄──►│   Backend       │◄──►│   + pgvector    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   CrewAI        │
                       │   Agents        │
                       │                 │
                       └─────────────────┘
```

- **Frontend**: Streamlit (Interactive web interface)
- **Backend**: FastAPI (High-performance API with async support)
- **AI Agents**: CrewAI (Multi-agent orchestration)
- **Database**: PostgreSQL + pgvector (Relational + vector storage)
- **Cache**: Redis (Session management and rate limiting)

## 🚦 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (optional but recommended)
- OpenAI API key (for CrewAI agents)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/content-creator-studio.git
cd content-creator-studio
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` file with your API keys:
```env
# Required for CrewAI agents
OPENAI_API_KEY=your_openai_api_key_here

# Optional for enhanced functionality
ANTHROPIC_API_KEY=your_anthropic_key
SERP_API_KEY=your_serp_api_key

# Database (use default for SQLite)
DATABASE_URL=sqlite:///./content_studio.db
```

### 3. Installation Options

#### Option A: Docker (Recommended)
```bash
docker-compose up -d
```

#### Option B: Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
cd backend && python main.py &

# Run frontend (in another terminal)
cd frontend && streamlit run streamlit_app.py
```

### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 Usage Guide

### Basic Content Generation
1. **Enter your topic**: "AI productivity tools for remote teams"
2. **Select platforms**: LinkedIn, Newsletter
3. **Choose tone**: Professional
4. **Enable research mode**: ✅
5. **Click Generate**: Let CrewAI agents work their magic!

### Advanced Workflows
```python
# Research-only workflow
POST /api/v1/research-only
{
  "topic": "Sustainable technology trends",
  "platforms": ["YouTube", "Blog"]
}

# Complete workflow with all agents
POST /api/v1/generate-content
{
  "topic": "Personal branding for entrepreneurs",
  "tone": "inspirational",
  "platforms": ["LinkedIn", "Instagram"],
  "research_mode": true,
  "lead_gen_mode": true,
  "outreach_mode": true,
  "target_audience": "Startup founders and entrepreneurs"
}
```

### API Response Example
```json
{
  "request_id": "crew_20240115_143022",
  "status": "completed",
  "success": true,
  "topic": "AI productivity tools",
  "platforms": ["LinkedIn", "Newsletter"],
  "research_brief": "# Research Brief: AI Productivity Tools...",
  "leads": [
    {
      "name": "TechExpert",
      "platform": "LinkedIn",
      "relevance_score": 0.92,
      "follower_count": 45000
    }
  ],
  "content": {
    "LinkedIn": "🚀 The Future of AI Productivity Tools...",
    "Newsletter": "Subject: The AI Revolution in Productivity..."
  },
  "sources": ["https://example.com/source1"],
  "workflow_steps": ["research", "lead_generation", "content_creation"],
  "total_duration": "0:02:15"
}
```

## 🔧 Configuration

### CrewAI Agent Settings
```python
# backend/core/config.py
class Settings(BaseSettings):
    # Agent Configuration
    MAX_RESEARCH_SOURCES: int = 10
    MAX_LEAD_RESULTS: int = 50
    CONTENT_GENERATION_TIMEOUT: int = 120
    
    # LLM Settings
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
```

### Platform Specifications
Each platform has optimized settings:
- **LinkedIn**: 3000 chars, professional tone, 3-5 hashtags
- **X/Twitter**: 280 chars, conversational, thread support
- **Instagram**: 2200 chars, visual focus, 5-10 hashtags
- **YouTube**: 5000 chars, engaging descriptions, SEO optimized

## 🤖 CrewAI Agents Deep Dive

### Research Agent
```python
# Capabilities
- Web search and content analysis
- Trend identification
- Source citation and verification
- Market research compilation

# Tools
- DuckDuckGo search
- Content analyzer
- Trend analyzer
```

### Lead Generation Agent
```python
# Capabilities  
- Social media profile discovery
- Influencer analysis and scoring
- Community identification
- Brand research

# Output
- Relevance scores (0-1)
- Engagement metrics
- Contact information
- Outreach recommendations
```

### Content Creator Agent
```python
# Capabilities
- Platform-specific optimization
- Hashtag generation
- Engagement enhancement
- Multi-format support

# Platform Adaptations
- LinkedIn: Professional networking focus
- Instagram: Visual storytelling
- YouTube: Educational/entertainment value
- Newsletter: Email marketing best practices
```

### Outreach Agent
```python
# Capabilities
- Personalized message crafting
- Tone matching
- Value proposition creation
- Follow-up templates

# Personalization Factors
- Recipient platform behavior
- Follower count and engagement
- Content style and niche
- Optimal send timing
```

## 📊 Monitoring & Analytics

### Agent Performance Metrics
- Research source quality and relevance
- Lead generation accuracy and scoring
- Content engagement predictions
- Outreach response rate estimates

### Workflow Tracking
```sql
-- Monitor workflow executions
SELECT 
    workflow_type,
    agent_name,
    AVG(EXTRACT(EPOCH FROM (end_time - start_time))) as avg_duration,
    COUNT(*) as total_executions,
    COUNT(*) FILTER (WHERE status = 'completed') as successful
FROM workflow_executions 
GROUP BY workflow_type, agent_name;
```

## 🔐 Security & Compliance

### Data Protection
- User data encryption at rest
- API key secure storage
- Session management with Redis
- GDPR compliance ready

### Rate Limiting
- API endpoint protection
- LLM usage monitoring  
- Credit-based usage tracking
- Abuse prevention

### Ethical AI Guidelines
- Robots.txt compliance for web scraping
- PII detection and redaction
- Opt-out mechanisms for outreach
- Transparent AI-generated content labeling

## 🚧 Development

### Project Structure
```
content-creator-studio/
├── frontend/           # Streamlit UI
│   ├── components/     # UI components
│   ├── utils/         # Frontend utilities
│   └── streamlit_app.py
├── backend/           # FastAPI backend
│   ├── agents/        # CrewAI agents
│   ├── api/          # API routes
│   ├── core/         # Core functionality
│   └── services/     # Business logic
├── database/         # Database schemas
├── tests/           # Test suites
└── tools/          # Utility tools
```

### Running Tests
```bash
# Backend tests
cd backend && pytest

# Frontend tests  
cd frontend && pytest

# Integration tests
pytest tests/integration/
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📈 Roadmap

### Phase 1: MVP ✅
- [x] Basic CrewAI agent implementation
- [x] Multi-platform content generation
- [x] Research and lead generation
- [x] Streamlit frontend

### Phase 2: Enhanced Features 🚧
- [ ] Advanced lead scoring algorithms
- [ ] Brand voice memory and consistency
- [ ] Content performance analytics
- [ ] Automated outreach scheduling

### Phase 3: Enterprise Features 📋
- [ ] Team collaboration tools
- [ ] Advanced workflow automation
- [ ] Custom agent training
- [ ] Enterprise integrations

## 🆘 Support

### Documentation
- [API Documentation](http://localhost:8000/docs)
- [CrewAI Agent Guide](docs/agents.md)
- [Platform Optimization](docs/platforms.md)

### Community
- [GitHub Issues](https://github.com/yourusername/content-creator-studio/issues)
- [Discussions](https://github.com/yourusername/content-creator-studio/discussions)
- [Discord Community](https://discord.gg/content-creator-studio)

### Professional Support
- Email: support@contentcreatorstudio.com
- Enterprise: enterprise@contentcreatorstudio.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: For the amazing multi-agent framework
- **Streamlit**: For the intuitive frontend framework
- **FastAPI**: For the high-performance backend framework
- **OpenAI**: For powering the AI agents
- **Community Contributors**: For making this project better

---

<div align="center">

**Built with ❤️ using CrewAI, Streamlit, and FastAPI**

[⭐ Star this repo](https://github.com/yourusername/content-creator-studio) | [🐛 Report Bug](https://github.com/yourusername/content-creator-studio/issues) | [💡 Request Feature](https://github.com/yourusername/content-creator-studio/issues)

</div>