FROM python:3.12

# Install dependencies
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
        gcc \
        build-essential \
        zlib1g-dev \
        wget \
        unzip \
        cmake \
        python3-dev \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
    && apt-get clean

# Install Python packages
RUN pip install --upgrade pip \
    && pip install \
        ipython[all] \
        numpy \
        nose \
        matplotlib \
        pandas \
        scipy \
        sympy \
        cython \
        spacy \
    && rm -fr /root/.cache

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
