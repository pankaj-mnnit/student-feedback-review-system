# 🎓 Student Feedback Review System

A web-based feedback management system that enables students to submit anonymous feedback for subjects and teachers. The system uses sentiment analysis to classify reviews and provides dedicated dashboards for teachers and administrators to monitor feedback and performance insights.

---

## ✨ Features

### 👨‍🎓 Student Module
- Anonymous feedback submission
- Subject-wise teacher selection
- 1–5 star rating system
- Feedback comments with character limit
- Responsive and user-friendly interface

### 🤖 Sentiment Analysis
- Automatic sentiment classification using TextBlob
- Categorizes feedback as:
  - Positive
  - Neutral
  - Negative

### 👨‍🏫 Teacher Module
- Personal dashboard
- Average rating overview
- Feedback statistics
- Sentiment distribution analysis
- View received feedback

### 👨‍💼 Admin Module
- Manage teachers and subjects
- View and manage feedback records
- Dashboard with overall statistics
- Create and manage admin accounts

---

## 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Frontend | HTML, CSS, JavaScript, Bootstrap 5 |
| Backend | Python, Flask |
| Database | SQLite |
| NLP | TextBlob |

---

## 📁 Project Structure

```text
Student Feedback Review System/
│
├── app.py
├── database.py
├── requirements.txt
├── feedback_system.db
│
├── routes/
│   ├── admin.py
│   ├── feedback.py
│   └── main.py
│
├── utils/
│   └── sentiment.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    ├── 404.html
    ├── 500.html
    ├── base.html
    ├── index.html
    ├── feedback.html
    │
    ├── admin/
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── feedbacks.html
    │   ├── teachers.html
    │   ├── subjects.html
    │   ├── admins.html
    │   └── profile.html
    │
    └── teacher/
        ├── dashboard.html
        └── feedbacks.html
```

---

## 🗄️ Database Tables

The system uses SQLite and includes the following tables:

- `subjects`
- `teachers`
- `subject_teachers`
- `feedback`

---

## 🔐 Default Login Credentials

### Admin Account

```text
User ID  : ADM001
Password : 123456
```

### Teacher Account

```text
User ID  : TCH001
Password : 123456
```

---

## 🎯 Project Objective

The objective of this project is to provide a simple and efficient platform for collecting student feedback, analyzing opinions using sentiment analysis, and helping educational institutions improve teaching quality through data-driven insights.

---

## 📈 Future Enhancements

- Advanced analytics dashboard
- Feedback report export
- Email notifications
- Enhanced sentiment analysis
- Improved data visualization

---
