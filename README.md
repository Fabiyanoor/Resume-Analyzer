# 🚀 AI Resume Analyzer Pro

A comprehensive AI-powered resume analysis platform that provides intelligent career insights, job matching, skill gap analysis, and interview preparation using advanced language models.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.0.346-green.svg)
![Groq](https://img.shields.io/badge/Groq-API-orange.svg)

## ✨ Features

### 📄 Resume Analysis
- **AI-Powered Scoring**: Get overall resume score and skills assessment
- **Experience Level Detection**: Automatic classification (Entry, Mid, Senior)
- **Skills Breakdown**: Detailed analysis of technical, soft skills, and industry knowledge
- **Actionable Recommendations**: Personalized improvement suggestions

### 🔍 Job Matching
- **Compatibility Scoring**: Percentage match between resume and job descriptions
- **Category Analysis**: Skills, experience, education, and culture fit evaluation
- **Strengths Identification**: Highlight your competitive advantages
- **Improvement Areas**: Specific recommendations to increase job fit

### 📊 Skill Gap Analysis
- **Target Role Assessment**: Compare current skills with role requirements
- **Missing Skills Identification**: Pinpoint exactly what you need to learn
- **Personalized Learning Path**: Step-by-step roadmap for skill development
- **Career Transition Support**: Smooth transition planning to new roles

### 🎯 Interview Preparation
- **Technical Questions**: Role-specific technical interview questions
- **Behavioral Questions**: Situation-based behavioral questions
- **Company-Specific Questions**: Tailored questions for target companies
- **Personalized Content**: Questions based on your resume and target job

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, Groq API (Llama 3.1 models)
- **Data Processing**: Pandas, PyPDF2, python-docx
- **Visualization**: Plotly
- **Environment**: Python-dotenv

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/))

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Fabiyanoor/Resume-Analyzer.git
   cd Resume-Analyzer
Create virtual environment


1. **Clone the repository**
   ```bash
   git clone https://github.com/Fabiyanoor/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Add your Groq API key to .env:
   # GROQ_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```


🚀 Usage
Launch the application: Run streamlit run app.py

Select analysis type: Choose from four main modules

Input your data: Paste resume content or upload files (PDF, DOCX, TXT)

Get insights: Receive AI-powered analysis and recommendations

Visualize results: Interactive charts and progress indicators

**Supported File Formats**
📄 PDF documents

📝 DOCX (Word documents)

📋 Plain text files

📝 Direct text input


