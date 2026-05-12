import sqlite3

def setup_database():
    conn = sqlite3.connect('school_ai.db')
    cursor = conn.cursor()

    cursor.executescript('''
        DROP TABLE IF EXISTS Tools;
        CREATE TABLE IF NOT EXISTS Tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            link TEXT,
            focus TEXT,
            min_age INTEGER,
            max_age INTEGER,
            grade_level INTEGER,
            req_tech TEXT,
            min_competency INTEGER
        );
    ''')

    tools_data = [
        ('Askie', 'https://askie.ai/', 'Math & Reading', 3, 4, 1, 'Tablet', 1),
        ('Khan Academy Kids', 'https://learn.khanacademy.org/khan-academy-kids/', 'Math & Reading', 3, 4, 1, 'Tablet', 1),
        ('Google Read Along', 'https://readalong.google.com/', 'Speech Confidence', 3, 8, 1, 'Tablet', 2),
        ('Arbitrator', 'https://arbitrator.ai/', 'Drawing & Creativity', 5, 6, 2, 'Tablet', 2),
        ('LittleLit', 'https://littlelit.app/', 'Storytelling', 5, 6, 2, 'Tablet', 3),
        ('AI Speak', 'https://aispeak.com/', 'Language Pronunciation', 7, 8, 3, 'Mobile', 3),
        ('Khanmigo', 'https://www.khanacademy.org/khanmigo', 'Academic Tutoring', 9, 10, 4, 'Laptop', 5),
        ('WordLab', 'https://wordlab.ai/', 'Vocabulary Building', 9, 10, 4, 'Web', 4),
        ('Teachable Machine', 'https://teachablemachine.withgoogle.com/', 'Science & Logic', 11, 12, 5, 'Laptop', 6),
        ('Canva Magic', 'https://www.canva.com/magic-home/', 'Design & Art', 11, 12, 5, 'Web', 5),
        ('KinderGPT', 'https://kindergpt.com/', 'Siri-like Q&A', 13, 14, 6, 'Web', 4),
        ('NotebookLM', 'https://notebooklm.google.com/', 'Research & Podcasts', 13, 16, 6, 'Laptop', 7),
        ('Wolfram Alpha', 'https://www.wolframalpha.com/', 'Complex Math & Science', 15, 16, 7, 'Laptop', 8)
    ]

    cursor.executemany('''
        INSERT INTO Tools (name, link, focus, min_age, max_age, grade_level, req_tech, min_competency) 
        VALUES (?,?,?,?,?,?,?,?)''', tools_data)
    
    conn.commit()
    return conn

def get_recommendation(conn, age, grade, tech, competency):
    cursor = conn.cursor()
    query = """
        SELECT name, focus, link, req_tech FROM Tools
        WHERE (? BETWEEN min_age AND max_age OR grade_level = ?)
        AND (req_tech = ? OR req_tech = 'Web')
        AND min_competency <= ?
    """
    cursor.execute(query, (age, grade, tech, competency))
    return cursor.fetchall()

if __name__ == "__main__":
    db_connection = setup_database()
    print("--- 🎓 Student AI Path Discovery ---")
    try:
        u_age = int(input("1. Enter Student Age: "))
        u_grade = int(input("2. Enter Grade Level (1-7): "))
        print("   Available Tech: Tablet, Mobile, Laptop")
        u_tech = input("3. What device do you use? ").strip().capitalize()
        u_comp = int(input("4. Tech Competency Score (1=Beginner, 10=Expert): "))

        results = get_recommendation(db_connection, u_age, u_grade, u_tech, u_comp)

        print(f"\n---  YOUR CUSTOM LEARNING PATH ---")
        if results:
            for name, focus, link, tech in set(results):
                print(f" {name.upper()}\n    Focus  : {focus}\n    Device : {tech}\n    Link   : {link}\n")
        else:
            print("No matching tools found.")
    except ValueError:
        print("Input Error: Please use numbers.")
    finally:
        db_connection.close()