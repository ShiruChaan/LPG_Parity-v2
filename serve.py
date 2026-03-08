import os
from functools import wraps
from flask import Flask, send_from_directory, request, redirect, url_for, session, render_template_string

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

LOGIN_USERNAME = os.environ.get('LOGIN_USERNAME', 'admin')
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD', 'welovelpg')

LOGIN_PAGE = '''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LPG Parity - Login</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'IBM Plex Mono', monospace;
  background: #0a0e1a;
  color: #e2e8f0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-container {
  background: #0f172a;
  border: 1px solid #1e3a5f;
  border-radius: 12px;
  padding: 40px;
  width: 380px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.login-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  margin: 0 auto 20px;
}
h1 {
  font-size: 14px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: .06em;
  text-align: center;
  margin-bottom: 4px;
}
.subtitle {
  font-size: 10px;
  color: #475569;
  letter-spacing: .12em;
  text-align: center;
  margin-bottom: 28px;
}
label {
  font-size: 10px;
  color: #64748b;
  display: block;
  margin-bottom: 5px;
  letter-spacing: .08em;
}
input[type="text"], input[type="password"] {
  width: 100%;
  background: #111827;
  border: 1px solid #374151;
  color: #f3f4f6;
  padding: 10px 14px;
  border-radius: 6px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  margin-bottom: 16px;
  transition: border-color .2s;
}
input:focus {
  outline: none;
  border-color: #3b82f6;
}
button {
  width: 100%;
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  border: none;
  color: #fff;
  padding: 11px;
  border-radius: 6px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .08em;
  cursor: pointer;
  transition: opacity .2s;
}
button:hover { opacity: 0.9; }
.error {
  background: #1c0a0a;
  border: 1px solid #ef4444;
  color: #ef4444;
  font-size: 11px;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 16px;
  text-align: center;
}
</style>
</head>
<body>
<div class="login-container">
  <div class="login-icon">&#9981;</div>
  <h1>LPG PARITY SYSTEM</h1>
  <div class="subtitle">AUTHORIZED ACCESS ONLY</div>
  {% if error %}
  <div class="error">{{ error }}</div>
  {% endif %}
  <form method="POST">
    <label>USERNAME</label>
    <input type="text" name="username" autocomplete="username" required autofocus>
    <label>PASSWORD</label>
    <input type="password" name="password" autocomplete="current-password" required>
    <button type="submit">SIGN IN</button>
  </form>
</div>
</body>
</html>'''


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template_string(LOGIN_PAGE, error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return send_from_directory('.', 'lpg_price_parity.html')


@app.route('/calculator')
@login_required
def calculator():
    return send_from_directory('.', 'lpg_parity_calculator.html')


@app.route('/<path:filename>')
@login_required
def serve_file(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8765))
    app.run(host='0.0.0.0', port=port, debug=False)
