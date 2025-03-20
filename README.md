### Running Sesame TTS on RunPod (Serverless)

This document outlines the steps to deploy and interact with Sesame TTS using RunPod serverless cloud.

---

### Step 1: Deploying Sesame TTS on RunPod

- **Docker Image:** Use the provided Docker image `mwiki/speech:v1`.
- Log in to your [RunPod account](https://www.runpod.io/) and navigate to serverless deployments.
- Create a new endpoint using the Docker image mentioned above (`mwiki/speech:v1`).

---

### Step 2: Running Sesame TTS

Once the deployment is complete, you'll receive an `endpoint_id`. Use it to interact with your deployed model via API.

Use the following example `curl` command to test your deployment:

```bash
curl -X POST "https://api.runpod.ai/v2/<endpoint_id>/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your API Key>" \
  -d '{
    "input": {
      "text": "Hello from Sesame AI. This is a test.",
      "speaker": 0,
      "max_audio_length_ms": 10000
    }
  }'
```

- Replace `<endpoint_id>` with your actual endpoint ID.
- Replace `<your API Key>` with your RunPod API key.

---

### Step 3: Testing and Exploration

Feel free to modify the input parameters to experiment:
- Change `text` to generate audio from different sentences.
- Modify the `speaker` ID to explore different voice profiles.
- Adjust `max_audio_length_ms` for audio length constraints.

---

Enjoy exploring Sesame TTS on RunPod!


