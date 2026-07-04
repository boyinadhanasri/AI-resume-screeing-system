import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.pdfgen import canvas
import io


# -------------------------------
# Calculate ATS Score
# -------------------------------
def calculate_match_score(job, resume_text):

    documents = [job, resume_text]

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(documents)

    score = cosine_similarity(
        tfidf[0:1],
        tfidf[1:2]
    )[0][0] * 100

    return score


# -------------------------------
# Extract Skills
# -------------------------------
def extract_skills(resume_text):

    skills = [
        "python","java","c","c++","sql","html","css",
        "javascript","react","node","streamlit",
        "machine learning","deep learning","tensorflow",
        "pandas","numpy","excel","power bi",
        "tableau","git","github","mysql",
        "mongodb","flask","django","bootstrap",
        "docker","aws"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill.title())

    return found_skills, skills


# -------------------------------
# Missing Skills
# -------------------------------
def extract_missing_skills(job, resume_text, skills):

    missing_skills = []

    for skill in skills:
        if skill.lower() in job.lower() and skill.lower() not in resume_text.lower():
            missing_skills.append(skill.title())

    return missing_skills


# -------------------------------
# Candidate Details
# -------------------------------
def extract_candidate_details(resume_text):

    lines = resume_text.split("\n")

    name = "Not Found"

    for line in lines:
        line = line.strip()

        if len(line) > 2 and all(ch.isalpha() or ch.isspace() for ch in line):
            name = line
            break

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.findall(email_pattern, resume_text)

    phone_pattern = r"(?:\+91[- ]?)?[6-9]\d{9}"
    phones = re.findall(phone_pattern, resume_text)

    return name, emails, phones


# -------------------------------
# Resume Suggestions
# -------------------------------
def generate_suggestions(resume_text, missing_skills):

    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Add {skill} skill.")

    if "project" not in resume_text.lower():
        suggestions.append("Add Projects section.")

    if "internship" not in resume_text.lower():
        suggestions.append("Mention Internship experience.")

    if "certification" not in resume_text.lower() and "certifications" not in resume_text.lower():
        suggestions.append("Add Certifications.")

    if "education" not in resume_text.lower():
        suggestions.append("Add Education details.")

    return suggestions


# -------------------------------
# Generate PDF Report
# -------------------------------
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

    c.setTitle("Resume Screening Report")

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, 800, "AI Resume Screening Report")

    c.setFont("Helvetica", 12)

    y = 770

    c.drawString(50, y, f"Candidate Name: {name}")
    y -= 20

    c.drawString(50, y, f"Email: {emails[0] if emails else 'Not Found'}")
    y -= 20

    c.drawString(50, y, f"Phone: {phones[0] if phones else 'Not Found'}")
    y -= 20

    c.drawString(50, y, f"ATS Score: {score:.2f}%")
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skills Found")
    y -= 20

    c.setFont("Helvetica", 12)

    for skill in found_skills:
        c.drawString(70, y, "• " + skill)
        y -= 18

    y -= 10

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Missing Skills")
    y -= 20

    c.setFont("Helvetica", 12)

    for skill in missing_skills:
        c.drawString(70, y, "• " + skill)
        y -= 18

    y -= 10

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Suggestions")
    y -= 20

    c.setFont("Helvetica", 12)

    if suggestions:
        for suggestion in suggestions:
            c.drawString(70, y, "• " + suggestion)
            y -= 18
    else:
        c.drawString(70, y, "• Excellent Resume")
        y -= 18

    c.save()

    buffer.seek(0)

    return buffer