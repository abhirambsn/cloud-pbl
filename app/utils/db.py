import psycopg2
import os

def init_db():
    print("Starting DB Connection")
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=4510,
        database="file_manager",
        user="admin",
        password="password"
    )
    print("Connected to RDS")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(200) NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_username(username):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=4510,
        database="file_manager",
        user="admin",
        password="password"
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return {'username': user[1], 'password': user[2]} if user else None

def add_user(username, password):
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=4510,
        database="file_manager",
        user="admin",
        password="password"
    )
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    conn.commit()
    cur.close()
    conn.close()
