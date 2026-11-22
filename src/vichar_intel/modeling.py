"""Exploratory content-view modelling using only pre-publication metadata available in the audit.
This is a low-sample baseline and is not suitable for operational prediction.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

def run_content_model(content: pd.DataFrame):
    df=content[(content.platform=="Instagram") & (content.content_type.isin(["Reel","Carousel"]))].copy()
    df["publish_date"]=pd.to_datetime(df.publish_date,errors="coerce")
    df=df.dropna(subset=["publish_date","views"]).sort_values("publish_date")
    if len(df)<25:
        return {"status":"insufficient_data","message":f"At least 25 Instagram feed rows required; found {len(df)}."}
    df["weekday"]=df.publish_date.dt.dayofweek.astype(str)
    df["month"]=df.publish_date.dt.month.astype(str)
    X=df[["content_type","weekday","month"]]
    y=np.log1p(df.views.astype(float))
    split=max(1,int(len(df)*0.8))
    X_train,X_test=X.iloc[:split],X.iloc[split:]
    y_train,y_test=y.iloc[:split],y.iloc[split:]
    if len(X_test)<5:
        return {"status":"insufficient_test_data","message":"Not enough chronological holdout examples."}
    prep=ColumnTransformer([("cat",OneHotEncoder(handle_unknown="ignore"),["content_type","weekday","month"])])
    models={
      "Naive median baseline":DummyRegressor(strategy="median"),
      "Random Forest exploratory":RandomForestRegressor(n_estimators=200,max_depth=3,min_samples_leaf=3,random_state=42)
    }
    results=[]
    for name,est in models.items():
        pipe=Pipeline([("prep",prep),("model",est)])
        pipe.fit(X_train,y_train)
        p=np.expm1(pipe.predict(X_test)); actual=np.expm1(y_test)
        results.append({"model":name,"test_rows":len(y_test),"MAE_views":float(mean_absolute_error(actual,p)),
                        "RMSE_views":float(mean_squared_error(actual,p)**0.5),"R2_log_scale":float(r2_score(y_test,pipe.predict(X_test)))})
    return {"status":"experimental_only","results":pd.DataFrame(results),"n_rows":len(df),
      "message":"Only date and content format are used because pre-publication features (duration, creative attributes, paid support, exact topic labels) are not consistently provided. Small, viral-outlier-heavy sample. Do not use for editorial decisions."}
