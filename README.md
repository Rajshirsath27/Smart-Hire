# Resume Analyzer Web Application

## 🚀 Project Overview
The **Resume Analyzer** is a full-stack web application that evaluates resumes using **keyword extraction** and **rule-based scoring** to simulate an **Applicant Tracking System (ATS)**.  
It provides **category-wise scoring**, structured feedback, and a dashboard to track resume analysis history. 

## 💡 Features

- **User Authentication**  
  - Registration and login system  
  - Password hashing and secure session management  

- **Resume Upload & Parsing**  
  - Upload PDF or text files  
  - Text extraction and preprocessing  

- **Keyword Extraction & Scoring**  
  - Compare resume content with role-specific skill dataset  
  - Calculate category-wise ATS score  
  - Generate structured improvement suggestions  

- **Dashboard & History Tracking**  
  - View all previously uploaded resumes  
  - Check scores and feedback  
---

## 🧰 Tech Stack

### Programming & Backend
- Python  
- Flask  
- SQLAlchemy ORM  
- Jinja2

### Database
- SQLite  
- CRUD Operations  
- Foreign Key Relationships

### Frontend
- HTML5, CSS3, Bootstrap  
- Responsive design using Jinja2 templates

### Authentication & Security
- Flask-Login  
- Secure Session Management  
- Password Hashing  

### Logic & Processing
- Text Processing & Cleaning  
- Keyword Extraction  
- Rule-Based Scoring Algorithm  
- Pattern Matching  
- Category-Based Evaluation

---

## ⚙️ How It Works (Step-by-Step)

1. **User Registration/Login** – Secure authentication using Flask-Login  
2. **Resume Upload** – Accept PDF or text files  
3. **Text Extraction & Preprocessing** – Clean text, lowercase, remove punctuation, tokenize  
4. **Keyword Matching** – Compare against predefined skill dataset  
5. **Score Calculation** – Category-wise match % and overall ATS score  
6. **Feedback Generation** – Provide suggestions for missing skills  
7. **Dashboard** – Display history of uploaded resumes with scores and feedback  

---

📊 **Usage**
Register and login
Upload resume (PDF or TXT)
View ATS score and feedback
Check history in the dashboard

