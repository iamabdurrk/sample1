import sqlite3

DATABASE_FILE = 'users.db'

def create_connection():
    return sqlite3.connect(DATABASE_FILE)

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_email TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    conn.commit()
    conn.close()


def get_user_by_id(user_id):
    """Fetch user details from the database by user ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {'username': user[0], 'email': user[1]}
    return None

def update_user_profile(user_id, new_username=None, new_password=None):
    """Update user profile information in the database."""
    conn = create_connection()
    cursor = conn.cursor()

    sql = "UPDATE users SET "
    updates = []
    params = []

    if new_username:
        updates.append("username = ?")
        params.append(new_username)

    if new_password:
        updates.append("password = ?")
        params.append(new_password)

    sql += ", ".join(updates) + " WHERE id = ?"
    params.append(user_id)

    cursor.execute(sql, tuple(params))
    conn.commit()
    conn.close()
def get_user_by_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
   
    cursor.execute("SELECT id, username, email, password FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def delete_note_from_db(note_id):
    """Delete a note from the database."""
    conn = create_connection()
    cursor = conn.cursor()

    
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (note_id,))
    print(cursor.fetchall())
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    cursor.execute('SELECT * FROM users WHERE id = ?', (note_id,))
    print(cursor.fetchall())
    conn.commit()
    conn.close()
def add_user(username, email, password):
    init_db()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def get_user_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_note_for_user(title, content, user_email):
    init_db()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (title, content, user_email) VALUES (?, ?, ?)', (title, content, user_email))
    conn.commit()
    conn.close()

def get_notes_from_db(user_email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE user_email = ?', (user_email,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def check_email_in_notes(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM notes WHERE user_email = ? LIMIT 1', (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def delete_note(note_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()

def get_note_by_id(note_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note

def update_note(note_id, title, content):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE notes SET title = ?, content = ? WHERE id = ?', (title, content, note_id))
    conn.commit()
    conn.close()
