# Project Information

## Tech Stack
- **Backend**: FastAPI, Python 3.10+, sentence-transformers, scikit-learn, PyMongo
- **Frontend**: Vue 3, Vite, Axios, Vue Router
- **Database**: MongoDB (Official Image)
- **Database GUI**: Mongo Express
- **Containerization**: Docker, Docker Compose

## Key Files
- `backend/app/services/nlp.py`: Hybrid semantic matching engine (80% CV-JD + 20% master skills), clustering, similarity scoring
- `backend/app/services/linkedin_scraper.py`: LinkedIn job scraping with embedding generation
- `backend/app/services/parser.py`: CV text extraction and candidate name extraction
- `backend/app/api/endpoints.py`: Main API routes (scrape-recommend, match-detailed, semantic-search)
- `backend/app/api/hr_endpoints.py`: HR routes (rank, cluster)
- `frontend/src/views/`: Vue components for each feature
- `frontend/src/router/index.js`: Route configuration

## API Endpoints
- `POST /api/scrape-recommend`: Scrape LinkedIn + recommend top 5 jobs
- `POST /api/match-detailed`: Hybrid semantic skill matching (matched vs missing)
- `POST /api/jobs/semantic-search`: Vector-based job search
- `POST /api/hr/rank`: Rank multiple CVs against job description
- `POST /api/hr/cluster`: Auto-cluster candidates by skills

## Commands
- `docker compose up --build`: Build and start services
- `docker compose down`: Stop services
- `docker compose exec backend python -m app.services.linkedin_scraper`: Run scraper manually

## Features
1. **Scrape & Find Matches**: Scrape LinkedIn jobs and recommend top 5 matches
2. **Detailed CV-JD Analysis**: Hybrid semantic skill matching (80% CV-JD direct + 20% master skills)
3. **Bulk CV Ranking**: Rank multiple CVs against a job description
4. **Semantic Job Search**: Search jobs using natural language queries
5. **HR Clustering**: Auto-group candidates into talent clusters

## Hybrid Semantic Matching (80/20 Weight)
### Stage 1: CV vs JD Direct (80% weight)
- Extract phrases from CV and JD
- Compute cosine similarity between all CV phrases and JD phrases
- Threshold > 0.75 → matched in CV
- Threshold < 0.75 → missing from CV

### Stage 2: CV vs Master Skills (20% weight)
- Compare CV phrases against 50+ standard IT skills
- If skill found in both CV and JD → matched
- If skill required in JD but missing in CV → missing

### Final Result
- Matched skills: Skills present in CV that JD requires
- Missing skills: Skills required by JD but missing from CV

## Notes
- All skill extraction uses hybrid semantic embeddings
- Job descriptions are embedded and stored in MongoDB for vector search
- K-Means clustering auto-labels clusters based on extracted skills
- Model `all-MiniLM-L6-v2` is pre-downloaded in Docker image
- Mongo Express available at `http://localhost:8081` (admin/password)
