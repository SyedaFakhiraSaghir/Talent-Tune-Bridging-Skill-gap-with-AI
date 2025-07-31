import streamlit as st
import requests

# Database definition
SKILL_DB = {
    "data scientist": ["python", "machine learning", "sql", "statistics"],
    "web developer": ["javascript", "html", "css", "react"]
}

# UI Configuration
st.set_page_config(
    page_title="SkillBridge",
    page_icon="🌉",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .stTextArea textarea {
        min-height: 200px;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = "http://localhost:8000/analyze"

# Main Form
with st.form("analysis_form"):
    st.title("🌉 SkillBridge Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        resume_text = st.text_area(
            "Paste your resume/CV:",
            placeholder="Include your skills, experiences, and education...",
            height=200
        )
    
    with col2:
        target_job = st.selectbox(  # Fixed missing comma here
            "Target job role:",
            options=list(SKILL_DB.keys()),
            index=0
        )
    
    submitted = st.form_submit_button("Analyze Skills")

# Results Handling
if submitted:
    if not resume_text.strip():
        st.warning("Please enter your resume text")
    else:
        try:
            response = requests.post(
                API_URL,
                json={
                    "resume_text": resume_text,
                    "target_job": target_job
                }
            )
            result = response.json()
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Analysis Complete!")
                
                # Display results
                with st.expander("🔍 Results", expanded=True):
                    st.subheader("Your Skills")
                    st.write(", ".join(result.get("current_skills", [])) or "None identified")
                    
                    st.subheader("Missing Skills")
                    st.write(", ".join(result.get("missing_skills", [])) or "None missing")
                    
                    st.subheader("Recommended Learning")
                    for course in result.get("recommended_courses", []):
                        st.write(f"- {course['name']}")

        except requests.exceptions.RequestException:
            st.error("Could not connect to the analysis server")

# Sidebar Note
st.sidebar.markdown("""
**How to use:**
1. Run the backend server first
2. Paste your resume text
3. Select target job role
4. Click 'Analyze Skills'
""")