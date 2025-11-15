# LearnSpace Project

Educational Platform built with Django, Celery, Redis and PostgreSQL.

## Prerequisites

- Docker
- Docker Compose
- Python 3.13+ (for local development)
- Poetry (for local development)

## Quick Start

### 1. Clone the repository
```bash
git clone <https://github.com/AndreySapeshko/LearnSpaceProject>
cd LearnSpaceProject
```

### 2. Environment Configuration

Create `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# Database
DATABASE_NAME=learnspace
DATABASE_USER=learnspace_user
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=db
DATABASE_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 3. Build and Start Services with Docker

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Check service status
docker compose ps
```

### 4. Initial Setup (First Run)

```bash
# Create superuser (interactive)
docker compose exec web python manage.py createsuperuser

# Or create superuser non-interactive
docker compose exec web python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

### 5. Access the Application

- **Django Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs/

## Service Overview

| Service | Port | Description |
|---------|------|-------------|
| web | 8000 | Django application |
| db | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache & message broker |
| celery | - | Celery worker for async tasks |
| celery-beat | - | Celery beat for periodic tasks |

## Development

### Without Docker (Local Development with Poetry)

#### 1. Install Poetry
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -
# OR
pip install poetry
```

#### 2. Set up the project
```bash
# Clone and navigate to project
git clone <repository-url>
cd LearnSpaceProject

# Install dependencies using Poetry
poetry install

# Activate virtual environment
poetry shell

# Or run commands directly without activating shell
poetry run python manage.py migrate
```

#### 3. Environment setup
```bash
# Copy environment file
cp .env.example .env

# Edit .env file for local development
# Change these settings in .env:
DATABASE_HOST=localhost
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

#### 4. Start external services
```bash
# Start PostgreSQL (requires installed PostgreSQL)
sudo service postgresql start
# OR using Docker for dependencies only:
docker compose up db redis -d

# Start Redis (requires installed Redis)
sudo service redis-server start
```

#### 5. Database setup
```bash
# Run migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Collect static files
poetry run python manage.py collectstatic
```

#### 6. Run development servers
```bash
# Terminal 1 - Django development server
poetry run python manage.py runserver

# Terminal 2 - Celery worker
poetry run celery -A config worker -l info

# Terminal 3 - Celery beat (if using periodic tasks)
poetry run celery -A config beat -l info
```

#### Alternative: Run all in one terminal
```bash
# Run Django server
poetry run python manage.py runserver

# In separate terminals, run:
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
```

### Poetry Useful Commands
```bash
# Add new dependency
poetry add package_name

# Add development dependency
poetry add --group dev package_name

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree

# Run any command in virtual environment
poetry run python manage.py [command]

# Export requirements.txt (if needed)
poetry export -f requirements.txt --output requirements.txt
```

## Useful Commands

### Development with Docker
```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f web
docker compose logs -f celery
docker compose logs -f celery-beat

# Run management commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py shell

# Check service health
docker compose ps
```

### Database Operations
```bash
# Database migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Database shell
docker compose exec db psql -U learnspace_user -d learnspace

# Backup database
docker compose exec db pg_dump -U learnspace_user learnspace > backup.sql
```

### Maintenance
```bash
# Stop all services
docker compose down

# Stop and remove with volumes
docker compose down -v

# Restart specific service
docker compose restart web

# Rebuild and restart
docker compose up -d --build

# View resource usage
docker compose stats
```

## Project Structure

```
LearnSpaceProject/
├── config/                 # Django project settings
├── apps/                   # Django applications
├── static/                 # Static files
├── media/                  # Media files
├── docker-compose.yml      # Docker composition
├── Dockerfile             # Container configuration
├── pyproject.toml         # Poetry configuration
└── .env                   # Environment variables
```

## Environment Variables

See `.env.example` for all available environment variables.

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Or change ports in docker-compose.yml
   ```

2. **Database connection issues**
   ```bash
   # Check if database is running
   docker compose ps db
   # Check database logs
   docker compose logs db
   ```

3. **Migration issues**
   ```bash
   # Reset migrations (development only)
   docker compose down -v
   docker compose up -d
   docker compose exec web python manage.py migrate
   ```

4. **Poetry installation issues**
   ```bash
   # Ensure Python version matches pyproject.toml
   python --version
   # Set Python version for Poetry
   poetry env use python3.12
   ```

### Service Health Checks

All services include health checks. Monitor with:
```bash
docker compose ps
```

## Production Deployment

For production deployment:
1. Set `DEBUG=False`
2. Configure proper `ALLOWED_HOSTS`
3. Set strong `SECRET_KEY`
4. Use production database
5. Configure static files serving
6. Set up SSL certificate

## Support

For issues and questions:
1. Check troubleshooting section above
2. Review service logs: `docker compose logs [service]`
3. Ensure all environment variables are set
4. Verify Docker and Docker Compose versions

---

**Note**: This project uses Docker Compose for container orchestration and Poetry for dependency management. Choose the development approach that best fits your needs.