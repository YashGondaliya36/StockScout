import streamlit as st
import pandas as pd
import plotly.express as px
from src.StockScout.pipeline.prediction import PredictionPipeline
import yaml
import os
import subprocess

def update_config(ticker):
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    config['data_ingestion']['ticker'] = ticker
    
    with open('config/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def main():
    st.title("Stock Price Prediction")
    
    ticker = st.text_input("Enter Stock Symbol (e.g., AAPL):", "AAPL")
    days = st.number_input("Number of days to predict:", min_value=1, value=7)
    
    if st.button("Predict"):
        with st.spinner("Training model..."):
            update_config(ticker)
            subprocess.run(["python", "main.py"])
            
            predictor = PredictionPipeline()
            predictions = predictor.Predict(days)
            
            dates = pd.date_range(start=pd.Timestamp.today(), periods=days).date
            df_predictions = pd.DataFrame({
                'Date': dates,
                'Predicted Price': predictions.flatten()
            })

            # Plot using Plotly Express
            fig = px.line(df_predictions, x='Date', y='Predicted Price', 
                          title=f"{ticker} Stock Price Prediction",
                          markers=True)

            st.plotly_chart(fig)

            # Display predictions
            st.subheader("Predicted Prices")
            st.dataframe(df_predictions)

if __name__ == "__main__":
    main()
