from fastapi import FastAPI, File, UploadFile, Header
from pydantic import BaseModel
from ats_api.skills import common_skills
from ats_api.analyzer import calculate_ats_score
import fitz

VALID_API_KEYS = [
    "arsh123",
    "premium456"
]

common_skills = [
    "python",
    "java",
    "sql",
    "git",
    "fastapi",
    "machine learning",
    "html",
    "css",
    "javascript",
    "react",
    "mongodb",
    "api",
    "docker",
    "aws"
]

app = FastAPI()

class ResumeRequest(BaseModel):
    resume: str
    job_keyboards: list[str]

@app.post("/analyze")
def analyze_resume(data: ResumeRequest):

    resume_text = data.resume.lower()

    matched_keywords = []

    for keyword in data.job_keywords:

        if keyword.lower() in resume_text:
            matched_keywords.append(keyword)

    keyword_score = int(
        (len(matched_keywords) / len(data.job_keywords)) * 70
    )

    achievement_score = 0

    achievement_words = [
        "improved",
        "increased",
        "developed",
        "managed",
        "led",
        "%"
    ]

    for word in achievement_words:

        if word in resume_text:
            achievement_score += 5

    if achievement_score > 30:
        achievement_score = 30

    final_score = keyword_score + achievement_score

    missing_keywords = [
        keyword
        for keyword in data.job_keywords
        if keyword not in matched_keywords
    ]

    suggestions = []

    if len(missing_keywords) > 0:
        suggestions.append(
            "Add more relevant job keywords"
        )

    if achievement_score < 10:
        suggestions.append(
            "Add measurable achievements"
        )

    if final_score < 60:
        suggestions.append(
            "Improve technical skills section"
        )

    return {
        "score": final_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    pdf = fitz.open(stream=await file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return {
        "filename": file.filename,
        "text": text[:1000]
    }
@app.post("/analyze-resume")
async def analyze_resume_pdf(
    file: UploadFile = File(...),
    job_keywords: str = ""
):

    pdf = fitz.open(
        stream=await file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in pdf:
        resume_text += page.get_text()

    resume_text = resume_text.lower()

    keywords = [
        keyword.strip()
        for keyword in job_keywords.split(",")
    ]

    matched_keywords = []

    for keyword in keywords:

        if keyword.lower() in resume_text:
            matched_keywords.append(keyword)

    keyword_score = int(
        (len(matched_keywords) / len(keywords)) * 70
    ) if len(keywords) > 0 else 0

    achievement_words = [
        "improved",
        "increased",
        "developed",
        "managed",
        "led",
        "%"
    ]

    achievement_score = 0

    for word in achievement_words:

        if word in resume_text:
            achievement_score += 5

    if achievement_score > 30:
        achievement_score = 30

    final_score = keyword_score + achievement_score

    missing_keywords = [
        keyword
        for keyword in keywords
        if keyword not in matched_keywords
    ]

    suggestions = []

    if len(missing_keywords) > 0:
        suggestions.append(
            "Add more relevant job keywords"
        )

    if achievement_score < 10:
        suggestions.append(
            "Add measurable achievements"
        )

    if final_score < 60:
        suggestions.append(
            "Improve technical skills section"
        )

    return {
        "score": final_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }

@app.post("/extract-keywords")
def extract_keywords(job_description: str):

    job_description = job_description.lower()

    found_skills = []

    for skill in common_skills:

        if skill in job_description:
            found_skills.append(skill)

    return {
        "keywords": found_skills
    }

@app.post("/smart-analyze")
async def smart_analyze(
    file: UploadFile = File(...),
    job_description: str = "",
    x_api_key: str = Header(None)
):
    if x_api_key not in VALID_API_KEYS:
        return {
            "error": "Invalid API Key"
    }

    pdf = fitz.open(
        stream=await file.read(),
        filetype="pdf"
    )

    resume_text = ""

    for page in pdf:
        resume_text += page.get_text()

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    extracted_keywords = []

    for skill in common_skills:

        if skill in job_description:
            extracted_keywords.append(skill)

    matched_keywords = []

    for keyword in extracted_keywords:

        if keyword in resume_text:
            matched_keywords.append(keyword)

    keyword_score = int(
        (len(matched_keywords) / len(extracted_keywords)) * 70
    ) if len(extracted_keywords) > 0 else 0

    achievement_words = [
        "improved",
        "increased",
        "developed",
        "managed",
        "led",
        "%"
    ]

    achievement_score = 0

    for word in achievement_words:

        if word in resume_text:
            achievement_score += 5

    if achievement_score > 30:
        achievement_score = 30

    final_score = keyword_score + achievement_score

    missing_keywords = [
        keyword
        for keyword in extracted_keywords
        if keyword not in matched_keywords
    ]

    suggestions = []

    if len(missing_keywords) > 0:
        suggestions.append(
            "Add missing job keywords"
        )

    if achievement_score < 10:
        suggestions.append(
            "Add measurable achievements"
        )

    return {
        "score": final_score,
        "extracted_keywords": extracted_keywords,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }
