#!/bin/bash

echo "🧪 Running Tests for Store Stock Management API"
echo "=============================================="
echo ""

if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest pytest-cov httpx
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🏃 Running unit tests..."
pytest tests/unit/ -v

echo ""
echo "🏃 Running integration tests..."
pytest tests/integration/ -v

echo ""
echo "📊 Generating coverage report..."
pytest --cov=app --cov-report=term --cov-report=html

echo ""
echo "✅ Tests complete!"
echo ""
echo "📄 Coverage report available at: htmlcov/index.html"
