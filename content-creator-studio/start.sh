#!/bin/bash

# Content Creator Studio Startup Script

echo "🎨 Starting Content Creator Studio..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️ .env file not found. Creating from example..."
    cp .env.example .env
    echo "✅ Please edit .env file with your API keys before running again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Start backend in background
echo "🚀 Starting FastAPI backend..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Streamlit frontend..."
cd frontend
streamlit run streamlit_app.py &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Content Creator Studio is now running!"
echo ""
echo "📱 Frontend: http://localhost:8501"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Content Creator Studio..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 All services stopped."
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for processes
wait