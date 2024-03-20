from fastapi import FastAPI
import uvicorn
import pickle

app = FastAPI(debug=True)

@app.get('/')
def home():
    return {"Welcome to Car Pricing Prediction"}

@app.get("/predict")
def predict(Year: str, Kms_Driven: str, Owner: str, 
            Fuel_Type_Diesel: str, Fuel_Type_Petrol: str,
            Seller_Type_Individual: str, Transmission_Manual: str):
    
    model = pickle.load(open('rf_model.pkl', 'rb'))
    pred = model.predict([[Year, Kms_Driven, Owner, Fuel_Type_Diesel, Fuel_Type_Petrol,
                          Seller_Type_Individual, Transmission_Manual]])
    output = round(pred[0],2)
    return f'You can sell your car for {output}'
    

if __name__ == '__main__':
    uvicorn.run(app)