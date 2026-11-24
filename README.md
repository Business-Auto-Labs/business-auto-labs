# Business Automation Labs CRM

A multi-niche, multi-country lead-generation CRM designed to discover, qualify, organise and manage potential business clients.

## Technology Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL / Supabase (planned)
- **Background Processing**: Redis and Celery (planned)

## Project Structure

```
Business-Auto-Labs-CRM/
├── frontend/           # Next.js + TypeScript frontend
│   ├── pages/          # Next.js routes
│   ├── components/     # Reusable UI components
│   ├── styles/         # Tailwind CSS configuration
│   ├── public/         # Static assets
│   ├── next.config.js  # Next.js configuration
│   └── tailwind.config.js # Tailwind CSS configuration
├── backend/            # FastAPI backend
│   ├── main.py         # FastAPI application entry point
│   ├── requirements.txt # Python dependencies
│   └── .env.example    # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Prerequisites

- Node.js >= 18.x
- Python >= 3.11
- npm or yarn
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Business-Auto-Labs-CRM
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Install Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```
# Backend API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### 5. Start the Development Servers

#### Frontend (Next.js)

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

#### Backend (FastAPI)

```bash
cd backend
python main.py
```

The backend API will be available at `http://localhost:8000`.

### 6. Verify the Health Check

Visit `http://localhost:8000/health` to confirm the backend is running:

```json
{
  "status": "healthy",
  "service": "backend"
}
```

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with welcome message |
| `/health` | GET | Health check endpoint |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## Development

### Frontend

- Run `npm run dev` to start the Next.js development server
- Run `npm run build` to build for production
- Run `npm run lint` to lint the codebase

### Backend

- Run `python main.py` to start the FastAPI development server
- Access the interactive API docs at `http://localhost:8000/docs`

## Next Steps (Phase 2)

- Configure PostgreSQL / Supabase database connection
- Implement user authentication
- Add lead discovery and qualification logic
- Implement email verification
- Build CRM pipeline management UI

## License

This project is proprietary software for Business Automation Labs.