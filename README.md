# Student Feedback Review System 🎓💬

An AI-powered, modern, and anonymous student feedback platform designed for educational institutions. The system enables students to submit ratings and feedback for courses and instructors while maintaining complete anonymity. Administrators and teachers can access dedicated dashboards to monitor feedback, analyze performance, and gain meaningful insights for continuous improvement.

Built with Flask, SQLite, and TextBlob, the platform combines a responsive SaaS-inspired user interface with intelligent sentiment analysis to create a complete feedback management solution.

---

## 🌟 Key Features

### 👨‍🎓 For Students
- 100% Anonymous Feedback Submission
- Dynamic Subject & Teacher Selection
- Interactive Rating System
- Anonymous Review Submission
- Responsive User Experience

### 🤖 AI Sentiment Analysis
- TextBlob NLP Integration
- Automatic Sentiment Classification
- Positive, Neutral & Negative Detection
- Real-Time Feedback Processing
- Future Analytics Support

### 👨‍🏫 For Teachers
- Personal Dashboard
- Performance Monitoring
- Recent Feedback Overview
- Rating Insights
- Teaching Improvement Analytics

### 👨‍💼 For Administrators
- Complete System Management
- Teacher Management
- Subject Management
- Subject Mapping Management
- Feedback Monitoring
- Analytics & Insights
- Administrator Management

### 🎨 UI/UX Highlights
- Modern SaaS Design Language
- Responsive Dashboard Layouts
- Professional Sidebar Navigation
- Premium Card-Based Interface
- Smooth Animations & Hover Effects
- Consistent Typography & Spacing

---

## 🛠️ Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Database | SQLite3 |
| NLP Engine | TextBlob |
| Icons | Lucide Icons |
| UI Design | Custom SaaS Design System |

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
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
└── templates/
    ├── 404.html
    ├── 500.html
    ├── base.html
    ├── index.html
    ├── login.html
    ├── feedback.html
    │
    ├── admin/
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── analytics.html
    │   ├── feedbacks.html
    │   ├── teachers.html
    │   ├── subjects.html
    │   ├── mappings.html
    │   └── admins.html
    │
    └── teacher/
        ├── dashboard.html
        └── feedbacks.html
```

---

## 📊 Database Schema

### Teachers

| Field | Type |
|---------|---------|
| user_id | Primary Key |
| name | Text |
| password | Text |
| created_at | Timestamp |

### Admins

| Field | Type |
|---------|---------|
| user_id | Primary Key |
| name | Text |
| password | Text |
| role | Text |

### Subjects

| Field | Type |
|---------|---------|
| subject_code | Primary Key |
| subject_name | Text |

### Subject Teachers

| Field | Type |
|---------|---------|
| id | Primary Key |
| subject_code | Foreign Key |
| teacher_user_id | Foreign Key |

### Feedbacks

| Field | Type |
|---------|---------|
| id | Primary Key |
| subject_code | Foreign Key |
| teacher_user_id | Foreign Key |
| teaching_style_rating | Integer |
| subject_knowledge_rating | Integer |
| class_environment_rating | Integer |
| feedback_message | Text |
| sentiment_label | Text |
| created_at | Timestamp |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd Student-Feedback-Review-System
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
python app.py
```

### 6️⃣ Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🔐 Authentication System

The platform uses secure role-based authentication.

### Administrator Access
- Manage Teachers
- Manage Subjects
- Manage Subject Mappings
- Manage Admins
- Review Feedback
- Access Analytics Dashboard

### Teacher Access
- View Assigned Subjects
- Access Feedback Dashboard
- Monitor Ratings
- Review Performance Insights

### Student Access
- Submit Anonymous Feedback
- Rate Learning Experience
- Share Suggestions & Reviews

---

## 🗺️ Route Structure

### Public Routes

```text
/
/login
/feedback
/get-teachers/<subject_code>
```

### Teacher Routes

```text
/teacher/dashboard
/teacher/feedbacks
/logout
```

### Admin Routes

```text
/admin/dashboard
/admin/analytics
/admin/feedbacks
/admin/teachers
/admin/subjects
/admin/mappings
/admin/admins
/logout
```

---

## 🔒 Security Features

- Session-Based Authentication
- Role-Based Access Control
- Protected Admin Routes
- Protected Teacher Routes
- Secure Logout Handling
- Parameterized SQLite Queries
- Anonymous Feedback Collection
- Input Validation & Sanitization
- Cache-Control Protection After Logout

---

## 📈 Core Modules

### Student Module
- Submit Anonymous Feedback
- Dynamic Teacher Loading
- Multi-Criteria Rating System
- Review Submission

### Teacher Module
- Personal Dashboard
- Feedback Monitoring
- Rating Insights
- Performance Tracking

### Admin Module
- Dashboard Overview
- Teacher Management
- Subject Management
- Subject Mapping
- Administrator Management
- Feedback Monitoring
- Analytics Dashboard

---

## 🎯 Project Highlights

- Anonymous Student Feedback Collection
- AI-Powered Sentiment Analysis
- Role-Based Authentication System
- Admin & Teacher Dashboards
- Subject & Faculty Management
- SQLite Database Integration
- Flask-Based Backend Architecture
- Modern SaaS-Inspired User Interface
- Responsive Design Across Devices
- Clean Modular Project Structure

---
