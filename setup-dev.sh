#!/bin/bash

# INNERA Development Setup Script
# This script sets up the development environment for the INNERA project

set -e  # Exit on any error

echo "🚀 Setting up CareSync Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.11+ is not installed. Please install Python first."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Some features may not work."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_warning "Docker Compose is not installed. Some features may not work."
    fi
    
    print_success "System requirements check completed."
}

# Setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created."
    else
        print_status "Virtual environment already exists."
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    print_success "Python environment setup completed."
}

# Setup frontend dependencies
setup_frontend() {
    print_status "Setting up frontend dependencies..."
    
    cd frontend-web
    
    # Install npm dependencies
    npm install
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
VITE_API_URL=http://localhost:5000/api
VITE_APP_VERSION=1.0.0
EOF
        print_success "Frontend environment file created."
    fi
    
    cd ..
    
    print_success "Frontend setup completed."
}

# Setup backend environment
setup_backend() {
    print_status "Setting up backend environment..."
    
    cd backend
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
LOG_FILE=logs/innera_backend.log
BCRYPT_LOG_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400
EOF
        print_success "Backend environment file created."
    fi
    
    # Create logs directory
    mkdir -p logs
    
    cd ..
    
    print_success "Backend setup completed."
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    # Check if Docker is available
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        print_status "Starting database services with Docker..."
        docker-compose up -d postgres redis
        
        # Wait for database to be ready
        print_status "Waiting for database to be ready..."
        sleep 10
        
        print_success "Database services started."
    else
        print_warning "Docker not available. Please start PostgreSQL and Redis manually."
        print_warning "PostgreSQL should be running on localhost:5432"
        print_warning "Redis should be running on localhost:6379"
    fi
}

# Create development scripts
create_dev_scripts() {
    print_status "Creating development scripts..."
    
    # Create start-backend.sh
    cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source ../venv/bin/activate
python main.py
EOF
    chmod +x start-backend.sh
    
    # Create start-frontend.sh
    cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend-web
npm run dev
EOF
    chmod +x start-frontend.sh
    
    # Create start-all.sh
    cat > start-all.sh << 'EOF'
#!/bin/bash
# Start all services
echo "Starting INNERA development environment..."

# Start database services
docker-compose up -d postgres redis

# Wait for database
sleep 5

# Start backend
cd backend
source ../venv/bin/activate
python main.py &
BACKEND_PID=$!

# Start frontend
cd ../frontend-web
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Services started. Press Ctrl+C to stop all services."

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
    chmod +x start-all.sh
    
    print_success "Development scripts created."
}

# Display next steps
show_next_steps() {
    echo ""
    echo "🎉 CareSync Development Environment Setup Complete!"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Start the backend:"
    echo "   ./start-backend.sh"
    echo ""
    echo "2. Start the frontend (in a new terminal):"
    echo "   ./start-frontend.sh"
    echo ""
    echo "3. Or start everything at once:"
    echo "   ./start-all.sh"
    echo ""
    echo "4. Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:5000"
    echo "   API Health: http://localhost:5000/api/health"
    echo ""
    echo "5. View logs:"
    echo "   Backend logs: backend/logs/"
    echo "   Docker logs: docker-compose logs -f"
    echo ""
    echo "6. Database access:"
    echo "   PostgreSQL: localhost:5432"
    echo "   Redis: localhost:6379"
    echo ""
    echo "Happy coding! 🚀"
}

# Main setup function
main() {
    echo "=========================================="
    echo "  CareSync Development Environment Setup"
    echo "=========================================="
    echo ""
    
    check_requirements
    setup_python_env
    setup_frontend
    setup_backend
    setup_database
    create_dev_scripts
    show_next_steps
}

# Run main function
main "$@" 