This project predicts the next 24 hourly kWh values based on the previous 48, using Holt–Winters exponential smoothing. It’s built with FastAPI and designed to be simple, robust, and quick to test.

## Why this setup?

* We're dealing with **hourly energy data**, so a **daily seasonal pattern** (`seasonal_periods=24`) makes sense.
* We use **additive** trend/seasonality to avoid values blowing up.
* Basic error handling is in place — invalid input returns HTTP 400 instead of killing the app.

## Quick start

### Set up a virtual environment
python -m venv .venv && source .venv/bin/activate

#### Install dependencies
pip install -r requirements.txt

#### Run the app
uvicorn main:app --reload

#### Then open: http://127.0.0.1:8000/docs to interact with the API.

## Running with Docker

### Build the image
docker build -t forecast-api .

### Run the container
docker run -p 8000:8000 forecast-api

## Request Example (JSON input)
{
  "series": [3.2, 3.1, 3.3, ..., 3.0]  // 48 hourly kWh values
}

## Response Example (JSON output)
{
  "prediction": [3.4, 3.5, ..., 3.6]  // 24-hour forecast
}

