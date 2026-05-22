# Use the official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the server
WORKDIR /app

# Copy your requirements file and install the libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app files (app.py, the pages folder, etc.)
COPY . .

# Expose the port that Google Cloud Run defaults to
EXPOSE 8080

# The command to start the app when the server wakes up
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
