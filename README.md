# Student Feedback Review System

A web-based feedback management system that allows students to submit anonymous feedback for subjects and teachers. The system uses sentiment analysis to classify feedback and provides separate dashboards for teachers and administrators to review insights and manage records.

## Features

### Student Module
- Anonymous feedback submission
- Subject-wise teacher selection
- Star rating system (1–5)
- Feedback comments with character limit

### Sentiment Analysis
- Automatic feedback analysis using TextBlob
- Classifies reviews as Positive, Neutral, or Negative

### Teacher Module
- Personal dashboard
- Average rating and feedback statistics
- Sentiment overview
- View received feedback

### Admin Module
- Manage teachers and subjects
- View and manage feedback records
- Dashboard with overall statistics
- Create and manage admin accounts

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Backend:** Python, Flask
- **Database:** SQLite
- **Sentiment Analysis:** TextBlob

## Project Structure

```text
Student Feedback Review System/
│
├── app.py
├── database.py
├── requirements.txt
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
│   └── js/
│
└── templates/
    ├── admin/
    └── teacher/
```

## Database

The system uses SQLite and consists of the following main tables:

- Subjects
- Teachers
- Subject Teachers
- Feedback
- System Flags

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd "Student Feedback Review System"
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Default Login Credentials

### Admin

```text
User ID: ADM001
Password: 123456
```

### Teacher

```text
User ID: TCH001
Password: 123456
```

## Future Enhancements

- Advanced analytics dashboard
- Feedback report export
- Email notifications
- Enhanced sentiment analysis

## License

This project was developed as a minor academic project for educational purposes.
