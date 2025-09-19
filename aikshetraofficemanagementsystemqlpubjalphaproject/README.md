# Office Management System

A comprehensive full-stack office management system built with Django REST API backend and Next.js frontend.

## Features

- **User Management**: Role-based access control (Admin, Employee, Trainee)
- **Employee Management**: Department and position tracking
- **Attendance System**: Real-time check-in/check-out with location tracking
- **Task Management**: Project assignment and progress tracking
- **Salary Management**: Payroll and compensation tracking
- **Learning Management**: Training modules and progress tracking
- **Real-time Notifications**: WebSocket-powered live updates

## Tech Stack

### Backend
- Django 4.2.7 with Django REST Framework
- PostgreSQL database
- Redis for caching and WebSocket support
- Django Channels for real-time functionality
- JWT authentication

### Frontend
- Next.js 14 with React 19
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Axios for API calls
- WebSocket integration

## Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Redis 6+

## Installation & Setup

### 1. Clone the Repository
\`\`\`bash
git clone <repository-url>
cd office-management-system
\`\`\`

### 2. Backend Setup (Django)

#### Create Virtual Environment
\`\`\`bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

#### Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

#### Environment Configuration
\`\`\`bash
cp .env.example .env
\`\`\`

Edit `.env` file with your configuration:
\`\`\`env
# Database
DATABASE_NAME=office_management
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
\`\`\`

#### Database Setup
\`\`\`bash
# Create PostgreSQL database
createdb office_management

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata fixtures/initial_data.json
\`\`\`

#### Start Backend Server
\`\`\`bash
python manage.py runserver
\`\`\`

The Django API will be available at `http://localhost:8000`

### 3. Frontend Setup (Next.js)

#### Install Dependencies
\`\`\`bash
# From project root
npm install
# or
pnpm install
\`\`\`

#### Environment Configuration
Create `.env.local` file in the root directory:
\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
\`\`\`

#### Start Frontend Server
\`\`\`bash
npm run dev
# or
pnpm dev
\`\`\`

The frontend will be available at `http://localhost:3000`

### 4. Redis Setup

#### Install Redis
\`\`\`bash
# On macOS with Homebrew
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# On Windows
# Download and install from https://redis.io/download
\`\`\`

#### Start Redis Server
\`\`\`bash
redis-server
\`\`\`

## Development Workflow

### Backend Development
\`\`\`bash
cd backend
source venv/bin/activate  # Activate virtual environment
python manage.py runserver  # Start Django server
\`\`\`

### Frontend Development
\`\`\`bash
npm run dev  # Start Next.js development server
\`\`\`

### Database Migrations
\`\`\`bash
cd backend
python manage.py makemigrations
python manage.py migrate
\`\`\`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
- Django Admin: `http://localhost:8000/admin/`

## Default Login Credentials

After creating a superuser, you can access the system with:
- **Admin Panel**: Use your superuser credentials
- **Frontend**: Create users through the admin panel or registration

## Project Structure

\`\`\`
office-management-system/
├── backend/                 # Django backend
│   ├── office_management/   # Main Django project
│   ├── accounts/           # User authentication
│   ├── employees/          # Employee management
│   ├── attendance/         # Attendance tracking
│   ├── tasks/             # Task management
│   ├── salary/            # Salary management
│   ├── learning/          # Learning management
│   ├── notifications/     # Real-time notifications
│   └── requirements.txt   # Python dependencies
├── src/                   # React components (legacy)
├── app/                   # Next.js app directory
├── components/            # Reusable UI components
├── lib/                   # Utility functions
└── package.json          # Node.js dependencies
\`\`\`

## Available Scripts

### Backend
- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Run database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files
- `python manage.py test` - Run tests

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure production database
3. Set up proper CORS settings
4. Use a production WSGI server like Gunicorn
5. Set up Redis for production

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred platform
3. Set production environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
