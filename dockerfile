# Use the official Python base image
FROM python:3.12

# Install required libraries and compilers, including additional dependencies
RUN apt-get update -qq \
    && apt-get install --no-install-recommends --yes \
        build-essential \
        default-libmysqlclient-dev \
        # Necessary for mysqlclient runtime. Do not remove.
        libmariadb3 \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --no-cache-dir mysqlclient \
    && apt-get autoremove --purge --yes \
        build-essential \
        default-libmysqlclient-dev

# Set the working directory inside the container
WORKDIR /app

COPY .env.example .env

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

RUN python -m spacy download en_core_web_lg

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 3301

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3301", "--reload"]
