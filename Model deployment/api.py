from flask import Flask, json, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('rf_model.pkl', 'rb'))

@app.route('/')
def home():
    return "Welcome to Car Pricing Prediction"

@app.route("/predict", methods = ["GET"])
def predict():
    Year =                      request.args.get("Year")
    Kms_Driven =                request.args.get("Kms_Driven")
    Owner =                     request.args.get("Owner")
    Fuel_Type_Diesel =          request.args.get("Fuel_Type_Diesel")
    Fuel_Type_Petrol =          request.args.get("Fuel_Type_Petrol")
    Seller_Type_Individual =    request.args.get("Seller_Type_Individual")
    Transmission_Manual =       request.args.get("Transmission_Manual")

    pred = model.predict([Year, Kms_Driven, Owner, Fuel_Type_Diesel, Fuel_Type_Petrol,
                          Seller_Type_Individual, Transmission_Manual])

    output = round(pred[0],2)
    return f'You can sell your car for {output}'