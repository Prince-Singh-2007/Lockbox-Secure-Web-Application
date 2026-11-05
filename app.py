import os, secrets, sqlite3
from pathlib import Path
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort
from werkzeug.security import generate_password_hash, check_password_hash

DB = Path(__file__).with_name('users.db')
app = Flask(__name__)
app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32), SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE') == '1', PERMANENT_SESSION_LIFETIME=1800, MAX_CONTENT_LENGTH=16384)

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB); g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc=None):
    conn = g.pop('db', None)
    if conn: conn.close()

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

@app.before_request
def csrf_guard():
    if 'csrf' not in session: session['csrf'] = secrets.token_urlsafe(32)
    if request.method == 'POST':
        token = request.form.get('csrf', '')
        if not token or not secrets.compare_digest(token, session.get('csrf', '')): abort(400, 'Invalid or missing CSRF token.')

@app.after_request
def headers(resp):
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    resp.headers['Cache-Control'] = 'no-store'
    return resp

def protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'uid' not in session:
            flash('Please log in to view the dashboard.', 'info'); return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

def valid_password(p):
    return len(p) >= 10 and any(c.islower() for c in p) and any(c.isupper() for c in p) and any(c.isdigit() for c in p) and any(not c.isalnum() for c in p)

@app.route('/')
def home(): return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u, p = request.form.get('username','').strip(), request.form.get('password','')
        if not (3 <= len(u) <= 30 and u.replace('_','').isalnum()):
            flash('Username must be 3–30 letters, numbers or underscores.', 'error')
        elif not valid_password(p):
            flash('Use at least 10 characters with uppercase, lowercase, a number and a symbol.', 'error')
        else:
            try:
                db().execute('INSERT INTO users(username,password_hash) VALUES (?,?)', (u, generate_password_hash(p, method='scrypt'))); db().commit()
                flash('Account created. Please sign in.', 'success'); return redirect(url_for('login'))
            except sqlite3.IntegrityError: flash('That username is already taken.', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u, p = request.form.get('username','').strip(), request.form.get('password','')
        row = db().execute('SELECT id, username, password_hash FROM users WHERE username = ?', (u,)).fetchone()
        if row and check_password_hash(row['password_hash'], p):
            session.clear(); session['uid'] = row['id']; session['username'] = row['username']; session['csrf'] = secrets.token_urlsafe(32); session.permanent = True
            flash('Signed in successfully.', 'success'); return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
@protected
def dashboard(): return render_template('dashboard.html', username=session.get('username','User'))

@app.route('/logout', methods=['POST'])
@protected
def logout(): session.clear(); flash('You have been logged out.', 'success'); return redirect(url_for('home'))

@app.errorhandler(400)
def bad_request(e): return render_template('error.html', message=getattr(e,'description','Bad request')), 400

if __name__ == '__main__':
    init_db(); app.run(host='127.0.0.1', port=5000, debug=False)
