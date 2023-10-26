from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import csv
import os
import re
from urllib.parse import quote, unquote
import plotly.express as px
import pandas as pd

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with a secret key for sessions
app.config['static'] = 'static/Image'

# Function to read user data to the text file


def read_user_data():
    user_data = {}
    with open('users.txt', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            user_data[row[0]] = row[1]
    return user_data

# Function to write user data to the text file


def write_user_data(user_data):
    with open('users.txt', mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, password in user_data.items():
            writer.writerow([username, password])


# Replace with the actual file path
log_file_path = 'user_logins.txt'
with open(log_file_path, 'a') as log_file:
    pass  # This will create the file if it doesn't exist

# Function to log user logins


def log_login(username, action):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Replace with the actual file path
    log_file_path = 'user_logins.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'User: {username}, {action} Time: {current_time}\n')

# Index Route


@app.route('/')
def index():
    username = session.get('username')
    if 'username' not in session:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    fir_data = [
        {
            "Crime Category": "Malware",
            "Crime Sub-Category": "Hacking",
            # Add more data attributes as needed
        },
        # Add more data entries as needed
    ]

    # Generate the chart HTML
    chart_html = generate_crime_category_chart(fir_data)

    # User is logged in, you can render the main page
    return render_template('index.html', username=username, chart_html=chart_html)


# Login Route


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_successful = True  # Initialize as True by default

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = read_user_data()

        if username in user_data and user_data[username] == password:
            # Log the user login
            log_login(username, 'Login')

            # Set the user's session
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # If the username and password are incorrect, set login_successful to False
            login_successful = False

    return render_template('index.html', login_successful=login_successful)


# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    username = session.get('username')
    session.pop('username', None)
    if username:
        # Log the user logout
        log_login(username, 'Logout')
    return redirect(url_for('index'))


# Create new users
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST' and ('username' in session and session['username'] == 'admin'):
        new_username = request.form['username']
        new_password = request.form['password']
        user_data = read_user_data()
        user_data[new_username] = new_password
        write_user_data(user_data)
        return redirect(url_for('index'))
    return render_template('create_user.html')

# Add crime report


@app.route('/crime_report', methods=['GET', 'POST'])
def crime_report():
    return render_template('crime_report.html')

# Add criminal report


@app.route('/criminal_report', methods=['GET', 'POST'])
def criminal_report():
    return render_template('criminal_report.html')

# Submit Request


@app.route('/submit', methods=['POST'])
def submit():

    folder_name = request.form.get('folder_name')
    if folder_name is None:
        return "Folder created successfully."
    folder_name = folder_name.replace('/', '_')

    # Retrieve data from the form
    folder_name = request.form.get('folder_name').replace('/', '_')
    fir_no = request.form.get('fir_no')
    fir_date = request.form.get('fir_date')
    incident_date = request.form.get('incident_date')
    incident_time = request.form.get('incident_time')
    state_territory = request.form.get('state_territory')
    district = request.form.get('district')
    police_station = request.form.get('police_station')
    suspect_name = request.form.get('suspect_name')
    suspect_name_alias = request.form.get('suspect_name_alias')
    crime_type = request.form.get('crime_type')
    crime_sub_type = request.form.get('crime_sub_type')
    crime_place = request.form.get('crime_place')
    crime_state = request.form.get('crime_state')
    suspect_phone = request.form.get('suspect_phone')
    suspect_imei = request.form.get('suspect_imei')
    suspect_bank_name = request.form.get('suspect_bank_name')
    suspect_bank_ifsc = request.form.get('suspect_bank_ifsc')
    bank_branch = request.form.get('bank_branch')
    bank_city = request.form.get('bank_city')
    bank_state = request.form.get('bank_state')
    account_number = request.form.get('account_number')
    account_name = request.form.get('account_name')
    crypto_account_number = request.form.get('crypto_account_number')
    crypto_account_name = request.form.get('crypto_account_name')
    description = request.form.get('description')
    suspect_upload = request.form.get('suspect_upload')
    # Add more form fields as needed

    # Replace the underscore with a slash for display purposes
    folder_display_name = folder_name.replace('_', '/')

    # 'data' is the directory where folders will be stored
    folder_path = os.path.join('data', folder_name)

    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create a file inside the folder and write the input data to it
        file_path = os.path.join(folder_path, 'data.txt')
        with open(file_path, 'w') as file:
            file.write(f"FIR Number: {fir_no}\n")
            file.write(f"FIR Date: {fir_date}\n")
            file.write(f"Incident Date: {incident_date}\n")
            file.write(f"Incident Time: {incident_time}\n")
            file.write(f"State / Territory: {state_territory}\n")
            file.write(f"District : {district}\n")
            file.write(f"Police station : {police_station}\n")
            file.write("\nSUSPECT DETAILS:-\n")
            file.write(f"Suspect Name: {suspect_name}\n")
            file.write(f"Suspect Alias Name: {suspect_name_alias}\n")
            file.write(f"Suspect Phone Number: {suspect_phone}\n")
            file.write(f"Suspect IMEI Number: {suspect_imei}\n")
            file.write(f"Crime Category: {crime_type}\n")
            file.write(f"Crime sub-Category: {crime_sub_type}\n")
            file.write(f"Crime Place: {crime_place}\n")
            file.write(f"Crime State: {crime_state}\n")
            file.write("\nBANKING DETAILS:-\n")
            file.write(f"Bank Name: {suspect_bank_name}\n")
            file.write(f"Bank IFSC Number: {suspect_bank_ifsc}\n")
            file.write(f"Bank Branch: {bank_branch}\n")
            file.write(f"Bank City: {bank_city}\n")
            file.write(f"Bank State: {bank_state}\n")
            file.write(f"Account Number: {account_number}\n")
            file.write(f"Account Holder's Name: {account_name}\n")
            file.write(f"Crypto Account Number: {crypto_account_number}\n")
            file.write(f"Crypto Account Name: {crypto_account_name}\n")
            file.write("\nADDITIONAL DETAILS:-\n")
            file.write(f"Description : {description}\n")
            file.write(f"suspect_upload : {suspect_upload}\n")

        # Create a DataFrame for each field
        phone_data = {
            "Suspect Phone Number": [suspect_phone]
        }
        df_phone = pd.DataFrame(phone_data)

        account_data = {
            "Account Number": [account_number]
        }
        df_account = pd.DataFrame(account_data)

        imei_data = {
            "Suspect IMEI Number": [suspect_imei]
        }
        df_imei = pd.DataFrame(imei_data)

        # Define the file paths for each Excel file
        phone_file_path = os.path.join(folder_path, 'phone_data.xlsx')
        account_file_path = os.path.join(folder_path, 'account_data.xlsx')
        imei_file_path = os.path.join(folder_path, 'imei_data.xlsx')

        # Write each DataFrame to its respective Excel file
        df_phone.to_excel(phone_file_path, index=False)
        df_account.to_excel(account_file_path, index=False)
        df_imei.to_excel(imei_file_path, index=False)

        # return render_template('crime_report.html')
        return f"Form submitted successfully. Folder Name: {folder_display_name}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def format_folder_name(name):
    # Replace spaces with underscores and make it lowercase
    return name.replace(' ', '_').lower()


@app.route('/submit_criminal', methods=['POST'])
def submit_criminal():
    try:
        # Retrieve data from the form
        name = request.form.get('criminal-name')
        alias = request.form.get('criminal-name-alias')
        fh_name = request.form.get('criminal-fh-name')
        dob = request.form.get('criminal-dob')
        age = request.form.get('criminal-age')
        occupation = request.form.get('criminal-occupation')
        gender = request.form.get('criminal-gender')
        criminal_adhar = request.form.get('criminal_adhar')
        criminal_voterid = request.form.get('criminal_voterid')
        criminal_dl = request.form.get('criminal_dl')
        criminal_passport = request.form.get('criminal_passport')

        # Create a folder with the name as the Full Name (with spaces replaced by underscores)
        folder_name = format_folder_name(name)
        folder_path = os.path.join('criminal_data', folder_name)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Store the information in a text file
        file_path = os.path.join(folder_path, 'criminal_data.txt')
        with open(file_path, 'w') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Alias Name: {alias}\n")
            file.write(f"Father/Husband Name: {fh_name}\n")
            file.write(f"Date of Birth: {dob}\n")
            file.write(f"Age: {age}\n")
            file.write(f"Occupation: {occupation}\n")
            file.write(f"Gender: {gender}\n")
            file.write(f"Criminal Adhar: {criminal_adhar}\n")
            file.write(f"Criminal Voter ID: {criminal_voterid}\n")
            file.write(f"Criminal Driving License: {criminal_dl}\n")
            file.write(f"Criminal Passport: {criminal_passport}\n")

        if photo := request.files['photo']:
            image_path = os.path.join(folder_path, 'photo.jpg')
            photo.save(image_path)

        # return render_template('criminal_report.html')
        return f"Form submitted successfully. Folder Name: {name}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/folders')
def folders():
    data_folder = 'data'
    folder_list = sorted(os.listdir(data_folder),
                         key=lambda folder: int(folder))

    return render_template('folders.html', folders=folder_list)


@app.route('/folders/<folder_name>')
def folder_contents(folder_name):
    folder_path = os.path.join('data', folder_name)
    data_file = os.path.join(folder_path, 'data.txt')
    image_file = os.path.join(folder_path, 'photo.jpg')

    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            folder_data = file.read()
    else:
        folder_data = "Data not found."

    return render_template('folder_contents.html', folder_name=folder_name, folder_data=folder_data)


def generate_crime_category_chart(data):
    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create a bar chart using Plotly Express
    fig = px.bar(df, x="Crime Category", title="Crime Categories")

    return fig.to_html(full_html=False)


if __name__ == '__main__':
    app.run(debug=True)
