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

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Screening & ATS System")

st.markdown(
    """
Upload your resume and compare it with a Job Description.
The system calculates the ATS score, identifies skills,
shows missing skills and suggests improvements.
"""
)

st.divider()

# --------------------------------------------------
# Job Description
# --------------------------------------------------

job = st.text_area(
    "📋 Enter Job Description",
    height=200
)

# --------------------------------------------------
# Upload Resume
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
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

# --------------------------------------------------
# Check Match
# --------------------------------------------------

if st.button("🔍 Check Match"):

    if job.strip() == "":
        st.warning("Please enter Job Description.")
        st.stop()

    if resume_text.strip() == "":
        st.warning("Please upload Resume.")
        st.stop()

    # ------------------------------------------
    # Processing
    # ------------------------------------------

    score = calculate_match_score(
        job,
        resume_text
    )

    found_skills, skills = extract_skills(
        resume_text
    )

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

    required_skills = 0

    for skill in skills:

        if skill.lower() in job.lower():
            required_skills += 1

    if required_skills == 0:

        skill_match = 100

    else:

        skill_match = (
            len(found_skills) /
            required_skills
        ) * 100

    # --------------------------------------------------
    # ATS Dashboard
    # --------------------------------------------------

    st.divider()

    st.subheader("📊 ATS Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎯 ATS Score",
        f"{score:.2f}%"
    )

    col2.metric(
        "🛠 Skills Found",
        len(found_skills)
    )

    col3.metric(
        "❌ Missing Skills",
        len(missing_skills)
    )

    st.progress(
        min(int(score),100)
    )

    st.info(
        f"""
ATS Score : **{score:.2f}%**

Skill Match : **{skill_match:.1f}%**

The ATS score is calculated using:

• Resume similarity

• Skill matching

• Keyword relevance
"""
    )
    # --------------------------------------------------
    # Resume Rating
    # --------------------------------------------------

    st.divider()

    st.subheader("⭐ Resume Rating")

    if score >= 90:
        st.success("🌟 Excellent Resume Match")
    elif score >= 75:
        st.success("✅ Good Resume Match")
    elif score >= 60:
        st.warning("👍 Average Resume Match")
    else:
        st.error("❌ Needs Improvement")

    # --------------------------------------------------
    # Skills Found
    # --------------------------------------------------

    st.divider()

    st.subheader("🛠 Skills Found")

    if found_skills:

        cols = st.columns(3)

        for i, skill in enumerate(found_skills):
            cols[i % 3].success(skill)

    else:

        st.warning("No skills detected.")

    # --------------------------------------------------
    # Missing Skills
    # --------------------------------------------------

    st.divider()

    st.subheader("❌ Missing Skills")

    if missing_skills:

        cols = st.columns(3)

        for i, skill in enumerate(missing_skills):
            cols[i % 3].error(skill)

    else:

        st.success("🎉 No Missing Skills Found!")

    # --------------------------------------------------
    # Candidate Details
    # --------------------------------------------------

    st.divider()

    st.subheader("👤 Candidate Details")

    c1, c2 = st.columns(2)

    with c1:
        st.write("### 👤 Name")
        st.success(name)

        st.write("### 📧 Email")
        st.info(emails[0] if emails else "Not Found")

    with c2:
        st.write("### 📱 Phone")
        st.info(phones[0] if phones else "Not Found")

        st.write("### 📄 Resume Pages")
        st.info(page_count)

    # --------------------------------------------------
    # Resume Suggestions
    # --------------------------------------------------

    st.divider()

    st.subheader("💡 Resume Improvement Suggestions")

    if suggestions:

        for suggestion in suggestions:
            st.warning("💡 " + suggestion)

    else:

        st.success(
            "Excellent! Your resume is well optimized for ATS."
        )

    # --------------------------------------------------
    # Resume Statistics
    # --------------------------------------------------

    st.divider()

    st.subheader("📈 Resume Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Words",
        len(resume_text.split())
    )

    col2.metric(
        "Characters",
        len(resume_text)
    )

    col3.metric(
        "Pages",
        page_count
    )

    # --------------------------------------------------
    # Resume Preview
    # --------------------------------------------------

    st.divider()

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=300
    )

    # --------------------------------------------------
    # PDF Report
    # --------------------------------------------------

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

    st.balloons()