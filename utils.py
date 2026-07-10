import re
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.pdfgen import canvas

# -------------------------------------------------
# Master Skills List
# -------------------------------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "streamlit",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "tableau",
    "git",
    "github",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "bootstrap",
    "docker",
    "aws"
]

# -------------------------------------------------
# Calculate ATS Score
# -------------------------------------------------

def calculate_match_score(job, resume_text):

    documents = [job, resume_text]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf[0:1],
        tfidf[1:2]
    )[0][0]

    job_lower = job.lower()
    resume_lower = resume_text.lower()

    required_skills = []

    matched_skills = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill.lower()) + r"\b",
            job_lower
        ):

            required_skills.append(skill)

            if re.search(
                r"\b" + re.escape(skill.lower()) + r"\b",
                resume_lower
            ):

                matched_skills.append(skill)

    if len(required_skills) == 0:
        skill_score = 1

    else:
        skill_score = len(matched_skills) / len(required_skills)

    final_score = (
        similarity * 0.70 +
        skill_score * 0.30
    ) * 100

    return round(final_score, 2)

# -------------------------------------------------
# Extract Skills
# -------------------------------------------------

def extract_skills(resume_text):

    resume_lower = resume_text.lower()

    found_skills = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill.lower()) + r"\b",
            resume_lower
        ):

            found_skills.append(skill.title())

    return found_skills, SKILLS

# -------------------------------------------------
# Missing Skills
# -------------------------------------------------

def extract_missing_skills(
    job,
    resume_text,
    skills
):

    job_lower = job.lower()

    resume_lower = resume_text.lower()

    missing_skills = []

    for skill in skills:

        if re.search(
            r"\b" + re.escape(skill.lower()) + r"\b",
            job_lower
        ):

            if not re.search(
                r"\b" + re.escape(skill.lower()) + r"\b",
                resume_lower
            ):

                missing_skills.append(skill.title())

    return missing_skills

# -------------------------------------------------
# Candidate Details
# -------------------------------------------------

def extract_candidate_details(resume_text):

    lines = resume_text.split("\n")

    ignore = [
        "resume",
        "education",
        "skills",
        "projects",
        "experience",
        "internship",
        "objective",
        "certifications"
    ]

    name = "Not Found"

    for line in lines:

        line = line.strip()

        if (
            len(line.split()) <= 4
            and line.lower() not in ignore
            and all(
                ch.isalpha() or ch.isspace()
                for ch in line
            )
        ):

            name = line

            break

    email_pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    emails = re.findall(
        email_pattern,
        resume_text
    )

    phone_pattern = (
        r"(?:\+91[- ]?)?"
        r"[6-9]\d{9}"
    )

    phones = re.findall(
        phone_pattern,
        resume_text
    )

    return name, emails, phones
# -------------------------------------------------
# Resume Suggestions
# -------------------------------------------------

def generate_suggestions(resume_text, missing_skills):

    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Add {skill} skill.")

    resume = resume_text.lower()

    if "project" not in resume:
        suggestions.append("Add Projects section with real-world projects.")

    if "internship" not in resume:
        suggestions.append("Mention Internship experience.")

    if "certification" not in resume and "certifications" not in resume:
        suggestions.append("Add Certifications.")

    if "education" not in resume:
        suggestions.append("Add Education details.")

    if "objective" not in resume:
        suggestions.append("Add Career Objective.")

    if "achievement" not in resume:
        suggestions.append("Include Achievements section.")

    if "github" not in resume:
        suggestions.append("Add GitHub profile link.")

    if "linkedin" not in resume:
        suggestions.append("Add LinkedIn profile link.")

    return suggestions


# -------------------------------------------------
# Generate PDF Report
# -------------------------------------------------

def generate_pdf_report(
    name,
    emails,
    phones,
    score,
    found_skills,
    missing_skills,
    suggestions
):

    buffer = io.BytesIO()

    c = canvas.Canvas(buffer)

    c.setTitle("AI Resume Screening Report")

    y = 800

    c.setFont("Helvetica-Bold",18)
    c.drawString(120,y,"AI Resume Screening Report")

    y -= 40

    c.setFont("Helvetica",12)

    c.drawString(50,y,f"Candidate Name : {name}")
    y -= 20

    c.drawString(
        50,
        y,
        f"Email : {emails[0] if emails else 'Not Found'}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Phone : {phones[0] if phones else 'Not Found'}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"ATS Score : {score:.2f}%"
    )

    y -= 35

    c.setFont("Helvetica-Bold",13)
    c.drawString(50,y,"Skills Found")
    y -= 25

    c.setFont("Helvetica",12)

    if found_skills:

        for skill in found_skills:

            if y < 60:
                c.showPage()
                c.setFont("Helvetica",12)
                y = 800

            c.drawString(70,y,"• "+skill)
            y -= 18

    else:

        c.drawString(70,y,"No Skills Found")
        y -= 20

    y -= 10

    c.setFont("Helvetica-Bold",13)
    c.drawString(50,y,"Missing Skills")
    y -= 25

    c.setFont("Helvetica",12)

    if missing_skills:

        for skill in missing_skills:

            if y < 60:
                c.showPage()
                c.setFont("Helvetica",12)
                y = 800

            c.drawString(70,y,"• "+skill)
            y -= 18

    else:

        c.drawString(70,y,"No Missing Skills")
        y -= 20

    y -= 10

    c.setFont("Helvetica-Bold",13)
    c.drawString(50,y,"Suggestions")
    y -= 25

    c.setFont("Helvetica",12)

    if suggestions:

        for suggestion in suggestions:

            if y < 60:
                c.showPage()
                c.setFont("Helvetica",12)
                y = 800

            c.drawString(70,y,"• "+suggestion)
            y -= 18

    else:

        c.drawString(
            70,
            y,
            "Excellent Resume. No Suggestions."
        )

    c.save()

    buffer.seek(0)

    return buffer