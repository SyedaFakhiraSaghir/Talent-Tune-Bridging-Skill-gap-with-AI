from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import math

app = FastAPI()

# Mock database
SKILL_DB = {
    "data scientist": ["python", "machine learning", "sql", "statistics"],
    "web developer": ["javascript", "html", "css", "react"],
    "devops engineer": ["docker", "kubernetes", "aws", "linux"]
}

COURSE_DB = [
    {"name": "Python Crash Course", "skills": ["python"], "url": "https://example.com/python"},
    {"name": "ML Fundamentals", "skills": ["machine learning"], "url": "https://example.com/ml"},
    {"name": "SQL Masterclass", "skills": ["sql"], "url": "https://example.com/sql"},
    {"name": "JavaScript Bootcamp", "skills": ["javascript"], "url": "https://example.com/js"}
]

class AnalysisRequest(BaseModel):
    resume_text: str
    target_job: str

@app.post("/analyze")
async def analyze_skills(request: AnalysisRequest):
    target_skills = SKILL_DB.get(request.target_job.lower(), [])
    
    if not target_skills:
        return {"error": "Job not found"}
    
    current_skills = [skill for skill in SKILL_DB.values() 
                     for skill in skill if skill in request.resume_text.lower()]
    
    gap_score = len(set(current_skills) & set(target_skills)) / len(set(target_skills))
    
    missing_skills = set(target_skills) - set(current_skills)
    recommended = [
        course for course in COURSE_DB
        if any(skill in missing_skills for skill in course["skills"])
    ][:3]
    
    return {
        "current_skills": list(set(current_skills)),
        "required_skills": target_skills,
        "missing_skills": list(missing_skills),
        "gap_score": round(gap_score, 2),
        "recommended_courses": recommended
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)