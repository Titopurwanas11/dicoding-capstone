# Code Flow Documentation

## Overview

```
USER (Browser)
    │
    ▼
frontend/src/App.vue          ← Vue 3 SPA (port 5173) with Vue Router
    │
    │ HTTP POST multipart/form-data / JSON
    ▼
backend/app/main.py           ← FastAPI entrypoint (port 8000)
    │
    ├──► backend/app/api/endpoints.py  ← General API routes
    ├──► backend/app/api/hr_endpoints.py ← HR API routes
    │
    ├──► backend/app/services/parser.py   ← Text extraction
    └──► backend/app/services/nlp.py      ← Hybrid semantic matching (80/20), clustering
              │
              └──► MongoDB (cv_matcher.linkedin_jobs) ← Data source with stored vectors
```

---

## 1. Hybrid Semantic Matching Flow (80/20 Weight)

```
[Match Detailed: CV-JD Analysis]
  │
  ├──► extract_text(cv_file) → cv_text
  ├──► extract_phrases(cv_text) → cv_phrases
  ├──► extract_phrases(jd_text) → jd_phrases
  │
  ├──► Stage 1: CV vs JD Direct Matching (80% weight)
  │      ├── Compute cosine similarity between cv_phrases × jd_phrases
  │      ├── If similarity > 0.75 → matched (weight 80%)
  │      └── If similarity < 0.75 → missing (weight 80%)
  │
  ├──► Stage 2: CV vs Master Skills (20% weight)
  │      ├── Compare cv_phrases against 50+ standard skills
  │      ├── If skill found in both CV and JD → matched (weight 20%)
  │      └── If skill required in JD but missing in CV → missing (weight 20%)
  │
  ├──► Combine weighted scores
  │      ├── matched_skills: Top 15 by combined score
  │      └── missing_skills: Top 15 by combined score
  │
  └──► Return similarity score, matched skills, and missing skills
```

---

## 2. Scrape & Recommend Flow (Job Seeker)

```
[Scrape & Find Matches]
  │
  ├──► scrape_linkedin_jobs(keyword, location, time_range)
  │      ├── Fetch jobs from LinkedIn guest API
  │      ├── Fetch full job description
  │      ├── Generate 'description_embedding' via sentence-transformers
  │      └── Save jobs into MongoDB
  │
  ├──► extract_text(cv_file) → cv_text
  ├──► model.encode(cv_text) → cv_emb
  ├──► Load jobs from MongoDB matching keyword/location
  │      ├── Compute cosine similarity: np.dot(cv_emb, job_emb)
  │      └── Sort jobs by highest similarity
  │
  └──► Return Top 5 job recommendations
```

---

## 3. Bulk CV Ranking Flow (HR)

```
[Bulk CV Ranking]
  │
  └──► Loop through each uploaded CV:
         ├── extract_text(cv) → cv_text
         ├── extract_candidate_name(cv_text) → candidate_name
         ├── get_similarity_score(cv_text, job_description) → score
         └── Append to rankings list
  │
  ├──► Sort candidates by highest score
  └──► Return ranked candidates list
```

---

## 4. Candidate Clustering Flow (HR)

```
[Candidate Clustering]
  │
  ├──► Extract texts from all uploaded CVs
  ├──► cluster_documents(texts, filenames, num_clusters)
  │      ├── model.encode(texts) → document embeddings
  │      ├── Run K-Means clustering (sklearn)
  │      ├── For each cluster, extract phrases and match against master skills
  │      └── Suggest cluster label: "Skill A / Skill B / Skill C"
  │
  └──► Return list of clusters with candidates and suggested labels
```

---

## 5. Semantic Job Search Flow

```
[Semantic Job Search]
  │
  ├──► model.encode(query) → query_emb
  ├──► Load all jobs with description embeddings from MongoDB
  ├──► Compute cosine similarity: np.dot(query_emb, job_emb)
  ├──► Sort jobs by highest similarity
  └──► Return Top 5 jobs matching query
```

---

## 6. Hybrid Matching Detailed Breakdown

### Stage 1: CV vs JD Direct (80% weight)
```python
for jd_phrase in jd_phrases:
    cv_similarities = cosine(jd_phrase, all_cv_phrases)
    if max_similarity > 0.75:
        matched[jd_phrase] = similarity * 0.80
    else:
        missing[jd_phrase] = similarity * 0.80
```

### Stage 2: CV vs Master Skills (20% weight)
```python
for skill in STANDARD_SKILLS:
    cv_sim = cosine(skill, cv_phrases)
    jd_sim = cosine(skill, jd_phrases)
    
    if cv_sim > 0.82 and jd_sim > 0.82:
        matched[skill] = min(cv_sim, jd_sim) * 0.20
    elif jd_sim > 0.82 and cv_sim <= 0.82:
        missing[skill] = jd_sim * 0.20
```

### Final Ranking
- Sort matched skills by combined weighted score
- Sort missing skills by combined weighted score
- Return top 15 of each
