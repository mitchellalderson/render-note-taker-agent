# Makefile for Render Meeting Notes Agent

.PHONY: help install dev up down logs clean build test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed"

dev: ## Start development servers (without Docker)
	@echo "Starting backend and frontend..."
	@make -j 2 dev-backend dev-frontend

dev-backend: ## Start backend dev server
	cd backend && python app.py

dev-frontend: ## Start frontend dev server
	cd frontend && npm run dev

up: ## Start all services with Docker Compose
	docker-compose up -d
	@echo "✅ All services started"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:3100"

down: ## Stop all Docker services
	docker-compose down
	@echo "✅ All services stopped"

logs: ## View Docker logs
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

build: ## Build all Docker images
	docker-compose build

rebuild: ## Rebuild all Docker images (no cache)
	docker-compose build --no-cache

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart backend service
	docker-compose restart backend

restart-frontend: ## Restart frontend service
	docker-compose restart frontend

clean: ## Clean all build artifacts and dependencies
	@echo "Cleaning..."
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf backend/uploads/*
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf frontend/out
	docker-compose down -v
	@echo "✅ Cleaned"

lint: ## Run linters
	@echo "Linting frontend..."
	cd frontend && npm run lint

test: ## Run tests
	@echo "Running backend chunking tests..."
	cd backend && python test_chunking.py

setup: install up ## Complete setup (install dependencies and start services)
	@echo "✅ Setup complete!"
	@echo "Visit http://localhost:3000 to get started"
	@echo ""
	@echo "⚠️  Don't forget to:"
	@echo "  1. Create a .env file in the root directory (copy from env.template)"
	@echo "  2. Add your ASSEMBLYAI_API_KEY"
	@echo "  3. Add your OPENAI_API_KEY"

ps: ## Show running containers
	docker-compose ps

stop: ## Alias for down
	@make down

start: ## Alias for up
	@make up

env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		cp env.template .env; \
		echo "✅ Created .env file from template"; \
		echo "⚠️  Please edit .env and add your API keys"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi


