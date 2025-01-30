import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import yaml

def load_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window=20):
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * 2)
    lower_band = rolling_mean - (rolling_std * 2)
    return upper_band, lower_band

def load_ticker_from_config():
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['data_ingestion']['ticker']

def main():
    st.title("Technical Indicators Analysis")
    
    # Ask user for time period for analysis
    time_period = st.selectbox("Select the time period for analysis:", ['1d', '5d', '1mo', '3mo', '1y', '5y'])
    
    # Load ticker from config.yaml
    ticker = load_ticker_from_config()
    st.write(f"Analyzing technical indicators for: **{ticker}** for the past {time_period}")
    
    # Load stock data
    data = load_stock_data(ticker, period=time_period)
    
    # Moving Averages
    st.header("Moving Averages")
    ma_window = st.slider("Select Moving Average Window:", min_value=5, max_value=100, value=20)
    data['MA'] = calculate_moving_average(data, ma_window)
    
    # Plot Moving Averages using Plotly Express
    fig_ma = px.line(data, x=data.index, y=['Close', 'MA'], labels={'value': 'Price', 'variable': 'Line'})
    fig_ma.update_layout(title=f"{ticker} Moving Average", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig_ma, use_container_width=True)

    # RSI
    st.header("Relative Strength Index (RSI)")
    rsi_window = st.slider("Select RSI Window:", min_value=5, max_value=30, value=14)
    data['RSI'] = calculate_rsi(data, rsi_window)
    
    # Plot RSI using Plotly Express
    fig_rsi = px.line(data, x=data.index, y='RSI', labels={'value': 'RSI'})
    fig_rsi.add_hline(y=70, line_color='red', line_dash='dash', annotation_text='Overbought', annotation_position='top left')
    fig_rsi.add_hline(y=30, line_color='green', line_dash='dash', annotation_text='Oversold', annotation_position='top left')
    fig_rsi.update_layout(title=f"{ticker} RSI", xaxis_title="Date", yaxis_title="RSI")
    st.plotly_chart(fig_rsi, use_container_width=True)

    # Bollinger Bands
    st.header("Bollinger Bands")
    bb_window = st.slider("Select Bollinger Bands Window:", min_value=5, max_value=100, value=20)
    upper_band, lower_band = calculate_bollinger_bands(data, bb_window)
    
    # Plot Bollinger Bands using Plotly Express
    fig_bb = px.line(data, x=data.index, y=['Close'], labels={'value': 'Price'})
    fig_bb.add_scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band', line=dict(color='red'))
    fig_bb.add_scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band', line=dict(color='green'))
    fig_bb.update_layout(title=f"{ticker} Bollinger Bands", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig_bb, use_container_width=True)

if __name__ == "__main__":
    main()
