import json
from flask import Flask, render_template, request, redirect, url_for

# Flask app banayein
app = Flask(__name__)

# Data file ka naam
FILE_NAME = "data.json"

def load_data():
    """File se purana data load karne ki koshish karta hai."""
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Naye data ko file mein save karta hai."""
    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=4)

# Main page (Home Page) ke liye route
@app.route('/')
def index():
    # Data load karo aur use HTML page par bhejo
    all_data = load_data()
    return render_template('index.html', data=all_data)

# Data add karne ke liye route (yeh form submission ko handle karega)
@app.route('/add', methods=['POST'])
def add_entry():
    # Form se data nikalo
    name = request.form['name']
    age_str = request.form['age']
    rs_str = request.form['rs']
    code = request.form['code']

    try:
        # Purana data load karo
        all_data = load_data()
        
        # Nayi entry banao
        new_entry = {
            "name": name,
            "age": int(age_str),
            "RS": int(rs_str),
            "unique_code": code
        }
        
        # Nayi entry ko jodo aur save karo
        all_data.append(new_entry)
        save_data(all_data)
        
    except ValueError:
        # Agar age ya rs number nahi hai to error handle karo (filhal ignore)
        print("Invalid number format.")

    # Data add hone ke baad wapas main page par bhej do
    return redirect(url_for('index'))

# Program chalaane ke liye
if __name__ == '__main__':
    app.run(debug=True)
