# Student Feedback Review System 🎓

A web-based feedback management system developed for educational institutions to collect anonymous student feedback about subjects and teachers. The system helps administrators and faculty members understand student opinions and improve the overall learning experience.

---

## ✨ Features

### Student
- Submit anonymous feedback
- Select subject and teacher
- Give ratings on multiple criteria
- Share suggestions and comments

### Teacher
- View received feedback
- Monitor ratings and performance
- Access feedback insights

### Admin
- Manage teachers
- Manage subjects
- Manage subject-teacher mappings
- View and monitor feedback
- Access analytics dashboard

### AI Integration
- Automatic sentiment analysis using TextBlob
- Classifies feedback as Positive, Neutral, or Negative

---

## 🛠️ Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **NLP:** TextBlob
- **Icons:** Lucide Icons

---

## 📁 Project Structure

```text
Student Feedback Review System/
│
├── app.py
├── database.py
├── feedback_system.db
├── requirements.txt
│
├── routes/
│   ├── admin.py
│   ├── feedback.py
│   └── main.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── admin/
│   ├── teacher/
│   ├── index.html
│   ├── login.html
│   └── feedback.html
│
└── utils/
    └── sentiment.py
```

---

## 🗄️ Database Tables

- Admins
- Teachers
- Subjects
- Subject Teachers
- Feedbacks

---

## 🚀 Installation

1. Clone the repository

```bash
git clone <repository-url>
cd Student-Feedback-Review-System
```

2. Create virtual environment

```bash
python -m venv venv
```

3. Activate virtual environment

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run the application

```bash
python app.py
```

6. Open in browser

```text
http://127.0.0.1:5000
```

---

## 🔐 Modules

### Student Module
- Anonymous Feedback Submission
- Teacher & Subject Selection
- Rating System

### Teacher Module
- Feedback Dashboard
- Performance Monitoring

### Admin Module
- User Management
- Subject Management
- Feedback Monitoring
- Analytics Dashboard

---

## 📄 Project Objective

The main objective of this project is to provide a secure and anonymous platform where students can share their feedback about subjects and faculty members. The collected feedback helps teachers and administrators identify strengths, address concerns, and improve the overall quality of education.

---

## 👨‍💻 Developed For

Minor Project – Student Feedback Review System

Department of Computer Science & Engineering
