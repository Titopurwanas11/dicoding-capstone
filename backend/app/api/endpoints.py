from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser import extract_text, clean_text
from app.services.nlp import get_similarity_score, match_cv_jd_hybrid, model
from app.services.linkedin_scraper import scrape_linkedin_jobs
from app.core.mongodb import get_jobs_collection
from sentence_transformers import util
import torch

router = APIRouter()

@router.post("/scrape-recommend")
async def scrape_and_recommend(
    time_range: str = Form("1w"),
    keyword: str = Form("Python Developer"),
    location: str = Form("Jakarta")
):
    # Step 1: Scrape jobs (generates descriptions & embeddings in DB)
    scraped_count = scrape_linkedin_jobs(keyword, location, time_range)
    
    # Step 2: Get jobs from MongoDB
    jobs_collection = get_jobs_collection()
    jobs = list(jobs_collection.find({"keyword_searched": keyword, "location": location}).sort("scraped_at", -1).limit(20))
    
    job_results = []
    for job in jobs:
        job_results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "url": job["url"]
        })
    
    return {
        "scraped_count": scraped_count,
        "recommendations": job_results
    }

@router.post("/match-detailed")
async def match_cv_to_job_detailed(
    cv: UploadFile = File(...),
    job_description: str = Form(...),
    domain: str = Form(...)
):
    file_bytes = await cv.read()
    cv_text = extract_text(file_bytes, cv.filename)
    
    # Bersihkan job_description juga (hapus HTML, URL, noise)
    jd_clean = clean_text(job_description)

    similarity_score = get_similarity_score(cv_text, jd_clean)
    
    # Hybrid semantic matching
    matched_skills, missing_skills = match_cv_jd_hybrid(cv_text, jd_clean, domain)
    
    return {
        "similarity_score": similarity_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "domain": domain
    }

@router.post("/jobs/semantic-search")
async def semantic_job_search(
    cv: UploadFile = File(...)
):
    # Extract text from uploaded CV (extract_text already applies clean_text)
    file_bytes = await cv.read()
    cv_text = extract_text(file_bytes, cv.filename)
    
    # Encode the CV text as the semantic query
    query_emb = model.encode(cv_text, convert_to_tensor=True)
    
    jobs_collection = get_jobs_collection()
    jobs = list(jobs_collection.find({"description_embedding": {"$exists": True}}))
    
    if not jobs:
        return []
    
    # Batch compute similarities using util.cos_sim for stability
    desc_embs = torch.tensor([job["description_embedding"] for job in jobs])
    similarities = util.cos_sim(query_emb, desc_embs)[0]
    
    results = []
    for i, job in enumerate(jobs):
        score = round(max(0.0, min(1.0, float(similarities[i]))) * 100, 2)
        
        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "url": job["url"],
            "score": score
        })
        
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]
