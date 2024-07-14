FROM python:3.10-slim

WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 30000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
