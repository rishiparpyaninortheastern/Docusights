# Use an official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file first (if exists)
COPY requirements.txt .

# Install dependencies (including Uvicorn)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install uvicorn \
    && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Use explicit Python path to run Uvicorn
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
