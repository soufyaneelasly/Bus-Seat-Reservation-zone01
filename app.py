from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        chosen_time TEXT,
        chosen_place TEXT,
        chosen_seat TEXT,
        UNIQUE(chosen_time, chosen_place, chosen_seat)
    )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'username' in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chosen_place, chosen_time, chosen_seat FROM users
            WHERE username = ?
        ''', (session['username'],))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and user_data['chosen_place'] and user_data['chosen_time'] and user_data['chosen_seat']:
            return redirect(url_for('result'))

        return render_template('home.html')
    else:
        # return redirect(url_for('login'))
        return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('choose_time_place'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, hashed_password))
            conn.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
        finally:
            conn.close()
    return render_template('register.html')

# @app.route('/choose_time_place', methods=['GET', 'POST'])
# def choose_time_place():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         chosen_time = request.form['chosen_time']
#         chosen_place = request.form['chosen_place']
#         session['chosen_time'] = chosen_time
#         session['chosen_place'] = chosen_place
#         return redirect(url_for('choose_seat'))

#     available_times = {
#         'zone01': ['8:00', '10:00', '11:00'],
#         'bnidrar': ['9:30', '17:30'],
#         'babelgharbi': ['9:30', '11:30', '18:30', '19:30']
#     }
#     return render_template('choose_time_place.html', available_times=available_times)

 






@app.route('/choose_time_place', methods=['GET', 'POST'])
def choose_time_place():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    available_times = {
        "zone01": ["8:00", "10:00", "11:00"],
        "bnidrari": ["9:30", "17:30"],
        "babelgharbi": ["9:30", "11:30", "18:30", "19:30"]
    }

    if request.method == 'POST':
        chosen_place = request.form['chosen_place']
        chosen_time = request.form['chosen_time']
        session['chosen_place'] = chosen_place
        session['chosen_time'] = chosen_time

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET chosen_place = ?, chosen_time = ?
            WHERE username = ?
        ''', (chosen_place, chosen_time, session['username']))
        conn.commit()
        conn.close()

        return redirect(url_for('choose_seat'))
    
    return render_template('choose_time_place.html', available_times=available_times)





#######################################################################################3
# @app.route('/choose_seat', methods=['GET', 'POST'])
# def choose_seat():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     chosen_place = session.get('chosen_place')
#     chosen_time = session.get('chosen_time')

#     # Get all seats already taken for the chosen place and time
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT chosen_seat FROM users
#         WHERE chosen_place = ? AND chosen_time = ?
#     ''', (chosen_place, chosen_time))
#     taken_seats = [row['chosen_seat'] for row in cursor.fetchall()]
#     conn.close()

#     # Define available seats (1 through 20) and exclude taken seats
#     available_seats = [str(seat) for seat in range(1, 21) if str(seat) not in taken_seats]

#     if request.method == 'POST':
#         chosen_seat = request.form['chosen_seat']

#         if chosen_seat in available_seats:
#             # The seat is available, so update the user's reservation
#             conn = get_db()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 UPDATE users
#                 SET chosen_seat = ?, chosen_time = ?, chosen_place = ?
#                 WHERE username = ?
#             ''', (chosen_seat, chosen_time, chosen_place, session['username']))
#             conn.commit()
#             conn.close()
#             session['chosen_seat'] = chosen_seat
#             return redirect(url_for('result'))
#         else:
#             # Seat is already taken, show an error message
#             flash('The seat is already taken. Please choose another seat.')
#             return redirect(url_for('choose_seat'))

#     return render_template('choose_seat.html', available_seats=available_seats)
#######################################################################################

 
 





@app.route('/choose_seat', methods=['GET', 'POST'])
def choose_seat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        chosen_seat = request.form['chosen_seat']
        chosen_time = session.get('chosen_time')
        chosen_place = session.get('chosen_place')

        # Check if the seat is available
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM users
            WHERE chosen_time = ? AND chosen_place = ? AND chosen_seat = ?
        ''', (chosen_time, chosen_place, chosen_seat))
        count = cursor.fetchone()[0]

        if count == 0:
            # The seat is available, so update the user's reservation
            cursor.execute('''
                UPDATE users
                SET chosen_seat = ?, chosen_time = ?, chosen_place = ?
                WHERE username = ?
            ''', (chosen_seat, chosen_time, chosen_place, session['username']))
            conn.commit()
            conn.close()
            session['chosen_seat'] = chosen_seat
            return redirect(url_for('result'))
        else:
            # Seat is already taken, show an error message
            flash('The seat is already taken. Please choose another seat.')
            return redirect(url_for('choose_seat'))

    chosen_place = session.get('chosen_place')
    chosen_time = session.get('chosen_time')

    # Get all seats already taken for the chosen place and time
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT chosen_seat FROM users
        WHERE chosen_place = ? AND chosen_time = ?
    ''', (chosen_place, chosen_time))
    taken_seats = cursor.fetchall()

    # Debug print for taken seats
    print(f'Taken seats: {taken_seats}')

    # Convert taken seats to integers, if valid
    taken_seats = [int(row['chosen_seat']) for row in taken_seats if row['chosen_seat']]
    
    # Debug print for taken seats after conversion
    print(f'Taken seats (int): {taken_seats}')

    conn.close()

    # Define available seats (1 through 20) and exclude taken seats
    available_seats = [seat for seat in range(1, 21) if seat not in taken_seats]

    # Debug print for available seats
    print(f'Available seats: {available_seats}')

    return render_template('choose_seat.html', available_seats=available_seats, chosen_place=chosen_place, chosen_time=chosen_time)








@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))

    chosen_time = session.get('chosen_time')
    chosen_place = session.get('chosen_place')
    chosen_seat = session.get('chosen_seat')
    return render_template('result.html', chosen_time=chosen_time, chosen_place=chosen_place, chosen_seat=chosen_seat)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('chosen_time', None)
    session.pop('chosen_place', None)
    session.pop('chosen_seat', None)
    return redirect(url_for('home'))






if __name__ == '__main__':
    init_db()
    app.run(debug=True)
