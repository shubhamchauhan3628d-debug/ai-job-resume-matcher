"""
app.py — Streamlit UI for the AI Job Scraper & Resume Matcher MVP.

Flow:
1. User pastes resume text and/or uploads a .txt / .pdf resume.
2. We extract plain text from whichever source is provided.
3. matcher.extract_skills() pulls a canonical skill set out of that text.
4. matcher.match_resume_to_jobs() scores every job posting and ranks them.
5. Results are shown as ranked cards with a score, matched skills, and reason.

No live API calls anywhere — everything is local, deterministic, and free
to run on Streamlit Community Cloud.
"""

import streamlit as st
import pandas as pd
from pypdf import PdfReader

from matcher import extract_skills, match_resume_to_jobs

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Job Matcher", page_icon="🎯", layout="centered")

st.title("🎯 AI Job Scraper & Resume Matcher")
st.write(
    "Paste your resume (or upload a file), and this tool ranks a set of "
    "sample job postings by how well your skills overlap with each one — "
    "with a plain-English reason for every match."
)


# ---------------------------------------------------------------------------
# Load job postings (cached so it only reads the CSV once per session)
# ---------------------------------------------------------------------------
@st.cache_data
def load_jobs():
    return pd.read_csv("data/jobs.csv")


jobs_df = load_jobs()


# ---------------------------------------------------------------------------
# Small display helpers
# ---------------------------------------------------------------------------
def skill_badges(skills_str: str, color: str) -> str:
    """Render a comma-separated skill string as small colored HTML chips."""
    if skills_str == "-" or not skills_str:
        return "<em>none</em>"
    chips = ""
    for skill in [s.strip() for s in skills_str.split(",")]:
        chips += (
            f"<span style='background-color:{color};color:white;"
            f"padding:2px 8px;border-radius:10px;font-size:0.8em;"
            f"margin:2px;display:inline-block;'>{skill}</span>"
        )
    return chips


def score_color(score: float) -> str:
    """Green for strong matches, amber for medium, red for weak."""
    if score >= 70:
        return "#2ECC71"
    elif score >= 40:
        return "#F1C40F"
    else:
        return "#E74C3C"


# ---------------------------------------------------------------------------
# Sidebar — context about the app + dataset
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. We scan your resume text for known skills/technologies "
        "(handling common variations, e.g. `JS` → `javascript`).\n"
        "2. Each job posting is scored by the **percentage of its required "
        "skills** your resume covers.\n"
        "3. Jobs are ranked highest match first, with matched and missing "
        "skills shown for each.\n\n"
        "Everything runs locally with rule-based matching — no external AI "
        "API calls at runtime."
    )
    st.divider()
    st.metric("Sample job postings", len(jobs_df))
    st.caption("Categories: " + ", ".join(sorted(jobs_df["category"].unique())))


def extract_text_from_pdf(uploaded_file) -> str:
    """Pull all text out of an uploaded PDF resume."""
    reader = PdfReader(uploaded_file)
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts)


# ---------------------------------------------------------------------------
# Resume input
# ---------------------------------------------------------------------------
st.subheader("1. Your resume")

pasted_text = st.text_area(
    "Paste your resume text here",
    height=200,
    placeholder="e.g. Computer Engineering student experienced in Python, "
                "pandas, SQL, machine learning ...",
)

uploaded_file = st.file_uploader(
    "...or upload a .txt or .pdf resume (optional — overrides pasted text if both are given)",
    type=["txt", "pdf"],
)

resume_text = pasted_text

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:  # .txt
        resume_text = uploaded_file.read().decode("utf-8", errors="ignore")

    with st.expander("Preview extracted text from uploaded file"):
        st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))


# ---------------------------------------------------------------------------
# Run matching
# ---------------------------------------------------------------------------
st.subheader("2. Find matches")

if st.button("🔍 Find Matches", type="primary"):
    if not resume_text or not resume_text.strip():
        st.warning("Please paste your resume text or upload a file first.")
    else:
        resume_skills = extract_skills(resume_text)

        if not resume_skills:
            st.warning(
                "No recognizable skills were found in your resume. "
                "Try including specific tools/technologies by name "
                "(e.g. Python, SQL, React)."
            )
        else:
            st.success(f"Detected {len(resume_skills)} skills: " + ", ".join(sorted(resume_skills)))

            results = match_resume_to_jobs(resume_skills, jobs_df)

            st.subheader("3. Ranked matches")

            # --- Filters ---
            filt_col1, filt_col2 = st.columns([2, 1])
            with filt_col1:
                categories = ["All categories"] + sorted(jobs_df["category"].unique())
                selected_category = st.selectbox("Filter by category", categories)
            with filt_col2:
                min_score = st.slider("Minimum match %", 0, 100, 0, step=10)

            filtered = results[results["match_score"] >= min_score]
            if selected_category != "All categories":
                filtered = filtered[filtered["category"] == selected_category]
            top_results = filtered.head(10)

            if top_results.empty:
                st.info("No jobs match the current filters. Try lowering the minimum score.")
            else:
                for _, row in top_results.iterrows():
                    color = score_color(row["match_score"])
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"### {row['title']}")
                            st.caption(f"{row['company']} · {row['category']}")
                        with col2:
                            st.markdown(
                                f"<h2 style='color:{color};text-align:right;margin:0;'>"
                                f"{row['match_score']:.0f}%</h2>",
                                unsafe_allow_html=True,
                            )

                        st.progress(min(int(row["match_score"]), 100))

                        st.markdown(
                            f"**Matched:** {skill_badges(row['matched_skills'], '#2ECC71')}",
                            unsafe_allow_html=True,
                        )
                        if row["missing_skills"] != "-":
                            st.markdown(
                                f"**Missing:** {skill_badges(row['missing_skills'], '#7F8C8D')}",
                                unsafe_allow_html=True,
                            )

st.divider()
st.caption(
    "Matching is rule-based: it extracts known skills/technologies from your "
    "resume text and scores jobs by percentage skill overlap. No external "
    "AI API calls are made at runtime."
)
