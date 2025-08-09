# Use the official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all files to /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
