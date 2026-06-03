# CV Summarizer & Job Matching System

A web-based application for CV Summarization, Job Matching, and Talent Analytics using Natural Language Processing (NLP).

## Features

- **Job Seeker Portal**:
  - **Scrape Jobs**: Pull real-time jobs from LinkedIn using keywords and locations.
  - **CV-JD Analysis**: Detailed analysis using hybrid semantic matching (80% CV-JD direct match + 20% Master Skills) to find similarity scores, matched skills, and missing skills.
  - **Semantic Search**: Upload CV and search for the most relevant jobs stored in MongoDB using vector embeddings.
- **HR Panel**:
  - **Bulk CV Ranking**: Upload multiple CVs to rank candidates against a target job description.
  - **Talent Clustering**: Group candidates into dynamically labeled clusters using K-Means clustering of CV embeddings.

## Architecture

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Vue.js (Vue 3 with Vite & Vue Router)
- **Database**: MongoDB (Storage for scraped jobs and embeddings)
- **Database GUI**: Mongo Express
- **NLP Engine**: `sentence-transformers` (configurable, default: `paraphrase-multilingual-MiniLM-L12-v2`)
- **Containerization**: Docker & Docker Compose

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints.py       # Core APIs (scrape, match, search)
│   │   │   ├── hr_endpoints.py    # HR APIs (rank, cluster)
│   │   │   └── jobs_endpoints.py  # Jobs operations
│   │   ├── core/
│   │   │   └── mongodb.py         # MongoDB connection helper
│   │   ├── services/
│   │   │   ├── linkedin_scraper.py# BeautifulSoup job scraper
│   │   │   ├── nlp.py             # NLP match, search, clustering logic
│   │   │   └── parser.py          # PDF/DOCX parsing & cleaning logic
│   │   └── main.py                # FastAPI app entrypoint
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── views/                 # View pages (Analyze, Cluster, Scrape, etc.)
│   │   ├── router/                # Vue Router configuration
│   │   ├── App.vue                # Root App component
│   │   └── main.js                # App entrypoint
│   ├── Dockerfile
│   └── package.json
├── .env.example                   # Env template
└── docker-compose.yml             # Orchestration file
```

## Installation & Setup

Follow these steps to run the project on a new device:

### Prerequisites

Make sure you have the following installed on your machine:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd caps-final
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure your credentials and preference:
   ```env
   MONGO_ROOT_USER=admin
   MONGO_ROOT_PASSWORD=password
   MONGO_EXPRESS_USER=admin
   MONGO_EXPRESS_PASSWORD=password
   MODEL_MAIN=paraphrase-multilingual-MiniLM-L12-v2
   ```

### Step 3: Start the Application

Build and run all services in the background using Docker Compose:

```bash
docker compose up --build
```

*(Note: The first run might take a few minutes as it downloads the model cache and builds images.)*

## Service Access URLs

Once Docker Compose is running, access the services using the following URLs:

- **Frontend Interface**: http://localhost:5173
- **Backend API Docs (Swagger)**: http://localhost:8000/docs
- **Mongo Express (Database Web UI)**: http://localhost:8081

## API Documentation

### Core Endpoints

- **POST `/api/scrape-recommend`**: Trigger scraping LinkedIn jobs and saving them in MongoDB.
- **POST `/api/match-detailed`**: Direct semantic match of CV and Job Description.
- **POST `/api/jobs/semantic-search`**: Compare uploaded CV against all scraped jobs using vector similarity.
- **POST `/api/hr/rank`**: Rank bulk CV uploads against a job description.
- **POST `/api/hr/cluster`**: Perform cluster analysis on candidate CVs.
- **GET `/api/jobs`**: Fetch jobs stored in MongoDB.
- **DELETE `/api/jobs/clear`**: Clear all jobs from MongoDB.
