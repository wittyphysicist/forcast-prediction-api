from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from statsmodels.tsa.holtwinters import ExponentialSmoothing

app = FastAPI()

class generate_forecast(BaseModel):
    series: List[float]

@app.post("/forecast")
def forecast(input_series: generate_forecast):
    s = input_series.series

    # to test if the length is correct
    if len(s) != 48:
        raise HTTPException(status_code=400, detail="need exactly 48 points")

    try:
        model = ExponentialSmoothing(
            input_series.series, trend="add", seasonal="add", seasonal_periods=24
        )
        fit = model.fit()
        prediction = fit.generate_forecast(24)
        return {"prediction": list(prediction)}
    
    except ValueError as ve:  # statsmodels often throws ValueError on bad series
        raise HTTPException(status_code=400, detail=f"invalid series: {ve}")
