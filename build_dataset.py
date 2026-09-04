import pandas as pd

jobs = [
    {
        "job_id": 1,
        "title": "Frontend Developer",
        "company": "TechWave Solutions",
        "category": "Web Development",
        "required_skills": "javascript, react, html, css, git",
        "description": "Build responsive user interfaces for our SaaS dashboard product. Work closely with designers to implement pixel-perfect, accessible UI components."
    },
    {
        "job_id": 2,
        "title": "Backend Developer (Node.js)",
        "company": "Bright Apps Inc",
        "category": "Web Development",
        "required_skills": "javascript, node.js, express, mongodb, rest api",
        "description": "Design and maintain REST APIs powering our mobile and web clients. Own database schema design and API performance."
    },
    {
        "job_id": 3,
        "title": "Full Stack Developer",
        "company": "Nimbus Softworks",
        "category": "Web Development",
        "required_skills": "javascript, react, node.js, sql, html, css",
        "description": "Ship end-to-end features across our React frontend and Node backend for a fast-growing fintech product."
    },
    {
        "job_id": 4,
        "title": "Junior Web Developer",
        "company": "StartUp Hub",
        "category": "Web Development",
        "required_skills": "html, css, javascript, git, responsive design",
        "description": "Entry-level role building marketing pages and small web apps for early-stage startup clients."
    },
    {
        "job_id": 5,
        "title": "Backend Developer (Python/Django)",
        "company": "CoreStack Technologies",
        "category": "Web Development",
        "required_skills": "python, django, sql, rest api, git",
        "description": "Maintain and extend a Django monolith serving a B2B logistics platform. Focus on API reliability and data integrity."
    },
    {
        "job_id": 6,
        "title": "Data Analyst",
        "company": "InsightMetrics",
        "category": "Data Science",
        "required_skills": "python, pandas, sql, excel, data visualization",
        "description": "Turn raw operational data into dashboards and reports that drive weekly business decisions for stakeholders."
    },
    {
        "job_id": 7,
        "title": "Data Scientist",
        "company": "QuantEdge Analytics",
        "category": "Data Science",
        "required_skills": "python, pandas, scikit-learn, machine learning, statistics",
        "description": "Build predictive models for customer churn and pricing optimization using structured transactional data."
    },
    {
        "job_id": 8,
        "title": "Business Intelligence Analyst",
        "company": "Clarity Consulting",
        "category": "Data Science",
        "required_skills": "sql, power bi, excel, data visualization, python",
        "description": "Design BI dashboards and automate recurring reporting for enterprise clients across retail and healthcare."
    },
    {
        "job_id": 9,
        "title": "Data Engineer",
        "company": "Pipeline Systems",
        "category": "Data Science",
        "required_skills": "python, sql, etl, airflow, cloud",
        "description": "Build and maintain ETL pipelines feeding our analytics warehouse. Experience with orchestration tools is a plus."
    },
    {
        "job_id": 10,
        "title": "Android Developer",
        "company": "Mobify Labs",
        "category": "Mobile Development",
        "required_skills": "java, kotlin, android sdk, xml, git",
        "description": "Develop and maintain native Android features for a consumer productivity app with 500k+ installs."
    },
    {
        "job_id": 11,
        "title": "iOS Developer",
        "company": "Appventure Studio",
        "category": "Mobile Development",
        "required_skills": "swift, xcode, ios sdk, git, ui design",
        "description": "Build polished native iOS experiences for a health-and-fitness app, working closely with product design."
    },
    {
        "job_id": 12,
        "title": "Cross-Platform Mobile Developer",
        "company": "Flutterly Apps",
        "category": "Mobile Development",
        "required_skills": "flutter, dart, firebase, git, rest api",
        "description": "Own features across our single Flutter codebase shipping to both iOS and Android for a social app."
    },
    {
        "job_id": 13,
        "title": "React Native Developer",
        "company": "Hybridtech",
        "category": "Mobile Development",
        "required_skills": "javascript, react native, redux, rest api, git",
        "description": "Build cross-platform mobile features for an e-commerce client using React Native and Redux."
    },
    {
        "job_id": 14,
        "title": "AI/Automation Engineer",
        "company": "AutomateNow Inc",
        "category": "AI & Automation",
        "required_skills": "python, rpa, api integration, automation, sql",
        "description": "Automate repetitive business workflows using RPA tools and Python scripts integrated with internal APIs."
    },
    {
        "job_id": 15,
        "title": "NLP Engineer",
        "company": "LinguaTech AI",
        "category": "AI & Automation",
        "required_skills": "python, nlp, transformers, machine learning, pytorch",
        "description": "Develop text classification and sentiment models for a customer feedback analytics product."
    },
    {
        "job_id": 16,
        "title": "Machine Learning Engineer",
        "company": "NeuralWorks AI",
        "category": "AI & Automation",
        "required_skills": "python, tensorflow, pytorch, machine learning, deployment",
        "description": "Take ML models from notebook to production, including deployment and monitoring pipelines."
    },
    {
        "job_id": 17,
        "title": "Computer Vision Engineer",
        "company": "VisionaryAI",
        "category": "AI & Automation",
        "required_skills": "python, opencv, deep learning, pytorch, computer vision",
        "description": "Build image classification and object detection models for a manufacturing quality-inspection product."
    },
    {
        "job_id": 18,
        "title": "DevOps/Automation Engineer",
        "company": "CloudOps Inc",
        "category": "AI & Automation",
        "required_skills": "python, docker, ci/cd, aws, automation",
        "description": "Automate deployment pipelines and infrastructure provisioning for a growing SaaS engineering team."
    },
    {
        "job_id": 19,
        "title": "AI Product Intern (Generative AI)",
        "company": "The Skillians",
        "category": "AI & Automation",
        "required_skills": "python, llm, prompt engineering, api integration, streamlit",
        "description": "Prototype and ship generative AI features end-to-end, from data pipeline to a deployed Streamlit demo."
    },
    {
        "job_id": 20,
        "title": "Python Automation Developer",
        "company": "Workflowly Tech",
        "category": "AI & Automation",
        "required_skills": "python, pandas, automation, api integration, sql",
        "description": "Build internal tools that automate data cleaning and reporting workflows across the ops team."
    },
]

df = pd.DataFrame(jobs)
df.to_csv("/home/claude/job_matcher/data/jobs.csv", index=False)
print(df.shape)
print(df.head())
