from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title="AirAware AI | Delhi PM2.5", page_icon="🌿", layout="wide")
st.title("AirAware AI · Delhi PM2.5 forecasting")
st.caption("MIT 105 Assessment 2 · SDG 11.6 · Research prototype")
model_path = BASE / "airaware_real_model.joblib"
if not model_path.exists():
    st.error("Trained model missing. Upload airaware_real_model.joblib to the repository.")
    st.stop()
obj = joblib.load(model_path)
st.success("Trained using 2025 Delhi Open-Meteo/CAMS modelled estimates (not ground observations).")
st.info("Enter historical daily PM2.5 values; no same-day future information.")
a, b, c = st.columns(3)
with a:
    lag1 = st.number_input("Yesterday PM2.5 (µg/m³)", min_value=0., max_value=1000., value=75.)
    lag2 = st.number_input("Two days ago", min_value=0., max_value=1000., value=70.)
with b:
    lag7 = st.number_input("Seven days ago", min_value=0., max_value=1000., value=65.)
    rolling7 = st.number_input("Mean of previous seven days", min_value=0., max_value=1000., value=70.)
with c:
    d = st.date_input("Forecast date")
if st.button("Forecast next-day PM2.5", type="primary"):
    x = pd.DataFrame([dict(lag1=lag1, lag2=lag2, lag7=lag7, rolling7=rolling7, dayofyear=d.timetuple().tm_yday, month=d.month)])
    pred = max(0, float(obj["model"].predict(x[obj["features"]])[0]))
    st.metric("Estimated PM2.5", f"{pred:.1f} µg/m³")
    st.caption(f'Selected model: {obj["name"]}. Not a regulatory alert or medical advice.')
metrics = BASE / "real_model_metrics.csv"
if metrics.exists():
    st.subheader("Chronological holdout evaluation")
    st.dataframe(pd.read_csv(metrics), hide_index=True)
st.caption("Data source: Open-Meteo Air Quality API; CAMS modelled estimates for Delhi (2025). External station validation remains future work.")
