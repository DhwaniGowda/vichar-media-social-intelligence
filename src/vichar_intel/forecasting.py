"""Small-sample baseline forecasting; intended for teaching, not production planning."""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

def forecast_daily_metric(daily: pd.DataFrame, metric: str="views", horizon: int=7):
    df=daily.copy()
    df["date"]=pd.to_datetime(df["date"], errors="coerce")
    df=df.dropna(subset=["date",metric]).sort_values("date")
    if len(df)<14:
        return {"status":"insufficient_data","message":f"Need at least 14 observations; received {len(df)}."}
    # Hold out final 7 records; use trailing 7-observation mean baseline.
    holdout=min(7, max(3, len(df)//4))
    train=df.iloc[:-holdout][metric].astype(float).to_numpy()
    test=df.iloc[-holdout:][metric].astype(float).to_numpy()
    pred=np.repeat(float(np.mean(train[-min(7,len(train)): ])),len(test))
    mae=float(mean_absolute_error(test,pred)); rmse=float(mean_squared_error(test,pred)**0.5)
    # Refit trailing mean. Forecast is a flat baseline; no seasonality inferred.
    fc=float(np.mean(df[metric].astype(float).to_numpy()[-min(7,len(df)):]))
    future=pd.date_range(df.date.max()+pd.Timedelta(days=1), periods=horizon, freq="D")
    forecast=pd.DataFrame({"date":future,"forecast":np.repeat(fc,horizon)})
    return {"status":"experimental_baseline","mae":mae,"rmse":rmse,"holdout_size":holdout,"forecast":forecast,
            "message":"7-observation trailing mean baseline. Short history and cross-posted IG+FB scope limit inference; not a dependable growth prediction."}
