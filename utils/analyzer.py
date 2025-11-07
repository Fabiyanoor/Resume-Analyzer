import os
import json
from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class ResumeAnalyzer:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
    def _get_llm(self, choice: str):
        """Get the appropriate LLM based on choice"""
        if "8B" in choice or "Fast" in choice:
            return ChatGroq(
                model_name="llama-3.1-8b-instant",  # Fast model
                api_key=self.groq_api_key
            )
        elif "70B" in choice or "Powerful" in choice:
            return ChatGroq(
                model_name="llama-3.1-70b-versatile",  # Powerful model
                api_key=self.groq_api_key
            )
        else:
            return ChatGroq(
                model_name="llama-3.1-8b-instant",  # Default to fast model
                api_key=self.groq_api_key
            )
    
    def _get_safe_llm(self, choice: str):
        """Get LLM with fallback for unavailable models"""
        try:
            llm = self._get_llm(choice)
            # Test if the model is available by making a simple call
            test_prompt = "Say 'test'"
            llm.invoke(test_prompt)
            return llm
        except Exception as e:
            # If any model fails, fallback to the reliable 8B model
            print(f"Model unavailable, falling back to llama-3.1-8b-instant. Error: {e}")
            return ChatGroq(
                model_name="llama-3.1-8b-instant",
                api_key=self.groq_api_key
            )
    
    def analyze_resume(self, resume_data: Dict, llm_choice: str) -> Dict:
        """Comprehensive resume analysis"""
        llm = self._get_safe_llm(llm_choice)
        
        template = """
        Analyze this resume data and provide constructive feedback in JSON format:
        
        {resume_data}
        
        Return ONLY valid JSON with this exact structure:
        {{
            "overall_score": 85,
            "skills_score": 90,
            "experience_level": "Mid-Level",
            "skills_breakdown": {{
                "technical_skills": 85,
                "soft_skills": 80,
                "industry_knowledge": 75
            }},
            "recommendations": [
                "Add more quantifiable achievements",
                "Include specific project outcomes",
                "Expand on leadership experience"
            ]
        }}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume_data"]
        )
        
        # Modern LangChain approach
        chain = prompt | llm
        result = chain.invoke({"resume_data": json.dumps(resume_data)})
        
        return self._safe_json_parse(result.content, {
            "overall_score": 75,
            "skills_score": 80,
            "experience_level": "Mid-Level",
            "skills_breakdown": {
                "technical_skills": 75,
                "soft_skills": 70,
                "industry_knowledge": 65
            },
            "recommendations": [
                "Focus on adding more specific achievements",
                "Include metrics and numbers to quantify impact",
                "Highlight leadership and collaboration experiences"
            ]
        })
    
    def job_match_analysis(self, resume_text: str, job_description: str, llm_choice: str) -> Dict:
        """Analyze match between resume and job description"""
        llm = self._get_safe_llm(llm_choice)
        
        template = """
        Analyze the match between resume and job description. Return ONLY valid JSON:
        
        RESUME: {resume_text}
        JOB: {job_description}
        
        JSON structure:
        {{
            "match_score": 85,
            "category_scores": {{
                "skills": 90,
                "experience": 80,
                "education": 85,
                "culture_fit": 75
            }},
            "strengths": ["Strong technical skills", "Relevant experience"],
            "improvements": ["Gain leadership experience", "Learn specific technology"]
        }}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume_text", "job_description"]
        )
        
        chain = prompt | llm
        result = chain.invoke({
            "resume_text": resume_text, 
            "job_description": job_description
        })
        
        return self._safe_json_parse(result.content, {
            "match_score": 70,
            "category_scores": {
                "skills": 75,
                "experience": 65,
                "education": 70,
                "culture_fit": 60
            },
            "strengths": ["Good foundational skills", "Relevant educational background"],
            "improvements": ["Gain more industry experience", "Develop missing technical skills"]
        })
    
    def skill_gap_analysis(self, resume_text: str, target_role: str, llm_choice: str) -> Dict:
        """Analyze skills gap for target role"""
        llm = self._get_safe_llm(llm_choice)
        
        template = """
        Analyze skills gap for target role. Return ONLY valid JSON:
        
        RESUME: {resume_text}
        TARGET: {target_role}
        
        JSON structure:
        {{
            "required_skills": ["Python", "SQL", "ML"],
            "current_skills": ["Python", "SQL"],
            "missing_skills": ["ML", "Data Viz"],
            "learning_path": ["Take ML course", "Build projects"]
        }}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume_text", "target_role"]
        )
        
        chain = prompt | llm
        result = chain.invoke({
            "resume_text": resume_text, 
            "target_role": target_role
        })
        
        return self._safe_json_parse(result.content, {
            "required_skills": ["Python", "SQL", "Machine Learning", "Data Visualization"],
            "current_skills": ["Python", "SQL"],
            "missing_skills": ["Machine Learning", "Data Visualization"],
            "learning_path": [
                "Take online course in Machine Learning fundamentals",
                "Learn data visualization with Tableau or Power BI",
                "Build portfolio projects using these skills"
            ]
        })
    
    def generate_interview_questions(self, resume_text: str, job_description: str, llm_choice: str) -> Dict:
        """Generate personalized interview questions"""
        llm = self._get_safe_llm(llm_choice)
        
        template = """
        Generate interview questions. Return ONLY valid JSON:
        
        RESUME: {resume_text}
        JOB: {job_description}
        
        JSON structure:
        {{
            "technical_questions": ["Q1", "Q2", "Q3", "Q4", "Q5"],
            "behavioral_questions": ["Q1", "Q2", "Q3", "Q4", "Q5"],
            "company_questions": ["Q1", "Q2", "Q3"]
        }}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["resume_text", "job_description"]
        )
        
        chain = prompt | llm
        result = chain.invoke({
            "resume_text": resume_text, 
            "job_description": job_description
        })
        
        return self._safe_json_parse(result.content, {
            "technical_questions": [
                "Explain your experience with the technologies mentioned in your resume",
                "Describe a challenging technical problem you solved recently",
                "How do you stay updated with the latest technologies in your field?",
                "What development methodologies have you worked with?",
                "Can you explain your experience with version control systems?"
            ],
            "behavioral_questions": [
                "Tell me about a time you worked in a team under pressure",
                "Describe a situation where you had to learn something new quickly",
                "How do you handle conflicting priorities?",
                "Tell me about a time you made a mistake and how you handled it",
                "Describe your approach to mentoring junior team members"
            ],
            "company_questions": [
                "Why are you interested in this type of role at our company?",
                "What do you know about our industry and recent trends?",
                "How do you see yourself contributing to our company's goals?"
            ]
        })
    
    def _safe_json_parse(self, text: str, default: Dict) -> Dict:
        """Safely parse JSON from LLM response"""
        try:
            # Extract JSON from text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        return default