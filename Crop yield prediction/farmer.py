from flask import *

from database import *
from knn import newpredict_farmer_cropss

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


from knn import *

@farmer.route('/crop_rec', methods=['POST', 'GET'])
def crop_rec():
    if request.method == 'POST':
        try:
            # Get input parameters from form
            params = {
                'moisture': float(request.form['mois']),
                'ph': float(request.form['ph']),
                'nitrogen': float(request.form['nitro']),
                'phosphorus': float(request.form['phos']),
                'potassium': float(request.form['pot']),
                'humidity': float(request.form['hum']),  # Changed from 'humi' to 'hum' to match HTML
                'rainfall': float(request.form['rain'])  # Changed from 'rainfall' to 'rain' to match HTML
            }
            
            # Calculate crop parameter ranges
            crop_values = calculate_crop_ranges(params)
            
            # Get crop prediction
            result = newpredict_farmer_cropss(crop_values)
            
            # Prepare response
            response_data = {
                'result': result,
                'input_params': params
            }
            
            return render_template('F_crop_rec.html', result=result)
            
        except Exception as e:
            # Handle errors gracefully
            error_response = {
                'result': f"Error: {str(e)}",
                'input_params': {}
            }
            return render_template('crop_prediction.html', result=result)
    
    # If it's a GET request, just render the form
    return render_template('crop_prediction.html', result=[])

def calculate_crop_ranges(params):
    """Calculate the ranges for crop parameters based on input values."""
    crop_values = []
    
    # Moisture range (±10%)
    moisture_base = params['moisture'] * 10
    crop_values.extend([moisture_base, moisture_base + 10])
    
    # pH range (-2 to +4)
    crop_values.extend([params['ph'] - 2, params['ph'] + 4])
    
    # Nitrogen range (±1%)
    nitrogen_base = params['nitrogen'] / 100
    crop_values.extend([nitrogen_base - 1, nitrogen_base + 1])
    
    # Phosphorus range (±1%)
    phosphorus_base = params['phosphorus'] / 100
    crop_values.extend([phosphorus_base - 1, phosphorus_base + 1])
    
    # Potassium range (±1%)
    potassium_base = params['potassium'] / 100
    crop_values.extend([potassium_base - 1, potassium_base + 1])
    
    # Temperature range (fixed)
    crop_values.extend([20, 38])  # temp_low, temp_high
    
    return crop_values




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


