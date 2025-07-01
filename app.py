from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
INQUIRIES_FILE = 'inquiries.json'
USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_inquiries():
    if not os.path.exists(INQUIRIES_FILE):
        return []
    with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_inquiries(inquiries):
    with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(inquiries, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'full_name': request.form['full_name'],
            'civil_id': request.form['civil_id'],
            'email': request.form['email'],
            'sector': request.form['sector'],
            'phone': request.form['phone'],
            'password': request.form['password']
        }
        users = load_users()
        if data['civil_id'] in users:
            flash('المستخدم مسجل بالفعل')
        else:
            users[data['civil_id']] = data
            save_users(users)
            flash('تم التسجيل بنجاح، يمكنك الآن تسجيل الدخول')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        civil_id = request.form['civil_id']
        password = request.form['password']

        # تحقق من الأدمن
        if civil_id == '123456789' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))

        users = load_users()
        if civil_id in users and users[civil_id]['password'] == password:
            session['user'] = civil_id
            return redirect(url_for('user_home'))

        flash('بيانات الدخول غير صحيحة')
    return render_template('login.html')

@app.route('/user_home')
def user_home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('user_home.html')

@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    if 'user' not in session:
        return redirect(url_for('login'))

    subject = request.form['subject']
    message = request.form['message']
    uploaded_file = request.files['file']
    filename = ""

    if uploaded_file and uploaded_file.filename:
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

    new_inquiry = {
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'user': session['user'],
        'subject': subject,
        'message': message,
        'file': filename,
        'reply': '',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    inquiries = load_inquiries()
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)
    flash('تم إرسال الاستشارة بنجاح')
    return redirect(url_for('user_home'))

@app.route('/my_inquiries')
def my_inquiries():
    if 'user' not in session:
        return redirect(url_for('login'))
    all_inquiries = load_inquiries()
    my_inq = [inq for inq in all_inquiries if inq['user'] == session['user']]
    return render_template('my_inquiries.html', inquiries=my_inq)

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))

    inquiries = load_inquiries()
    users = load_users()
    return render_template('admin_dashboard.html', inquiries=inquiries, users=users)

@app.route('/reply/<inq_id>', methods=['POST'])
def reply(inq_id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    reply_text = request.form['reply']
    inquiries = load_inquiries()

    for inquiry in inquiries:
        if inquiry['id'] == inq_id:
            inquiry['reply'] = reply_text
            break

    save_inquiries(inquiries)
    flash('تم إرسال الرد')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("✅ التطبيق يعمل - افتح المتصفح على http://127.0.0.1:5000")
    app.run(debug=True)
