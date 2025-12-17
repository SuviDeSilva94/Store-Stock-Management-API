#!/bin/bash

echo "🧪 Running Tests for Store Stock Management API"
echo "=============================================="
echo ""

echo "📦 Checking Docker services..."
if ! docker-compose ps | grep -q "Up"; then
    echo "⚠️  Docker containers are not running!"
    echo "Starting Docker Compose services..."
    docker-compose up -d
    echo "Waiting for services to be ready..."
    sleep 5
fi

echo ""
echo "🏃 Running all tests inside Docker container..."
docker-compose exec api pytest tests/ -v --cov=app --cov-report=term --cov-report=html

echo ""
echo "✅ Tests complete!"
echo ""
echo "📄 Coverage report available at: htmlcov/index.html"
