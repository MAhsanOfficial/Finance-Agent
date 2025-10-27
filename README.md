# Finance Agent FastAPI Application

A FastAPI application for managing payment data with AI agent integration using OpenAI Agents and Gemini API.

## Features

- 🚀 FastAPI server with automatic API documentation
- 💾 Database integration (PostgreSQL or SQLite)
- 🤖 AI Agent integration with Gemini API
- 📊 Payment data management endpoints
- 🔍 Health check and monitoring endpoints
- 📝 Comprehensive error handling and logging

## Quick Start

### Option 1: Using the startup script (Recommended)

```bash
python start_server.py
```

This script will:
- Create a `.env` file with default SQLite configuration
- Check dependencies
- Start the FastAPI server

### Option 2: Manual setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   # Copy the example and edit as needed
   cp .env.example .env
   ```

3. **Start the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
# For PostgreSQL:
DATABASE_URL=postgresql://username:password@localhost:5432/finance_db

# For SQLite (default):
DATABASE_URL=sqlite:///./finance.db

# Gemini API Configuration (optional for agent functionality)
GEMINI_API_KEY=your_gemini_api_key_here
```

## API Endpoints

- **GET /** - View payment data from mockdata
- **GET /health** - Health check and system status
- **POST /save-to-db/** - Save mockdata to database
- **GET /get-payments/** - Retrieve saved payments from database
- **GET /run-agent/** - Execute the AI agent (requires GEMINI_API_KEY)

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Database Setup

### SQLite (Default)
No additional setup required. The application will create `finance.db` automatically.

### PostgreSQL
1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE finance_db;
   ```
3. Update `DATABASE_URL` in `.env` file
4. Install PostgreSQL driver: `pip install psycopg2-binary`

## AI Agent Setup

The AI agent functionality requires:
1. A valid `GEMINI_API_KEY` in your `.env` file
2. The `openai-agents` package installed

If the agent is not available, the application will still work for basic payment data management.

## Troubleshooting

### Common Issues

1. **"DATABASE_URL not set" error:**
   - The application now defaults to SQLite if no DATABASE_URL is provided
   - Check your `.env` file configuration

2. **"Agent not available" error:**
   - Ensure `GEMINI_API_KEY` is set in `.env`
   - Install the agents package: `pip install openai-agents`

3. **Import errors:**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (requires >= 3.11)

### Logs

The application includes comprehensive logging. Check the console output for detailed error messages and system status.

## Project Structure

```
├── main.py              # FastAPI application and routes
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── mockdata.py          # Sample payment data
├── start_server.py      # Startup script
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Development

To run in development mode with auto-reload:
```bash
uvicorn main:app --reload
```

## License

This project is for educational purposes.
