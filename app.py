import streamlit as st

def main():
    st.set_page_config(
        page_title="StockScout - Intelligent Stock Analysis & Prediction",
        layout="wide"
    )

    # Header Section
    st.title("🎯 StockScout")
    st.subheader("Your Intelligent Stock Analysis & Prediction Platform")

    # Main Description
    st.markdown("""
    ### 📊 Transform Your Trading Strategy with Data-Driven Insights
    
    StockScout combines advanced machine learning with fundamental and technical analysis 
    to help you make informed investment decisions.
    """)

    st.markdown("## 🚀 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📈 Price Prediction",expanded=True):
                st.write("""
                - Advanced ML-based price forecasting
                - Customizable prediction timeframes
                - Historical trend analysis
                - Confidence intervals for predictions
                """)
        
    with col2:
        with st.expander("📊 Fundamental Analysis",expanded=True):
                st.markdown("""
                - Market capitalization insights
                - Dividend history and yields
                - Financial ratios analysis
                - Company performance metrics
                """)
    
    with st.expander("📉 Technical Indicators",expanded=True):
        st.markdown("""
        - Moving averages (SMA, EMA) for trend identification
        - RSI and MACD for momentum analysis
        - Volume analysis for trade validation
        - Support and resistance levels detection
        """)

    # How It Works
    st.markdown("## 🎯 How It Works")
    
    st.markdown("""
    1. **Enter Stock Details**
       - Input your desired stock symbol
       - Choose prediction timeframe
       
    2. **Get Comprehensive Analysis**
       - View price predictions with confidence intervals
       - Access detailed fundamental analysis
       - Explore technical indicators
       
    3. **Make Informed Decisions**
       - Compare different metrics
       - Analyze trends and patterns
       - Export reports for further analysis
    """)

    # Footer Section
    st.markdown("---")
    st.markdown("""
    ### 📌 Note
    StockScout is designed for informational purposes only. Always conduct your own 
    research and consult with financial advisors before making investment decisions.
    """)

    st.markdown("""
    <small>
    *The predictions and analysis provided are based on historical data and should not 
    be considered as financial advice. Market conditions can change rapidly, and past 
    performance is not indicative of future results.*
    </small>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()