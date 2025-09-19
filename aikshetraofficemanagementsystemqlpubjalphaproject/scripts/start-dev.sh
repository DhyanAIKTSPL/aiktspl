#!/bin/bash

# Development startup script
echo "🚀 Starting Office Management System in development mode..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    fi
    return 0
}

# Check required ports
check_port 3000 || echo "Frontend port 3000 is busy"
check_port 8000 || echo "Backend port 8000 is busy"
check_port 6379 || echo "Redis port 6379 is busy"

# Start Redis in background
echo "🔴 Starting Redis..."
redis-server --daemonize yes

# Start Django backend in background
echo "🐍 Starting Django backend..."
cd backend
source venv/bin/activate
python manage.py runserver &
DJANGO_PID=$!
cd ..

# Wait a moment for Django to start
sleep 3

# Start Next.js frontend
echo "⚛️  Starting Next.js frontend..."
npm run dev &
NEXTJS_PID=$!

# Function to cleanup processes on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $DJANGO_PID 2>/dev/null
    kill $NEXTJS_PID 2>/dev/null
    redis-cli shutdown 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo "✅ All services started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/schema/swagger-ui/"
echo "👑 Admin Panel: http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait
