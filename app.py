import os
import re
from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import PyPDF2
from config import Config
from extensions import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from models import User, ResumeReport


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
#  HOME → Redirect to Login
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))
# =========================
# Register
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already registered!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")
# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password")

    return render_template("login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.name)

import os
# =========================
# UPLOAD & ANALYZE RESUME
# =========================
@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
   ## Update Your /analyze Route
    # job_role = request.form.get("job_role")
    file = request.files.get("resume")

    if not file:
        flash("Please upload a resume file.")
        return redirect(url_for("dashboard"))

    content = ""

    # Handle file types
    if file.filename.endswith(".txt"):
        content = file.read().decode("utf-8")

    elif file.filename.endswith(".pdf"):
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content += page.extract_text()

    else:
        flash("Only PDF or TXT files are allowed.")
        return redirect(url_for("dashboard"))

    # -------------------------
    # Keyword Matching Logic
    # -------------------------


    # keywords = [
    #     "Python", "Flask", "SQL",
    #     "Machine Learning", "Java",
    #     "HTML", "CSS", "JavaScript"
    # ]
    keywords = [

    # # Programming Languages
    # "Python", "Java", "JavaScript", "C++", "C",

    # Web Technologies
    "HTML", "CSS", "Bootstrap", "React", "Angular",
    "Vue", "Node.js", "Flask", "Django",
    "REST API", "JSON", "AJAX",

    # # Java Stack
    # "Spring", "Spring Boot", "Hibernate",
    # "JDBC", "Servlets", "JSP",
    # "OOP", "Collections", "Multithreading",

    # # Databases
    # "SQL", "MySQL", "PostgreSQL",
    # "MongoDB", "Oracle",

    # # Data & Analytics
    # "Data Analysis", "Data Cleaning",
    # "Data Visualization", "Data Mining",
    # "Business Intelligence",
    # "ETL", "Dashboarding",

    # # Python Libraries
    # "Pandas", "NumPy", "Matplotlib",
    # "Seaborn", "Scikit-learn",
    # "TensorFlow", "Keras",

    # # Machine Learning
    # "Machine Learning", "Deep Learning",
    # "Regression", "Classification",
    # "Clustering", "NLP",

    # # Tools
    # "Excel", "Power BI", "Tableau",
    # "Git", "GitHub",
    # "Docker", "AWS",

    # # Concepts
    # "Statistics", "Algorithms",
    # "Data Structures", "Design Patterns",
    # "Microservices", "API Integration"
]

    detected_skills = []
    missing_skills = []

    for word in keywords:
        if word.lower() in content.lower():
            detected_skills.append(word)
        else:
            missing_skills.append(word)

    score = int((len(detected_skills) / len(keywords)) * 100)

    # -------------------------
    # Suggestions (IMPORTANT)
    # -------------------------

    suggestions = []

    if score < 40:
        suggestions.append("Add more technical skills.")
        suggestions.append("Include measurable achievements.")
    elif score < 70:
        suggestions.append("Improve keyword optimization.")
        suggestions.append("Add more project details.")
    else:
        suggestions.append("Great resume structure.")
        suggestions.append("Try tailoring resume for specific jobs.")

    # -------------------------
    # Save to Database
    # -------------------------

    report = ResumeReport(
        user_id=current_user.id,
        file_name=file.filename,
        ats_score=score,
        skills_found=", ".join(detected_skills),
        missing_skills=", ".join(missing_skills),
        suggestions=", ".join(suggestions)
    )

    db.session.add(report)
    db.session.commit()

    return render_template(
        "result.html",
        score=score,
        skills=detected_skills,
        suggestions=suggestions
    )

# =========================
# RESUME HISTORY
# =========================
@app.route("/history")
@login_required
def history():
    reports = ResumeReport.query.filter_by(user_id=current_user.id)\
                                 .order_by(ResumeReport.created_at.desc())\
                                 .all()

    return render_template("history.html", reports=reports)
# =========================
# VIEW SINGLE REPORT
# =========================
@app.route("/report/<int:report_id>")
@login_required
def view_report(report_id):
    report = ResumeReport.query.get_or_404(report_id)

    # Security check (important)
    if report.user_id != current_user.id:
        flash("Unauthorized access.")
        return redirect(url_for("history"))

    return render_template("view_report.html", report=report)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)





