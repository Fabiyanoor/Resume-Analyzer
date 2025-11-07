import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from utils.resume_parser import ResumeParser
from utils.analyzer import ResumeAnalyzer
from utils.visualizations import create_skill_chart, create_match_radar

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ResumeAnalyzerApp:
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
        self.parser = ResumeParser()
        
    def run(self):
        # Header
        st.markdown('<h1 class="main-header">🚀 AI-Powered Resume Analyzer Pro</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar
        st.sidebar.title("Configuration")
        analysis_type = st.sidebar.selectbox(
            "Select Analysis Type",
            ["Resume Analysis", "Job Matching", "Skill Gap Analysis", "Interview Prep"]
        )
        
        llm_choice = st.sidebar.radio(
    "Select AI Model",
    ["Groq (Llama-3.1-8B - Fast)", "Groq (Llama-3.1-70B - Powerful)"]  # Updated models
                                      )
        # Main content
        if analysis_type == "Resume Analysis":
            self.resume_analysis(llm_choice)
        elif analysis_type == "Job Matching":
            self.job_matching(llm_choice)
        elif analysis_type == "Skill Gap Analysis":
            self.skill_gap_analysis(llm_choice)
        else:
            self.interview_prep(llm_choice)
    
    def resume_analysis(self, llm_choice):
        st.header("📄 Resume Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Input Your Resume")
            resume_input = st.text_area(
                "Paste your resume content here:",
                height=300,
                placeholder="Paste your resume text here...\n\nInclude:\n- Work experience\n- Education\n- Skills\n- Projects\n- Achievements"
            )
            
            resume_file = st.file_uploader(
                "Or upload resume file (PDF, DOCX, TXT)",
                type=['pdf', 'docx', 'txt'],
                key="resume_upload"
            )
        
        with col2:
            if resume_input or resume_file:
                st.subheader("Analysis Results")
                
                with st.spinner("🤖 AI is analyzing your resume..."):
                    try:
                        # Parse resume
                        if resume_file:
                            resume_data = self.parser.parse_resume(resume_file)
                        else:
                            resume_data = self.parser.parse_resume(resume_input)
                        
                        # Analyze resume
                        analysis_result = self.analyzer.analyze_resume(
                            resume_data, llm_choice
                        )
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Overall Score", f"{analysis_result['overall_score']}/100")
                        with col2:
                            st.metric("Skills Match", f"{analysis_result['skills_score']}%")
                        with col3:
                            st.metric("Experience Level", analysis_result['experience_level'])
                        
                        # Skills visualization
                        st.subheader("📊 Skills Breakdown")
                        st.plotly_chart(
                            create_skill_chart(analysis_result['skills_breakdown']),
                            use_container_width=True
                        )
                        
                        # Recommendations
                        st.subheader("💡 Improvement Recommendations")
                        for i, rec in enumerate(analysis_result['recommendations'], 1):
                            st.write(f"{i}. {rec}")
                            
                    except Exception as e:
                        st.error(f"Error analyzing resume: {str(e)}")
            else:
                st.info("👆 Please enter your resume content or upload a file to get started.")
    
    def job_matching(self, llm_choice):
        st.header("🔍 Job Matching Analysis")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Your Resume")
            resume_text = st.text_area(
                "Paste your resume content:",
                height=200,
                placeholder="Paste your resume content here..."
            )
        
        with col2:
            st.subheader("Job Description")
            job_description = st.text_area(
                "Paste the job description:",
                height=200,
                placeholder="Paste the job description here..."
            )
        
        if st.button("🔍 Analyze Job Match", type="primary") and resume_text and job_description:
            with st.spinner("Analyzing job match..."):
                try:
                    match_result = self.analyzer.job_match_analysis(
                        resume_text, job_description, llm_choice
                    )
                    
                    # Display match score
                    match_score = match_result['match_score']
                    st.subheader(f"Overall Match Score: {match_score}%")
                    
                    if match_score >= 80:
                        st.success("🎉 Strong Match! You're a great fit for this role.")
                    elif match_score >= 60:
                        st.warning("👍 Good Match! Some areas could be improved.")
                    else:
                        st.error("📝 Needs Work! Significant gaps identified.")
                    
                    st.progress(match_score / 100)
                    
                    # Radar chart
                    st.plotly_chart(
                        create_match_radar(match_result['category_scores']),
                        use_container_width=True
                    )
                    
                    # Detailed analysis
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("✅ Your Strengths")
                        for strength in match_result['strengths']:
                            st.success(f"• {strength}")
                    
                    with col2:
                        st.subheader("📝 Areas for Improvement")
                        for improvement in match_result['improvements']:
                            st.error(f"• {improvement}")
                            
                except Exception as e:
                    st.error(f"Error in job matching: {str(e)}")
    
    def skill_gap_analysis(self, llm_choice):
        st.header("📊 Skill Gap Analysis")
        
        target_role = st.text_input(
            "Enter your target role:",
            placeholder="e.g., Data Scientist, Frontend Developer, Product Manager"
        )
        
        resume_text = st.text_area(
            "Paste your resume content:",
            height=200,
            placeholder="Paste your resume content here..."
        )
        
        if st.button("Analyze Skill Gaps", type="primary") and target_role and resume_text:
            with st.spinner("Analyzing skill gaps..."):
                try:
                    gap_analysis = self.analyzer.skill_gap_analysis(
                        resume_text, target_role, llm_choice
                    )
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("🎯 Required Skills")
                        for skill in gap_analysis['required_skills']:
                            st.write(f"• {skill}")
                    
                    with col2:
                        st.subheader("✅ Your Current Skills")
                        for skill in gap_analysis['current_skills']:
                            st.write(f"• {skill}")
                    
                    with col3:
                        st.subheader("📝 Missing Skills")
                        for skill in gap_analysis['missing_skills']:
                            st.write(f"• {skill}")
                    
                    # Learning path
                    st.subheader("🚀 Recommended Learning Path")
                    for i, recommendation in enumerate(gap_analysis['learning_path'], 1):
                        st.info(f"{i}. {recommendation}")
                        
                except Exception as e:
                    st.error(f"Error in skill gap analysis: {str(e)}")
    
    def interview_prep(self, llm_choice):
        st.header("🎯 Interview Preparation")
        
        job_description = st.text_area(
            "Paste the job description:",
            height=150,
            placeholder="Paste the job description here..."
        )
        
        resume_text = st.text_area(
            "Paste your resume content (optional):",
            height=150,
            placeholder="Paste your resume content here..."
        )
        
        if st.button("Generate Interview Questions", type="primary") and job_description:
            with st.spinner("Generating personalized interview questions..."):
                try:
                    questions = self.analyzer.generate_interview_questions(
                        resume_text if resume_text else "General candidate", 
                        job_description, 
                        llm_choice
                    )
                    
                    st.subheader("🧠 Technical Questions")
                    for i, question in enumerate(questions['technical_questions'], 1):
                        st.write(f"**{i}. {question}**")
                    
                    st.subheader("💼 Behavioral Questions")
                    for i, question in enumerate(questions['behavioral_questions'], 1):
                        st.write(f"**{i}. {question}**")
                    
                    st.subheader("🏢 Company & Role Questions")
                    for i, question in enumerate(questions['company_questions'], 1):
                        st.write(f"**{i}. {question}**")
                        
                except Exception as e:
                    st.error(f"Error generating questions: {str(e)}")

# Run the app
if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ GROQ_API_KEY not found. Please check your .env file")
    else:
        app = ResumeAnalyzerApp()
        app.run()