# 🚀 Content Creator Studio - Setup Guide

## 📋 Quick Start (5 minutes)

### 1. Environment Setup
```bash
# Copy environment file
cp env.example .env

# Edit .env with your API keys
# At minimum, add your OpenAI API key:
# OPENAI_API_KEY=your_openai_key_here
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Option 1: Use the startup script
python start.py

# Option 2: Run manually
# Terminal 1 - Backend:
cd backend && uvicorn main:app --reload

# Terminal 2 - Frontend:
cd frontend && streamlit run streamlit_app.py
```

### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🐳 Docker Setup (Alternative)

### 1. Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Individual Docker Services
```bash
# Build and run backend
cd backend
docker build -t content-studio-backend .
docker run -p 8000:8000 content-studio-backend

# Build and run frontend
cd frontend
docker build -t content-studio-frontend .
docker run -p 8501:8501 content-studio-frontend
```

## 🔧 Configuration

### Required API Keys
Add these to your `.env` file:

```env
# Required for AI functionality
OPENAI_API_KEY=your_openai_key_here

# Optional but recommended
ANTHROPIC_API_KEY=your_anthropic_key_here
SERP_API_KEY=your_serp_api_key_here

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/content_studio
REDIS_URL=redis://localhost:6379
```

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | No | - |
| `SERP_API_KEY` | Search API key | No | - |
| `DATABASE_URL` | Database connection | No | sqlite:///./content_studio.db |
| `DEBUG` | Debug mode | No | true |
| `BACKEND_URL` | Backend URL for frontend | No | http://localhost:8000 |

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend tests/
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Generate content (example)
curl -X POST "http://localhost:8000/api/v1/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI productivity tools",
    "tone": "professional",
    "platforms": ["LinkedIn", "Twitter"],
    "research_mode": true
  }'
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Make sure you're in the project root
cd content-creator-studio

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### 2. Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Find process using port 8501
netstat -ano | findstr :8501
```

#### 3. Database Connection Issues
```bash
# For SQLite (default), no setup needed
# For PostgreSQL, ensure it's running and accessible
```

#### 4. API Key Issues
- Verify your API key is correct
- Check if you have sufficient credits
- Ensure the key has the right permissions

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
# or on Windows:
set DEBUG=true

# Run with verbose output
python start.py
```

## 📊 Project Structure

```
content-creator-studio/
├── frontend/                 # Streamlit web interface
│   ├── components/          # UI components
│   ├── utils/              # Utility functions
│   └── streamlit_app.py    # Main frontend app
├── backend/                 # FastAPI backend
│   ├── agents/             # CrewAI agents
│   ├── api/                # API routes and models
│   ├── core/               # Core configuration
│   └── services/           # Business logic services
├── database/               # Database schema
├── tests/                  # Test suite
└── docker-compose.yml      # Docker configuration
```

## 🎯 Next Steps

### Phase 1: Basic Functionality (Week 1)
1. ✅ Set up project structure
2. ✅ Create basic UI components
3. ✅ Implement mock API responses
4. 🔄 Connect real OpenAI API
5. 🔄 Test end-to-end workflow

### Phase 2: Enhanced Features (Week 2-3)
1. Add real research capabilities
2. Implement lead generation
3. Add content export features
4. Create user authentication
5. Add project management

### Phase 3: Production Ready (Week 4+)
1. Add comprehensive error handling
2. Implement rate limiting
3. Add monitoring and logging
4. Create deployment scripts
5. Add comprehensive testing

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in the terminal
3. Ensure all dependencies are installed
4. Verify your API keys are correct
5. Check the GitHub issues page

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)



