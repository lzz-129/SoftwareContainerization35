# Use a base image with Python pre-installed
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0" ,"--port=5000"]