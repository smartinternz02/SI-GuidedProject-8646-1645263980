import numpy as np
import pickle
import joblib
import matplotlib
import matplotlib.pyplot as plt
import time
import pandas
import os
from flask import Flask, request, jsonify, render_template
import json

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "urHgj6ezHeupOaICaGF1G1gNu-Uu4dQW1vQ2QZ0pjO4d"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8e16b491-9bb5-40c2-9ded-a3094b4de776/predictions?version=2021-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())


app = Flask(__name__)

scale = pickle.load(open('C:/Users/SmartbridgePC/Desktop/AIML/Guided projects/rainfall_prediction/IBM end point deploy/scale.pkl','rb'))

@app.route('/')# route to display the home page
def home():
    return render_template('index.html') #rendering the home page

@app.route('/predict',methods=["POST","GET"])# route to show the predictions in a web UI
def predict():
    #  reading the inputs given by the user
    Sex = request.form["Sex"]
    Maritalstatus = request.form["Maritalstatus"]
    Age = request.form["Age"]
    Education = request.form["Education"]
    Income = request.form["Income"]
    Occupation = request.form["Occupation"]
    Settlementsize = request.form["Settlementsize"]
    t = [[int(Sex),int(Maritalstatus),int(Age),int(Education),
          int(Income),int(Occupation),int(Settlementsize)]]
    payload_scoring = {"input_data": [{"field": [["Sex","Maritalstatus","Age","Education","Income","Occupation","Settlementsize"]], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8e16b491-9bb5-40c2-9ded-a3094b4de776/predictions?version=2021-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    return render_template('index.html',prediction_text = "The predicted customer belongs to the class" +str(pred))
     # showing the prediction results in a UI
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)