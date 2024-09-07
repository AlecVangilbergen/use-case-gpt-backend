# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run the application
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
