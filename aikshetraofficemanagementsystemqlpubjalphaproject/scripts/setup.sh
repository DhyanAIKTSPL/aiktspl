#!/bin/bash

# Office Management System Setup Script
echo "🚀 Setting up Office Management System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install PostgreSQL 12+ first."
    exit 1
fi

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed. Please install Redis 6+ first."
    exit 1
fi

echo "✅ All prerequisites are installed!"

# Backend setup
echo "🔧 Setting up Django backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Please edit backend/.env with your database credentials"
fi

# Create database (you may need to adjust this based on your PostgreSQL setup)
echo "📊 Setting up database..."
createdb office_management 2>/dev/null || echo "Database may already exist"

# Run migrations
python manage.py migrate

# Create superuser (interactive)
echo "👤 Creating superuser account..."
python manage.py createsuperuser

cd ..

# Frontend setup
echo "🎨 Setting up Next.js frontend..."

# Install Node.js dependencies
npm install

# Create frontend environment file
if [ ! -f .env.local ]; then
    cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
EOL
    echo "✅ Created .env.local with default settings"
fi

echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Start Redis: redis-server"
echo "2. Start Django backend: cd backend && source venv/bin/activate && python manage.py runserver"
echo "3. Start Next.js frontend: npm run dev"
echo ""
echo "Then visit http://localhost:3000 to access the application"
