# Library Management System

## Overview

This is a Flask-based Library Management System that provides a comprehensive platform for managing books, users, and loan transactions. The system supports two user roles: students who can search and borrow books, and administrators who can manage the entire library catalog and oversee all loan operations.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Replit Auth integration with Flask-Dance OAuth
- **Session Management**: Flask-Login for user session handling
- **Deployment**: Gunicorn WSGI server with autoscale deployment

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **CSS Framework**: Bootstrap 5 with Replit dark theme
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript with Bootstrap components

### Database Schema
- **Users Table**: Stores user information with role-based access (student/admin)
- **OAuth Table**: Manages OAuth tokens for Replit authentication
- **Books Table**: Catalog management (title, author, ISBN, availability)
- **Loans Table**: Tracks borrowing transactions and due dates

## Key Components

### Authentication System
- Replit Auth integration for seamless user login
- Role-based access control (student vs admin permissions)
- OAuth token storage with browser session management
- Automatic user creation on first login

### Book Management
- Complete CRUD operations for library catalog
- Search functionality by title, author, ISBN, and category
- Availability tracking and inventory management
- Admin-only book creation and editing capabilities

### Loan Management
- Student loan requests and tracking
- Due date calculation and overdue detection
- Admin oversight of all library transactions
- Return processing and status updates

### User Interface
- Responsive design with Bootstrap framework
- Role-specific dashboards and navigation
- Dark theme optimized for Replit environment
- Intuitive search and filtering interfaces

## Data Flow

1. **User Authentication**: Users authenticate via Replit Auth, creating or retrieving user records
2. **Role-Based Routing**: System redirects users to appropriate dashboards based on their role
3. **Book Discovery**: Students search and browse the catalog, while admins manage inventory
4. **Loan Processing**: Students request loans, admins approve/manage, system tracks due dates
5. **Return Management**: Loan status updates flow through the system to maintain accurate availability

## External Dependencies

### Core Dependencies
- **Flask**: Web application framework and routing
- **SQLAlchemy**: Database ORM and migration management
- **Flask-Dance**: OAuth integration specifically for Replit Auth
- **Flask-Login**: User session and authentication state management
- **Psycopg2**: PostgreSQL database adapter
- **Gunicorn**: Production WSGI server

### Frontend Dependencies
- **Bootstrap 5**: UI components and responsive grid system
- **Font Awesome**: Icon library for enhanced user interface
- **Replit Bootstrap Theme**: Dark theme optimization for Replit environment

## Deployment Strategy

### Environment Configuration
- PostgreSQL database via environment variable `DATABASE_URL`
- Session security via `SESSION_SECRET` environment variable
- Replit-native deployment with autoscale capabilities

### Production Setup
- Gunicorn serves the application on port 5000
- ProxyFix middleware handles reverse proxy headers
- Database connection pooling with health checks
- Automatic table creation on application startup

### Development Workflow
- Hot reload enabled for development iterations
- Debug logging configured for troubleshooting
- Separate development and production configurations

## Changelog

Changelog:
- June 25, 2025. Fixed database connection issues, switched to SQLite for reliability, added sample users and books
- June 16, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.