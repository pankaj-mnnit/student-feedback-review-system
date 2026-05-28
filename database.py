import sqlite3

DATABASE_FILE = 'feedback_system.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_code TEXT PRIMARY KEY,
            subject_name TEXT NOT NULL
        )
    ''')

    # 2. teachers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            admin TEXT DEFAULT 'no'
        )
    ''')
    
    # Try to drop the legacy teacher column from subjects table if it exists
    try:
        cursor.execute("ALTER TABLE subjects DROP COLUMN teacher")
    except sqlite3.OperationalError:
        pass

    # 3. subject_teachers table (for many-to-many relationship)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_teachers (
            subject_code TEXT,
            teacher_id TEXT,
            FOREIGN KEY(subject_code) REFERENCES subjects(subject_code) ON DELETE CASCADE,
            FOREIGN KEY(teacher_id) REFERENCES teachers(user_id) ON DELETE CASCADE,
            PRIMARY KEY(subject_code, teacher_id)
        )
    ''')

    # 4. feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            teacher TEXT NOT NULL,
            rating_star INTEGER NOT NULL,
            feedback_comment TEXT NOT NULL,
            sentiment_analysis TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (subject) REFERENCES subjects(subject_code),
            FOREIGN KEY (teacher) REFERENCES teachers(user_id)
        )
    ''')

    # 5. system_flags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_flags (
            flag_name TEXT PRIMARY KEY,
            flag_value TEXT
        )
    ''')

    # Check if database schema is already seeded
    cursor.execute("SELECT flag_value FROM system_flags WHERE flag_name = 'db_seeded'")
    row = cursor.fetchone()
    if row and row['flag_value'] == 'yes':
        conn.close()
        return

    # Remove old demo records if they exist
    demo_ids = ['t001', 't002', 'admin']
    for did in demo_ids:
        cursor.execute("DELETE FROM teachers WHERE user_id = ?", (did,))
        
    # Remove old demo records from subjects if they exist
    demo_subjects = ['CS101', 'MA101', 'EN101']
    for sub_code in demo_subjects:
        cursor.execute("DELETE FROM subjects WHERE subject_code = ?", (sub_code,))

    # Insert or update actual teacher/admin records
    actual_teachers = [
        ('TCH001', 'Mr. Manoj Kumar', '123456', 'no'),
        ('TCH002', 'Mr. Nitesh Gupta', '123456', 'no'),
        ('TCH003', 'Neelam Bisen', '123456', 'no'),
        ('TCH004', 'Pranjali Pachpor', '123456', 'no'),
        ('ADM001', 'Anurag Shrivastva', '123456', 'yes')
    ]
    
    for uid, name, pwd, adm in actual_teachers:
        cursor.execute("SELECT * FROM teachers WHERE user_id = ?", (uid,))
        if cursor.fetchone():
            cursor.execute("UPDATE teachers SET name = ? WHERE user_id = ?", (name, uid))
        else:
            cursor.execute("INSERT INTO teachers (user_id, name, password, admin) VALUES (?, ?, ?, ?)", (uid, name, pwd, adm))

    # Insert or update actual subject records
    actual_subjects = [
        ('AL 601', 'Theory of Computation', 'TCH001'),
        ('AL 602', 'Computer Networks', 'TCH002'),
        ('AL 603', 'Data and Visual Analytics', 'TCH003'),
        ('AL 604', 'Cloud Computing', 'TCH004')
    ]
    for code, name, teacher_id in actual_subjects:
        cursor.execute("SELECT * FROM subjects WHERE subject_code = ?", (code,))
        if cursor.fetchone():
            cursor.execute("UPDATE subjects SET subject_name = ? WHERE subject_code = ?", (name, code))
        else:
            cursor.execute("INSERT INTO subjects (subject_code, subject_name) VALUES (?, ?)", (code, name))
        
        # Seed the subject_teachers mapping
        cursor.execute("SELECT * FROM subject_teachers WHERE subject_code = ? AND teacher_id = ?", (code, teacher_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO subject_teachers (subject_code, teacher_id) VALUES (?, ?)", (code, teacher_id))

    # Seed extra subject-teacher mappings for TCH001 to teach multiple subjects
    extra_mappings = [
        ('AL 602', 'TCH001'),
        ('AL 603', 'TCH001')
    ]
    for code, teacher_id in extra_mappings:
        cursor.execute("SELECT * FROM subject_teachers WHERE subject_code = ? AND teacher_id = ?", (code, teacher_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO subject_teachers (subject_code, teacher_id) VALUES (?, ?)", (code, teacher_id))

    # Mark database as successfully seeded
    cursor.execute("INSERT OR REPLACE INTO system_flags (flag_name, flag_value) VALUES ('db_seeded', 'yes')")
    conn.commit()
    conn.close()
