# Deployment and verification

1. Confirm the model artifact `airaware_real_model.joblib` and metrics file are in the repository root.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Select **Create app** → **Deploy a public app from GitHub**.
4. Repository: `gurkiratjanjua13-creator/MIT105-AirAware-AI-SDG11`; branch: `main`; file: `app.py`.
5. Deploy, then test a prediction with lag1=75, lag2=70, lag7=65, rolling7=70, and forecast date 2026-10-25. Expected prediction is approximately 67.8 µg/m³ if dependencies are compatible.
6. Confirm the metrics table and its Ridge MAE 26.383, RMSE 35.077, R² 0.375.
7. Capture the public URL, screenshot and deployment date for the final report and slides.

**Note:** Localhost is not public deployment. Never claim successful public deployment until the live URL is tested. The stored model is a joblib/pickle object; load only this trusted artifact. CAMS estimates are not direct ground measurements.
