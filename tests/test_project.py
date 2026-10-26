from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_metrics_exist_and_have_three_models():
    df = pd.read_csv(ROOT / "real_model_metrics.csv")
    assert len(df) == 3
    assert {"model", "MAE", "RMSE", "R2", "CV_MAE_mean"} <= set(df.columns)
    assert df["MAE"].notna().all()

def test_ridge_is_holdout_winner():
    df = pd.read_csv(ROOT / "real_model_metrics.csv")
    assert df.loc[df.MAE.idxmin(), "model"] == "Ridge"

def test_model_artifact_exists():
    assert (ROOT / "airaware_real_model.joblib").is_file()
