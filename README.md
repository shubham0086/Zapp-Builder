# 🎨 Content Creator Studio

> AI-powered content creation and lead generation platform that turns ideas into engaging content across multiple platforms.

## 🚀 Features

- **🔍 AI Research**: Comprehensive topic research with source citations
- **🎯 Lead Generation**: Find relevant creators, brands, and communities  
- **📝 Content Creation**: Generate platform-native content for YouTube, Instagram, LinkedIn, X, and more
- **📧 Outreach Automation**: Personalized outreach messages
- **💾 Export Options**: CSV, JSON, Markdown exports
- **🎨 Brand Voice**: Maintain consistent tone across all content

## 🏗️ Architecture

- **Frontend**: Streamlit (Interactive web interface)
- **Backend**: FastAPI (High-performance API)
- **AI Agents**: CrewAI (Multi-agent orchestration)
- **Database**: PostgreSQL + pgvector (Relational + vector storage)
- **Cache**: Redis (Session management)

## 🚦 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL with pgvector extension

### 1. Clone & Setup
```bash
git clone <repository-url>
cd content-creator-studio
cp env.example .env
# Edit .env with your API keys
```

### 2. Run with Docker
```bash
docker-compose up -d
```

### 3. Access the Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run frontend
streamlit run frontend/streamlit_app.py

# Run backend (in another terminal)
cd backend && uvicorn main:app --reload
```

## 📝 API Usage

### Generate Content
```bash
curl -X POST "http://localhost:8000/api/v1/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI productivity tools",
    "tone": "professional",
    "platforms": ["LinkedIn", "X"],
    "research_mode": true,
    "lead_gen_mode": false
  }'
```

## 🔧 Configuration

Key environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `SERP_API_KEY`: Search API for research

## 📊 Project Status

- ✅ MVP: Basic research and content generation
- 🚧 v1.0: Lead generation, outreach, payments
- 📋 v1.1: Advanced filtering, brand voice memory

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- 📖 Documentation
- 🐛 Issue Tracker
- 💬 Discussions



