# Use the official Python base image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

COPY .env.example .env

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip install uv 
RUN uv venv
# Install the Python dependencies
RUN uv pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 3301

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3301", "--reload"]
