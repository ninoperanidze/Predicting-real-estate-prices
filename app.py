from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
pipeline = joblib.load('xgboost_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form
    area = float(request.form['area'])
    type_ = request.form['type']
    district = request.form['district']
    status = request.form['status']
    condition = request.form['condition']
    
    # Create a feature DataFrame in the same order as the training data
    features = pd.DataFrame([[area, type_, district, status, condition]], 
                            columns=['area', 'type', 'district', 'status', 'condition'])

    # Make prediction
    prediction = pipeline.predict(features)
    price_per_sqm = prediction[0]

    return render_template('index.html', prediction_text=f'Predicted Price per sqm: {price_per_sqm:.2f}')

if __name__ == '__main__':
    app.run(debug=True)