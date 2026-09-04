# 🎯 AI Job Scraper & Resume Matcher

An MVP that matches a resume against a set of job postings by skill overlap,
producing a ranked list of jobs with a plain-English reason for each match.

Built as a submission for The Skillians' Generative AI Developer internship
Build Sprint.

## How it works

1. **Skill extraction** — the resume (pasted text or an uploaded `.txt`/`.pdf`)
   is scanned against a curated vocabulary of ~60 tech skills and common
   synonyms/abbreviations (e.g. `JS` → `javascript`, `ML` → `machine learning`),
   so wording differences don't break matching.
2. **Scoring** — each job posting's `required_skills` is compared against the
   extracted resume skills. Score = percentage of a job's required skills the
   resume covers.
3. **Ranking** — jobs are sorted by score, with matched and missing skills
   shown for each, plus a generated reason string.

This is intentionally **rule-based, not a live LLM call** — deterministic,
free to run, and fast, while still doing meaningful work in the skill-extraction
step (normalizing messy resume text into a clean, comparable skill set).

## Tech stack

- **Python + pandas** — data handling and matching logic
- **Streamlit** — UI, deployed on Streamlit Community Cloud
- **pypdf** — text extraction from uploaded PDF resumes

## Project structure

```
job_matcher/
├── app.py              # Streamlit UI
├── matcher.py           # skill extraction + matching/scoring logic
├── build_dataset.py     # generates the sample job postings dataset
├── requirements.txt
├── .streamlit/
│   └── config.toml       # UI theme
└── data/
    └── jobs.csv           # 20 sample job postings
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live demo

[link here after deployment]
