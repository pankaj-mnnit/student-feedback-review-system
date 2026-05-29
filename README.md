# Student Feedback Review System 🎓💬

An AI-powered, modern, and anonymous student feedback platform designed for educational institutions. This system allows students to submit ratings and review comments for their courses and instructors in under a minute, completely anonymously.

The backend is built using **Python, Flask, SQLite, and TextBlob**, while the frontend provides a responsive and modern SaaS-style user experience.

---

## 🌟 Key Features

### 👨‍🎓 For Students

- 100% Anonymous Feedback Submission
- No Registration or Login Required
- Dynamic Subject & Teacher Selection
- Interactive Star Rating System
- Real-Time Character Counter
- Responsive and User-Friendly Interface

### 🤖 AI Sentiment Analysis Engine

- TextBlob NLP Integration
- Automatic Sentiment Classification
- Positive, Neutral, and Negative Detection
- Real-Time Feedback Analysis
- Graceful Fallback Handling

### 👨‍🏫 For Teachers

- Dedicated Teacher Dashboard
- Personal Performance Insights
- Average Rating Overview
- Sentiment Distribution Analysis
- Rating Distribution Statistics
- Recent Feedback Monitoring

### 👨‍💼 For Administrators

- Global Dashboard Overview
- Feedback Monitoring & Management
- Teacher Management (CRUD)
- Subject Management (CRUD)
- Subject–Teacher Mapping
- Admin Management
- System Analytics & Insights

### 🎨 UI/UX & Security Highlights

- Modern SaaS-Style Interface
- Responsive Layout Design
- Interactive Components & Animations
- Session-Based Authentication
- Role-Based Access Control
- Cache-Control Protection
- Input Validation & Formatting
- Anonymous Feedback Collection

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---------|---------|---------|
| Frontend | HTML5, CSS3, Vanilla JavaScript | User Interface & Interactions |
| Framework | Flask | Routing & Application Logic |
| Database | SQLite3 | Data Storage |
| AI/NLP | TextBlob | Sentiment Analysis |
| Icons | Lucide Icons, Font Awesome, Bootstrap Icons | UI Components |
| Styling | Custom SaaS Design System | Modern User Experience |

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
│   ├── js/
│   │   └── script.js
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

## 📊 Database Schema Design

The system uses a relational SQLite database consisting of the following tables:

### 1. Subjects

Stores subject information.

| Field |
|---------|
| subject_code (PK) |
| subject_name |

### 2. Teachers

Stores teacher account information.

| Field |
|---------|
| user_id (PK) |
| name |
| password |
| created_at |

### 3. Admins

Stores administrator account information.

| Field |
|---------|
| user_id (PK) |
| name |
| password |
| role |

### 4. Subject Teachers

Maps teachers to subjects.

| Field |
|---------|
| id (PK) |
| subject_code (FK) |
| teacher_user_id (FK) |

### 5. Feedbacks

Stores anonymous student feedback.

| Field |
|---------|
| id (PK) |
| subject_code (FK) |
| teacher_user_id (FK) |
| teaching_style_rating |
| subject_knowledge_rating |
| class_environment_rating |
| feedback_message |
| sentiment_label |
| created_at |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or above
- pip package manager

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd Student-Feedback-Review-System
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
```

#### 3. Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Run the Application

```bash
python app.py
```

#### 6. Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🔑 Default Credentials

### Administrator Accounts

| User ID | Role |
|---------|---------|
| A001 | Principal |
| A002 | HOD |
| A003 | TG |

### Teacher Accounts

| User ID | Teacher Name |
|---------|---------|
| T001 | Dr. Ramesh Sharma |
| T002 | Prof. Sunita Iyer |
| T003 | Dr. Arvind Kulkarni |
| T004 | Prof. Meena Nair |
| T005 | Dr. Suresh Pandey |
| T006 | Prof. Kavita Desai |
| T007 | Dr. Rajiv Bhatia |
| T008 | Dr. Neha Verma |

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
- Cache-Control Protection
- Parameterized SQLite Queries
- Anonymous Feedback Collection
- Input Validation & Sanitization

---

## 📈 Core Modules

### Student Module

- Anonymous Feedback Submission
- Subject & Teacher Selection
- Multi-Criteria Rating System
- Sentiment-Based Review Processing

### Teacher Module

- Personal Dashboard
- Performance Monitoring
- Rating Analysis
- Feedback Insights

### Admin Module

- Dashboard Overview
- Teacher Management
- Subject Management
- Subject Mapping
- Feedback Monitoring
- Analytics Dashboard
- Administrator Management

---

## 🎯 Project Highlights

- Anonymous Student Feedback Collection
- AI-Powered Sentiment Analysis
- Admin & Teacher Dashboards
- Subject & Teacher Management
- SQLite Database Integration
- Flask-Based Backend Architecture
- Responsive SaaS-Style User Interface
- Role-Based Authentication System
- Modern Analytics Dashboard
- Clean Modular Project Structure

---

## 📄 License

This project was developed for educational and academic purposes. It demonstrates web application development, database design, authentication systems, feedback analytics, and modern SaaS-style dashboard implementation using Flask and SQLite.
