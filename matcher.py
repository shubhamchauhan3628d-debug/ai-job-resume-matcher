"""
matcher.py — Rule-based resume-to-job skill matching.

Approach:
1. SKILL_SYNONYMS maps common variations/abbreviations to one canonical skill name.
2. extract_skills() scans free-text resume content and returns the set of
   canonical skills found in it.
3. match_resume_to_jobs() compares that set against each job's required_skills
   and scores jobs by percentage overlap, with a human-readable reason.

No external API calls — everything here is deterministic string matching,
so it works identically locally and on Streamlit Cloud with zero setup cost.
"""

import re
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Canonical skill vocabulary + synonyms
# ---------------------------------------------------------------------------
# Keys = variations that might appear in a resume (lowercase).
# Values = the canonical skill name, which MUST match the spelling used in
# jobs.csv's required_skills column, or matching will silently fail.
SKILL_SYNONYMS = {
    # Web
    "js": "javascript", "javascript": "javascript",
    "react": "react", "react.js": "react", "reactjs": "react",
    "react native": "react native", "reactnative": "react native",
    "node": "node.js", "node.js": "node.js", "nodejs": "node.js",
    "express": "express", "express.js": "express",
    "html": "html", "html5": "html",
    "css": "css", "css3": "css",
    "redux": "redux",
    "django": "django",
    "mongodb": "mongodb", "mongo": "mongodb",
    "rest api": "rest api", "rest apis": "rest api", "restful api": "rest api", "api": "rest api",
    "git": "git", "github": "git",
    "responsive design": "responsive design",

    # Data
    "python": "python",
    "pandas": "pandas",
    "sql": "sql", "mysql": "sql", "postgresql": "sql", "postgres": "sql",
    "excel": "excel",
    "data visualization": "data visualization", "data viz": "data visualization",
    "power bi": "power bi", "powerbi": "power bi",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "machine learning": "machine learning", "ml": "machine learning",
    "statistics": "statistics",
    "etl": "etl",
    "airflow": "airflow",
    "cloud": "cloud", "aws": "cloud", "gcp": "cloud", "azure": "cloud",

    # Mobile
    "java": "java",
    "kotlin": "kotlin",
    "android sdk": "android sdk", "android": "android sdk",
    "xml": "xml",
    "swift": "swift",
    "xcode": "xcode",
    "ios sdk": "ios sdk", "ios": "ios sdk",
    "ui design": "ui design",
    "flutter": "flutter",
    "dart": "dart",
    "firebase": "firebase",

    # AI / Automation
    "rpa": "rpa",
    "api integration": "api integration",
    "automation": "automation",
    "nlp": "nlp",
    "transformers": "transformers",
    "pytorch": "pytorch",
    "tensorflow": "tensorflow",
    "deployment": "deployment",
    "opencv": "opencv",
    "deep learning": "deep learning",
    "computer vision": "computer vision",
    "docker": "docker",
    "ci/cd": "ci/cd", "cicd": "ci/cd",
    "llm": "llm", "llms": "llm", "large language model": "llm",
    "prompt engineering": "prompt engineering",
    "streamlit": "streamlit",
}


def extract_skills(resume_text: str) -> set:
    """
    Scan resume_text for any known skill/synonym and return the set of
    canonical skill names found.

    Matching is done on lowercased text using word-boundary-aware search,
    so 'java' won't incorrectly match inside 'javascript'.
    """
    text = resume_text.lower()
    found = set()

    # Sort synonyms longest-first so multi-word terms (e.g. "machine learning")
    # are checked before their shorter substrings could cause confusion.
    for phrase in sorted(SKILL_SYNONYMS.keys(), key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        if re.search(pattern, text):
            found.add(SKILL_SYNONYMS[phrase])

    return found


def _parse_required_skills(skills_str: str) -> set:
    """Turn a 'python, pandas, sql' string into {'python', 'pandas', 'sql'}."""
    return {s.strip().lower() for s in skills_str.split(",") if s.strip()}


def match_resume_to_jobs(resume_skills: set, jobs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Score every job in jobs_df against resume_skills.

    Returns a DataFrame sorted by match_score descending, with columns:
    job_id, title, company, category, match_score (0-100), matched_skills,
    missing_skills, reason.
    """
    rows = []
    for _, job in jobs_df.iterrows():
        required = _parse_required_skills(job["required_skills"])
        matched = required & resume_skills
        missing = required - resume_skills

        score = round(100 * len(matched) / len(required), 1) if required else 0.0

        if matched:
            reason = (
                f"Matched {len(matched)}/{len(required)} required skills: "
                f"{', '.join(sorted(matched))}."
            )
            if missing:
                reason += f" Missing: {', '.join(sorted(missing))}."
        else:
            reason = "No overlapping skills found with your resume."

        rows.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            "category": job["category"],
            "match_score": score,
            "matched_skills": ", ".join(sorted(matched)) if matched else "-",
            "missing_skills": ", ".join(sorted(missing)) if missing else "-",
            "reason": reason,
        })

    result = pd.DataFrame(rows).sort_values(
        by="match_score", ascending=False
    ).reset_index(drop=True)

    return result
