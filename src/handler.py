import runpod
import torch
import torchaudio
import base64
import io
import os
from huggingface_hub import hf_hub_download, login

# Import the CSM generator
# We'll assume the generator.py is included in your src files
# If not, you might need to clone the repo or add it to your requirements
try:
    from generator import load_csm_1b
except ImportError:
    # If not directly available, try to import from the csm package
    import sys
    sys.path.append("/app/csm")
    from generator import load_csm_1b

hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    print("Logging in to Hugging Face Hub...")
    login(token=hf_token)
    print("Login successful!")
else:
    print("WARNING: No Hugging Face token provided. Set the HF_TOKEN environment variable if the model is private.")
# Load the model at startup to keep it in memory
print("Downloading and loading CSM-1B model...")
model_path = hf_hub_download(repo_id="sesame/csm-1b", filename="ckpt.pt")
generator = load_csm_1b(model_path, "cuda" if torch.cuda.is_available() else "cpu")
print("Model loaded successfully!")

def handler(job):
    """
    Handler function that generates speech from text using CSM-1B model.
    
    Input parameters:
    - text (str): The text to convert to speech
    - speaker (int, optional): Speaker ID, defaults to 0
    - context (list, optional): Context for generation, defaults to empty list
    - max_audio_length_ms (int, optional): Maximum audio length in milliseconds, defaults to 10,000
    
    Returns:
    - audio_base64 (str): Base64 encoded WAV audio
    - sample_rate (int): Sample rate of the generated audio
    - duration_ms (float): Duration of the generated audio in milliseconds
    """
    job_input = job["input"]
    
    # Extract parameters from the job input
    text = job_input.get("text", "Hello from Sesame.")
    speaker = job_input.get("speaker", 0)
    context = job_input.get("context", [])
    max_audio_length_ms = job_input.get("max_audio_length_ms", 10000)
    
    print(f"Generating audio for text: {text}")
    
    try:
        # Generate audio using CSM-1B
        audio = generator.generate(
            text=text,
            speaker=speaker,
            context=context,
            max_audio_length_ms=max_audio_length_ms,
        )
        
        # Convert to WAV format
        buffer = io.BytesIO()
        torchaudio.save(buffer, audio.unsqueeze(0).cpu(), generator.sample_rate, format="wav")
        buffer.seek(0)
        
        # Encode the audio as base64
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Calculate duration
        duration_ms = (audio.shape[0] / generator.sample_rate) * 1000
        
        return {
            "status": "success",
            "audio_base64": audio_base64,
            "sample_rate": generator.sample_rate,
            "duration_ms": float(duration_ms),
            "format": "wav"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Start the RunPod serverless handler
runpod.serverless.start({"handler": handler})
