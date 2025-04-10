from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import os  # This is important for accessing the dynamic port

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        if airline == 'Jet Airways':
            Jet_Airways = 1
            IndiGo = Air_India = Multiple_carriers = SpiceJet = Vistara = GoAir = Multiple_carriers_Premium_economy = Jet_Airways_Business = Vistara_Premium_economy = Trujet = 0
        elif airline == 'IndiGo':
            Jet_Airways = IndiGo = 1
            Air_India = Multiple_carriers = SpiceJet = Vistara = GoAir = Multiple_carriers_Premium_economy = Jet_Airways_Business = Vistara_Premium_economy = Trujet = 0
        # Handle other airlines similarly...

        # Source
        Source = request.form["Source"]
        if Source == 'Delhi':
            s_Delhi, s_Kolkata, s_Mumbai, s_Chennai = 1, 0, 0, 0
        elif Source == 'Kolkata':
            s_Delhi, s_Kolkata, s_Mumbai, s_Chennai = 0, 1, 0, 0
        # Handle other sources similarly...

        # Destination
        Destination = request.form["Destination"]
        if Destination == 'Cochin':
            d_Cochin, d_Delhi, d_New_Delhi, d_Hyderabad, d_Kolkata = 1, 0, 0, 0, 0
        elif Destination == 'Delhi':
            d_Cochin, d_Delhi, d_New_Delhi, d_Hyderabad, d_Kolkata = 0, 1, 0, 0, 0
        # Handle other destinations similarly...

        # Prepare the input data for prediction
        d = [
            Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min,
            dur_hour, dur_min, Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers,
            Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara, Vistara_Premium_economy, s_Chennai,
            s_Delhi, s_Kolkata, s_Mumbai, d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi
        ]
        
        prediction = model.predict([d])
        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("index.html")

if __name__ == "__main__":
    # Get the port from the environment (Render sets the port dynamically)
    port = int(os.environ.get("PORT", 5000))  # Defaults to 5000 if not set

    # Run the app on all available IP addresses (0.0.0.0) and the correct port
    app.run(host="0.0.0.0", port=port, use_reloader=False)
