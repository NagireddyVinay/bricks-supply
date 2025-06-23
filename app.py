from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'super_secret_key'

ADMIN_PASSWORD = 'admin123'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    message = request.form['message']

    with open('messages.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, message])

    return redirect('/contact')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid password"
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    messages = []
    try:
        with open('messages.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            messages = list(reader)
    except FileNotFoundError:
        pass

    return render_template('admin.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)