from flask import Flask, render_template, request, redirect, url_for, session
from database import add_user, get_user_by_email, get_user_by_id, add_note_for_user, get_notes_from_db, check_email_in_notes, delete_note, get_note_by_id, update_note, delete_note_from_db

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)

        if user is None:
            error = "User not found."
            return render_template('user_not_found.html', error=error)

        if user[3] == password:  
            session['email'] = email
            session['user_id'] = user[0] 
            username = email.split('@')[0]

            if check_email_in_notes(email):
                notes = get_notes_from_db(email)
                return render_template('dashboard.html', notes=notes, username=username, email=email)
            else:
                return render_template('dashboard.html', username=username, email=email)
        else:
            error = "Invalid password."
            return render_template('login.html', error=error)

    return render_template('login.html')
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id')  
    if not user_id:
        return redirect(url_for('home'))  

    user = get_user_by_id(user_id) 

    if user:
        username = user['username'] 
        email = user['email']  
        password = user['password'] 
        
        return render_template('profile.html', username=username, email=email, password=password)
    
    return "User not found", 404

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = email.split('@')[0]

        if add_user(username, email, password):
            return render_template('dashboard.html', username=username, email=email)
        else:
            return render_template('email_exist.html')

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    if not email:
        return redirect(url_for('home'))

    username = email.split('@')[0]
    notes = get_notes_from_db(email)
    return render_template('dashboard.html', notes=notes, username=username, email=email)

@app.route('/create-note', methods=['POST'])
def create_note():
    title = request.form['title']
    content = request.form['content']
    email = session.get('email')

    if not email:
        return redirect(url_for('home'))

    add_note_for_user(title, content, email)
    return redirect(url_for('dashboard'))

@app.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note_route(note_id):
    delete_note_from_db(note_id)
    return redirect(url_for('dashboard'))

@app.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
def edit_note_route(note_id):
    note = get_note_by_id(note_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        update_note(note_id, title, content)
        return redirect(url_for('dashboard'))

    return render_template('edit_note.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)
