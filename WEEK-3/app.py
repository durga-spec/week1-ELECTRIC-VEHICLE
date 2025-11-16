
# app.py
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import os

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="🔋 EV Prediction Dashboard",
    layout="wide",
    page_icon="🔋"
)

st.title("🔋 EV Prediction Dashboard")
st.markdown("""
Predict **EV Range**, **Sales**, and **Price** based on your vehicle's specifications.
Use the sliders to input the EV details below and click **Predict**.
""")

# ------------------ Tabs ------------------
tab1, tab2, tab3 = st.tabs(["Prediction", "Visualization", "Chatbot"])

# ------------------ Tab 1: Prediction ------------------
with tab1:
    st.header("📌 Enter EV Details")
    col1, col2 = st.columns(2)
    with col1:
        battery = st.slider("Battery Capacity (kWh)", min_value=20, max_value=200, value=50)
        weight = st.slider("Weight (kg)", min_value=800, max_value=3000, value=1500)
    with col2:
        motor = st.slider("Motor Power (kW)", min_value=50, max_value=500, value=100)
        charging = st.slider("Charging Stations", min_value=10, max_value=10000, value=500)

    if st.button("Predict"):
        folder_path = os.path.dirname(__file__)
        try:
            range_model = joblib.load(os.path.join(folder_path, "ev_range_model.pk1"), mmap_mode='r')
        except:
            range_model = None
            st.warning("Could not load EV Range model!")

        try:
            sales_model = joblib.load(os.path.join(folder_path, "ev_performance_model.pk1"), mmap_mode='r')
        except:
            sales_model = None
            st.warning("Could not load EV Sales model!")

        try:
            price_model = joblib.load(os.path.join(folder_path, "ev_price_model.pk1"), mmap_mode='r')
        except:
            price_model = None
            st.warning("Could not load EV Price model!")

        features = np.array([[battery, motor, weight, charging]])

        col_r, col_s, col_p = st.columns(3)

        # Range Prediction
        if range_model:
            try:
                predicted_range = range_model.predict(features)[0]
                col_r.metric("🔋 Predicted Range (km)", f"{predicted_range:.2f}")
            except Exception as e:
                col_r.error(f"Error: {e}")

        # Sales Prediction
        if sales_model:
            try:
                predicted_sales = sales_model.predict(features)[0]
                col_s.metric("📈 Predicted Sales (units)", f"{predicted_sales:.0f}")
            except Exception as e:
                col_s.error(f"Error: {e}")

        # Price Prediction
        if price_model:
            try:
                predicted_price = price_model.predict(features)[0]
                col_p.metric("💰 Predicted Price (USD)", f"${predicted_price:.2f}")
            except Exception as e:
                col_p.error(f"Error: {e}")

# ------------------ Tab 2: Visualization ------------------
with tab2:
    st.header("📊 Metrics Visualization")
    try:
        metrics_df = pd.DataFrame({
            "Metric": ["Range (km)", "Sales (units)", "Price (USD)"],
            "Value": [predicted_range if range_model else 0,
                      predicted_sales if sales_model else 0,
                      predicted_price if price_model else 0]
        })

        def metric_color(row):
            if row["Metric"] == "Range (km)":
                return "green" if row["Value"] > 300 else "orange" if row["Value"] > 150 else "red"
            if row["Metric"] == "Sales (units)":
                return "green" if row["Value"] > 1000 else "orange" if row["Value"] > 500 else "red"
            if row["Metric"] == "Price (USD)":
                return "green" if row["Value"] < 50000 else "orange" if row["Value"] < 100000 else "red"
            return "blue"

        metrics_df["Color"] = metrics_df.apply(metric_color, axis=1)

        fig = px.bar(
            metrics_df,
            x="Metric",
            y="Value",
            color="Color",
            color_discrete_map="identity",
            text="Value",
            height=400
        )
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(yaxis=dict(title="Value"), uniformtext_minsize=12, uniformtext_mode="hide")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Visualization error: {e}")

# ------------------ Tab 3: Chatbot ------------------
with tab3:
    st.header("💬 EV Chatbot")
    faq_responses = {
        "range": "🔋 EV range is the distance an electric vehicle can travel on a full charge.",
        "efficiency": "⚡ Efficiency can be increased by optimizing battery use, reducing weight, and maintaining optimal driving conditions.",
        "sales": "📈 EV sales are affected by price, incentives, availability of charging stations, and consumer awareness.",
        "price": "💰 EV price depends on battery capacity, motor power, features, brand, and government incentives.",
        "government incentive": "🏛️ Government incentives reduce the effective price of an EV and can boost sales.",
        "charging": "🔌 More charging stations make EVs more practical, positively affecting sales.",
        "battery": "🔋 Higher battery capacity increases range but may increase cost.",
        "motor": "⚡ Motor power affects performance and efficiency."
    }

    user_question = st.text_input("Ask a question about EVs:")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Ask Question"):
        if user_question:
            question = user_question.lower()
            answer = "❌ Sorry, I don't know the answer to that."
            for key in faq_responses:
                if key in question:
                    answer = faq_responses[key]
                    break
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("Bot", answer))

    for speaker, text in st.session_state.chat_history:
        if speaker == "You":
            st.info(f"**{speaker}:** {text}")
        else:
            st.success(f"**{speaker}:** {text}")