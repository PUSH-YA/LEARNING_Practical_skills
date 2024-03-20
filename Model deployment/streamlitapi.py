import pickle
import streamlit as st
import os

model = pickle.load(open('rf_model.pkl', 'rb'))

def main():
    st.title('Car Pricing Prediction')

    Year =                      st.text_input("Year")
    Kms_Driven =                st.text_input("Kms_Driven")
    Owner =                     st.text_input("Owner")
    Fuel_Type_Diesel =          st.text_input("Fuel_Type_Diesel")
    Fuel_Type_Petrol =          st.text_input("Fuel_Type_Petrol")
    Seller_Type_Individual =    st.text_input("Seller_Type_Individual")
    Transmission_Manual =       st.text_input("Transmission_Manual")

    # prediction code
    if st.button('Predict'):
        pred = model.predict([[Year, Kms_Driven, Owner, Fuel_Type_Diesel, Fuel_Type_Petrol,
                          Seller_Type_Individual, Transmission_Manual]])
        output = round(pred[0],2)
        st.success(f'You can sell your car for {output}')

if __name__ == '__main__':
    main()

# can run it with streamlit run streamlitapi.py