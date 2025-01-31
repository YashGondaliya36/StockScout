import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import yaml

def load_company_info(ticker):
    stock = yf.Ticker(ticker)
    return stock

def load_ticker_from_config():
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['data_ingestion']['ticker']

def convert_to_indian_format(number):
    if number is None:
        return 'N/A'
    
    sign = "-" if number < 0 else ""  # Preserve negative sign
    number = abs(number)  # Work with absolute value for formatting
    
    if number >= 1e7:  # 1 crore
        return f"{sign}₹{number/1e7:.2f} Cr"
    elif number >= 1e5:  # 1 lakh
        return f"{sign}₹{number/1e5:.2f} L"
    elif number >= 1e3:  # 1 thousand
        return f"{sign}₹{number/1e3:.2f} K"
    else:
        return f"{sign}₹{number:.2f}"


def format_financial_statement(df):
    """Convert financial statement values to Indian format"""
    formatted_df = df.copy()
    for col in formatted_df.columns:
        formatted_df[col] = formatted_df[col].apply(convert_to_indian_format)
    return formatted_df

def get_brief_summary(text, max_words=50):
    """Get first few words of the summary"""
    if not text:
        return "No description available"
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]) + "..."

def main():
    st.header("📊 Stock Fundamental Analysis",divider='rainbow')
    
    # Load ticker from config.yaml
    ticker = load_ticker_from_config()
    st.write(f"Analyzing stock for: **{ticker}**")
    
    if ticker:
        try:
            stock = load_company_info(ticker)
            info = stock.info
            
            # Company Quick Overview
            st.header("Quick Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Price", convert_to_indian_format(info.get('currentPrice')))
                st.metric("Market Cap", convert_to_indian_format(info.get('marketCap')))
                
            with col2:
                st.metric("52W High", convert_to_indian_format(info.get('fiftyTwoWeekHigh')))
                st.metric("52W Low", convert_to_indian_format(info.get('fiftyTwoWeekLow')))
                
            with col3:
                st.metric("P/E Ratio", round(info.get('trailingPE', 0), 2))
                st.metric("Beta", round(info.get('beta', 0), 2))

            # Brief Company Description with expander for full view
            st.subheader("About Company")
            full_summary = info.get('longBusinessSummary', 'No description available')
            brief_summary = get_brief_summary(full_summary)
            st.write(brief_summary)
            if len(full_summary) > len(brief_summary):
                with st.expander("Read more"):
                    st.write(full_summary)

            # Key Financial Metrics
            with st.expander("📊 Financial Metrics"):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Income Metrics")
                    metrics = {
                        "Revenue": info.get('totalRevenue'),
                        "Net Income": info.get('netIncomeToCommon'),
                        "EBITDA": info.get('ebitda')
                    }
                    for metric, value in metrics.items():
                        st.metric(metric, convert_to_indian_format(value))

                with col2:
                    st.subheader("Balance Sheet Metrics")
                    metrics = {
                        "Total Debt": info.get('totalDebt'),
                        "Cash and Cash Equivalents": info.get('totalCash')
                    }
                    for metric, value in metrics.items():
                        st.metric(metric, convert_to_indian_format(value))

            # Historical Financials with Indian format
            with st.expander("📈 Historical Financials"):
                income_stmt = stock.financials
                balance_sheet = stock.balance_sheet
                cash_flow = stock.cashflow

                tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
                
                with tab1:
                    st.dataframe(format_financial_statement(income_stmt))
                with tab2:
                    st.dataframe(format_financial_statement(balance_sheet))
                with tab3:
                    st.dataframe(format_financial_statement(cash_flow))

            # Stock Performance Chart using Plotly Express
            with st.expander("📊 Stock Performance"):
                time_period = st.text_input("Enter the time period for analysis (e.g., '1d','2mo', '3y'):", '1y')
                hist = stock.history(period=time_period)

                # Create a line chart for stock prices
                fig = px.line(hist, x=hist.index, y=["Open", "High", "Low", "Close"],
                              labels={"value": "Stock Price (₹)", "variable": "Price Type"},
                              title=f"{ticker} Stock Price Trend ({time_period})")

                # Create a bar chart for volume
                fig_volume = px.bar(hist, x=hist.index, y="Volume",
                                    labels={"Volume": "Traded Volume"},
                                    title="Trading Volume")

                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig_volume, use_container_width=True)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            st.write("Please check if the ticker symbol is correct.")

if __name__ == "__main__":
    main()
