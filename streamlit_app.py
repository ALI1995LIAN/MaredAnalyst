import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="المارد الملكي", layout="centered", initial_sidebar_state="collapsed")

# --- UI Elements ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>المارد الملكي</h1>", unsafe_allow_html=True)
st.markdown("---")

symbol = st.text_input("1. أدخل رمز العملة أو السهم", placeholder="مثال: BTC-USD, EURUSD=X, AAPL")

col1, col2 = st.columns(2)
with col1:
    price_type = st.selectbox("2. اختر النوع", ["قمة", "قاع"])
with col2:
    price_value = st.number_input("3. أدخل السعر المرجعي", min_value=0.0, step=0.01, format="%.5f")

# --- Main Button ---
if st.button("👑 احسب الأهداف", type="primary", use_container_width=True):
    if not symbol or price_value <= 0:
        st.warning("يرجى إدخال الرمز والسعر بشكل صحيح.")
    else:
        with st.spinner("...جاري جلب البيانات والتحليل"):
            try:
                # --- Data Fetching (Connects to live prices) ---
                data = yf.download(symbol, period="6mo", interval="1d")
                
                if data.empty:
                    st.error("لم يتم العثور على بيانات للرمز المدخل. تأكد من صحة الرمز.")
                else:
                    # --- Analysis Logic ---
                    low_price = data['Low'].min()
                    high_price = data['High'].max()
                    num_levels = 3 # 3 target levels
                    levels = []
                    
                    if price_type == "قمة":
                        # Calculate 3 target levels downwards
                        levels = np.linspace(price_value, low_price, num_levels + 2)[1:-1]
                    else: # قاع
                        # Calculate 3 target levels upwards
                        levels = np.linspace(price_value, high_price, num_levels + 2)[1:-1]
                    
                    st.success("تم التحليل بنجاح!")
                    
                    # --- Display Results ---
                    st.markdown("---")
                    st.markdown("<h2 style='color: #FFD700;'>🎯 الأهداف المحسوبة</h2>", unsafe_allow_html=True)
                    
                    if len(levels) > 0:
                        for i, target_price in enumerate(levels):
                            st.metric(label=f"الهدف {i+1}", value=f"{target_price:,.4f}")
                    else:
                        st.info("لم يتمكن من حساب الأهداف.")

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
