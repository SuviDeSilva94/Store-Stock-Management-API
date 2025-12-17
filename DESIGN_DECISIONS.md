# Design Decisions

## Technology Stack

Python + FastAPI - Modern, fast, auto-generates API docs, great for building REST APIs.

PostgreSQL - Reliable database with strong ACID transaction support, perfect for managing inventory.

SQLAlchemy ORM - Provides database abstraction and makes it easy to work with Python objects.

Docker - Containerization for consistent deployment across environments.

## Architecture

Clean 3-Tier Architecture:
- API Layer - Handles HTTP requests and responses
- Domain Layer - Contains business logic and models
- Infrastructure Layer - Database access and external services

SOLID Principles applied throughout the codebase.

## Design Patterns

- Repository Pattern - Separates data access from business logic
- Dependency Injection - Uses FastAPI's Depends() for loose coupling
- Factory Pattern - Manages object creation in dependency factories

## Security

JWT Authentication - Stateless token-based auth for scalability.

bcrypt Password Hashing - Secure one-way encryption.

## Testing

57 Total Tests:
- 33 Unit Tests - Test components in isolation with mocks
- 24 Integration Tests - Test end-to-end API flows with real database

## Database

Transaction Management - All operations are atomic and can rollback on errors.

Product Model - id, name, sku (unique), stock, created_at, updated_at

## Implementation Summary

- Clean architecture and SOLID principles
- Comprehensive testing
- JWT authentication
- Docker setup
- Database transactions


