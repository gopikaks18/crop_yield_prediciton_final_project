from flask import *

from database import *
# from knn import newpredict_farmer_cropss

farmer = Blueprint('farmer',__name__)

@farmer.route('/farmer_home')
def farmer_home():
    return render_template("farmer_home.html")


@farmer.route('/add_complaint', methods=['get', 'post'])
def add_complaint():
    data = {}

    # Fetch complaints in descending order (latest first)
    qry = "SELECT * FROM complaint ORDER BY date DESC"
    res = select(qry)
    if res:
        data['view'] = res

    if 'add' in request.form:
        complaint = request.form['complaint']
        print(complaint)

        y = "INSERT INTO complaint VALUES (NULL, '%s', '%s', 'pending', CURDATE())" % (session['fam'], complaint)
        insert(y)

        return "<script>alert('Successfully added'); window.location='add_complaint'</script>"

    return render_template("add_complaint.html", data=data)



@farmer.route('/about')
def farmer_about():
    return render_template("about.html")


@farmer.route('/service')
def farmer_service():
    return render_template("service.html")

@farmer.route('/view_notification')
def view_notification():
    data={}
    qry = "SELECT * FROM notification"
    data['view'] = select(qry)
    return render_template('view_notification.html', data = data)


from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  

@farmer.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('public.login'))  


@farmer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authenticate user here
        session['user_id'] = user.id  # Set user session after successful login
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    return render_template('login.html')


################################################################################################


# from knn import *
from flask import render_template, request
import pandas as pd
import pickle
import numpy as np

@farmer.route('/crop_rec', methods=['POST', 'GET'])
def crop_rec():
    result = None  # Default result value
    
    if request.method == 'POST':
        # Get input values from the form
        state_name = request.form['state']
        district_name = request.form['district']
        crop_year = int(request.form['year'])
        season = request.form['season']
        crop = request.form['crop']
        area = float(request.form['area'])

        # Load the trained model, scaler, and label encoders
        with open('knn_crop_yield_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        with open('label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)

        # Create a DataFrame from user input
        new_data = pd.DataFrame({
            'State_Name': [state_name],
            'District_Name': [district_name],
            'Crop_Year': [crop_year],
            'Season': [season],
            'Crop': [crop],
            'Area': [area]
        })
        
        # Preprocess categorical values
        for col in ['State_Name', 'District_Name', 'Season', 'Crop']:
            if col in new_data.columns:
                le = label_encoders[col]
                new_data[col] = new_data[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
                if (new_data[col] == -1).any():
                    print(f"Warning: Unknown categories found in {col}")
        
        # Scale the input features
        X_new_scaled = scaler.transform(new_data[['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Area']])
        
        # Predict crop yield
        prediction = model.predict(X_new_scaled)
        result = f"Predicted Production: {prediction[0]:.2f}"
    
    return render_template('crop_prediction.html', result=result)



import textwrap
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from IPython.display import display, Markdown


# Google Gemini API Key
GOOGLE_API_KEY = 'AIzaSyC11_rV1NlFqnVZx9AQBzOqJYFSd3bGZ4k'
genai.configure(api_key=GOOGLE_API_KEY)

model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def to_markdown(text):
    text = text.replace('*', ' ')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate_gemini_response(prompt):
    # Generate a general response without specific focus on Ayurveda or medicinal plants
    response = model.generate_content(prompt)
    return response.text


@farmer.route('/chat_bot', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get('message')
        gemini_response = generate_gemini_response(user_message)
        return jsonify({'response': gemini_response})  # Return a JSON response
    return render_template("chat_bot.html")  # Render the chat page on GET request


