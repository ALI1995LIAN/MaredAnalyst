import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="المارد الملكي", layout="centered", initial_sidebar_state="collapsed")

# --- UI Elements ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>👑 المارد الملكي 👑</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Inputs ---
symbol = st.text_input("1. أدخل رمز العملة أو السهم", placeholder="مثال: BTC-USD, EURUSD=X, AAPL")

col1, col2 = st.columns(2)
with col1:
    price_type = st.selectbox("2. اختر النوع", ["قمة", "قاع"])
with col2:
    price_value = st.number_input("3. أدخل السعر المرجعي", min_value=0.0, step=0.01, format="%.5f")

# --- Main Button ---
if st.button("👑 احسب الأهداف 👑", type="primary", use_container_width=True):
    if not symbol or price_value <= 0:
        st.warning("يرجى إدخال الرمز والسعر بشكل صحيح.")
    else:
        with st.spinner("جاري جلب البيانات والتحليل... يرجى الانتظار."):
            try:
                # --- Data Fetching (Connects to live prices) ---
                data = yf.download(symbol, period="6mo", interval="1d")

                if data.empty:
                    st.error("لم يتم العثور على بيانات للرمز المدخل. تأكد من صحة الرمز.")
                else:
                    # --- Analysis Logic ---
                    st.success("تم التحليل بنجاح! 🎉")

                    # Fibonacci Levels Calculation
                    if price_type == "قمة": # Bearish Case (Targets are below)
                        diff = data['High'].max() - data['Low'].min()
                        levels = [
                            price_value - 0.236 * diff,
                            price_value - 0.382 * diff,
                            price_value - 0.500 * diff,
                            price_value - 0.618 * diff,
                        ]
                        level_names = ["الهدف الأول (23.6%)", "الهدف الثاني (38.2%)", "الهدف الثالث (50%)", "الهدف الذهبي (61.8%)"]
                    else: # Bullish Case (Targets are above)
                        diff = data['High'].max() - data['Low'].min()
                        levels = [
                            price_value + 0.236 * diff,
                            price_value + 0.382 * diff,
                            price_value + 0.500 * diff,
                            price_value + 0.618 * diff,
                        ]
                        level_names = ["الهدف الأول (23.6%)", "الهدف الثاني (38.2%)", "الهدف الثالث (50%)", "الهدف الذهبي (61.8%)"]

                    # --- Display Results ---
                    st.markdown("### 🎯 الأهداف المحسوبة (فيبوناتشي)")
                    results_df = pd.DataFrame({
                        "المستوى": level_names,
                        "السعر المتوقع": [f"{level:.4f}" for level in levels]
                    })
                    st.dataframe(results_df, use_container_width=True, hide_index=True)

                    # --- Charting ---
                    st.markdown("### 📈 الرسم البياني")
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='السعر'))
                    fig.add_hline(y=price_value, line_dash="dot", line_color="white", annotation_text=f"السعر المرجعي: {price_value}", annotation_position="bottom right")
                    for level, name in zip(levels, level_names):
                        fig.add_hline(y=level, line_dash="dash", line_color="#FFD700", annotation_text=name, annotation_position="top left")
                    fig.update_layout(title=f'تحليل {symbol}', yaxis_title='السعر', template='plotly_dark', xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {e}")
