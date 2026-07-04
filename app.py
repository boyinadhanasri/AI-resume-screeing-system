import streamlit as st
import pdfplumber

from utils import (
    calculate_match_score,
    extract_skills,
    extract_missing_skills,
    extract_candidate_details,
    generate_suggestions,
    generate_pdf_report
)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Screening & ATS System")
st.markdown("### Upload a resume and compare it with a Job Description")
st.divider()

# -------------------------------
# Job Description
# -------------------------------
job = st.text_area("📋 Enter Job Description")

# -------------------------------
# Upload Resume
# -------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)

resume_text = ""
page_count = 0

if uploaded_file:

    with pdfplumber.open(uploaded_file) as pdf:

        page_count = len(pdf.pages)

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    st.success("✅ Resume uploaded successfully!")

# -------------------------------
# Check Match
# -------------------------------
if st.button("🔍 Check Match"):

    if job.strip() == "":
        st.warning("Please enter the Job Description.")
        st.stop()

    if resume_text.strip() == "":
        st.warning("Please upload a Resume.")
        st.stop()

    # -------------------------------
    # Processing
    # -------------------------------

    score = calculate_match_score(job, resume_text)

    found_skills, skills = extract_skills(resume_text)

    missing_skills = extract_missing_skills(
        job,
        resume_text,
        skills
    )

    name, emails, phones = extract_candidate_details(
        resume_text
    )

    suggestions = generate_suggestions(
        resume_text,
        missing_skills
    )

    # -------------------------------
    # Dashboard
    # -------------------------------

    st.divider()

    st.subheader("📊 ATS Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("🎯 ATS Score", f"{score:.2f}%")
    c2.metric("🛠 Skills Found", len(found_skills))
    c3.metric("❌ Missing Skills", len(missing_skills))

    st.progress(min(int(score), 100))

    # -------------------------------
    # Resume Rating
    # -------------------------------

    st.divider()

    st.subheader("⭐ Resume Rating")

    if score >= 80:
        st.success("Excellent Resume Match")
    elif score >= 60:
        st.info("Good Resume Match")
    elif score >= 40:
        st.warning("Average Resume Match")
    else:
        st.error("Poor Resume Match")

    # -------------------------------
    # Skills Found
    # -------------------------------

    st.divider()

    st.subheader("🛠 Skills Found")

    if found_skills:
        for skill in found_skills:
            st.success("✅ " + skill)
    else:
        st.warning("No skills found.")

    # -------------------------------
    # Missing Skills
    # -------------------------------

    st.divider()

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error("❌ " + skill)
    else:
        st.success("🎉 No Missing Skills")

    # -------------------------------
    # Candidate Details
    # -------------------------------

    st.divider()

    st.subheader("👤 Candidate Details")

    st.write("### 👤 Name")
    st.write(name)

    st.write("### 📧 Email")
    st.write(emails[0] if emails else "Not Found")

    st.write("### 📱 Phone")
    st.write(phones[0] if phones else "Not Found")

    # -------------------------------
    # Suggestions
    # -------------------------------

    st.divider()

    st.subheader("💡 Resume Improvement Suggestions")

    if suggestions:
        for suggestion in suggestions:
            st.warning("💡 " + suggestion)
    else:
        st.success("Excellent! Your resume looks well prepared.")

    # -------------------------------
    # Statistics
    # -------------------------------

    st.divider()

    st.subheader("📈 Resume Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Words", len(resume_text.split()))
    c2.metric("Characters", len(resume_text))
    c3.metric("Pages", page_count)

    # -------------------------------
    # Resume Preview
    # -------------------------------

    st.divider()

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=300
    )

    # -------------------------------
    # Download PDF Report
    # -------------------------------

    st.divider()

    st.subheader("📥 Download Resume Screening Report")

    pdf_buffer = generate_pdf_report(
        name,
        emails,
        phones,
        score,
        found_skills,
        missing_skills,
        suggestions
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="Resume_Screening_Report.pdf",
        mime="application/pdf"
    )