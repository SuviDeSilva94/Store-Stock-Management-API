#!/bin/bash

echo "🏪 Store Stock Management API"
echo "==============================="
echo ""

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker is installed"
echo ""

echo "🛑 Stopping any existing containers..."
docker-compose down

echo "🚀 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "🏥 Checking API health..."
response=$(curl -s http://localhost:8000/health)

if [ $? -eq 0 ]; then
    echo "✅ API is running!"
    echo ""
    echo "Response: $response"
    echo ""
    echo "📚 API Documentation:"
    echo "   - Swagger UI: http://localhost:8000/docs"
    echo "   - ReDoc:      http://localhost:8000/redoc"
    echo ""
    echo "🔗 API Base URL: http://localhost:8000/api/v1"
    echo ""
    echo "💡 To view logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 To stop:"
    echo "   docker-compose down"
    echo ""
else
    echo "❌ Failed to connect to API. Check logs with:"
    echo "   docker-compose logs"
fi
