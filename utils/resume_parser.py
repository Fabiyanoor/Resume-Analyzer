import re
from typing import Dict, List
from docx import Document
import PyPDF2

class ResumeParser:
    def __init__(self):
        self.skill_keywords = self._load_skill_keywords()
    
    def _load_skill_keywords(self) -> List[str]:
        """Load common skill keywords"""
        return [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'nosql',
            'aws', 'docker', 'kubernetes', 'machine learning', 'deep learning',
            'tensorflow', 'pytorch', 'data analysis', 'tableau', 'power bi',
            'agile', 'scrum', 'devops', 'ci/cd', 'git', 'rest api', 'graphql',
            'html', 'css', 'typescript', 'angular', 'vue', 'mongodb', 'postgresql',
            'mysql', 'redis', 'linux', 'unix', 'bash', 'shell', 'powershell'
        ]
    
    def parse_resume(self, file) -> Dict:
        """Parse resume file and extract information"""
        if hasattr(file, 'read'):
            # It's a file upload
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                return self._parse_pdf(file)
            elif file_extension == 'docx':
                return self._parse_docx(file)
            elif file_extension == 'txt':
                return self._parse_txt(file)
        else:
            # It's text input
            return self._extract_information(file)
    
    def _parse_pdf(self, file) -> Dict:
        """Parse PDF resume using PyPDF2"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return self._extract_information(text)
        except Exception as e:
            return self._extract_information(f"PDF parsing error: {str(e)}")
    
    def _parse_docx(self, file) -> Dict:
        """Parse DOCX resume"""
        try:
            doc = Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return self._extract_information(text)
        except Exception as e:
            return self._extract_information(f"DOCX parsing error: {str(e)}")
    
    def _parse_txt(self, file) -> Dict:
        """Parse TXT resume"""
        try:
            text = file.read().decode('utf-8')
            return self._extract_information(text)
        except Exception as e:
            return self._extract_information(f"TXT parsing error: {str(e)}")
    
    def _extract_information(self, text: str) -> Dict:
        """Extract structured information from resume text"""
        # Basic information extraction using regex
        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        
        # Extract education
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'b\.', 'm\.', 'phd']
        education = []
        for keyword in education_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text.lower()):
                education.append(keyword)
        
        # Extract skills
        found_skills = []
        for skill in self.skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
                found_skills.append(skill)
        
        # Extract experience (simple years detection)
        experience_years = re.findall(r'(\d+)\s*(?:years?|yrs?)', text.lower())
        experience = experience_years[0] if experience_years else "Not specified"
        
        return {
            'email': email[0] if email else "Not found",
            'phone': phone[0] if phone else "Not found",
            'skills': found_skills,
            'education': list(set(education)),
            'experience_years': experience,
            'raw_text': text,
            'word_count': len(text.split()),
            'character_count': len(text)
        }