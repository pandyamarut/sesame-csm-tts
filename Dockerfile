FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3.10 \
    python3.10-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone the CSM repository
WORKDIR /app
RUN git clone https://github.com/SesameAILabs/csm.git

# Set up Python environment with virtual env (as in your original commands)
WORKDIR /app/csm
RUN python3.10 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt && \
    pip install huggingface_hub torchaudio

# Python dependencies from the original template
COPY builder/requirements.txt /requirements.txt
RUN . /app/csm/.venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Copy handler.py to the root if not already in src

# Keep the container running and run the handler with the virtual environment
CMD ["/bin/bash", "-c", "source /app/csm/.venv/bin/activate && python -u src/handler.py"]