FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip is updated
RUN python3.10 -m pip install --upgrade pip setuptools wheel

# Clone the CSM repository
WORKDIR /app
RUN git clone https://github.com/SesameAILabs/csm.git

# Set up working directory
WORKDIR /app/csm

# Install the specific dependencies required
RUN python3.10 -m pip install --no-cache-dir \
    torch==2.4.0 \
    torchaudio==2.4.0 \
    tokenizers==0.21.0 \
    transformers==4.49.0 \
    huggingface_hub==0.28.1 \
    torchtune==0.4.0 \
    torchao==0.9.0 \
    einops \
    && python3.10 -m pip install --no-cache-dir moshi==0.2.2 \
    && python3.10 -m pip install --no-cache-dir git+https://github.com/SesameAILabs/silentcipher@master

# Copy the additional requirements if needed
COPY builder/requirements.txt /requirements.txt
RUN if [ -f "/requirements.txt" ]; then \
    python3.10 -m pip install --upgrade -r /requirements.txt --no-cache-dir; \
    rm /requirements.txt; \
    fi

# Add src files (Worker Template)
COPY src /src



# Use a direct command rather than entrypoint
CMD ["python3.10", "-u", "/src/handler.py"]
