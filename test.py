import asyncio
import aiohttp
import base64
import json

async def test_runpod_api():
    # Your RunPod API details
    ENDPOINT_ID = "<RUNPOD_ENDPOINT_ID>"
    API_KEY = "<RP_API_KEY>"
    
    # API URL
    url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Request body
    payload = {
        "input": {
            "text": "Hwy How are YOu?",
            "speaker": 0,
            "max_audio_length_ms": 10000
        }
    }
    
    async with aiohttp.ClientSession() as session:
        # Make the initial request
        print("Sending request...")
        async with session.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            print(f"Status code: {response.status}")
            print("Initial response:", json.dumps(result, indent=2))
            
            # If asynchronous API (standard RunPod)
            if "id" in result:
                job_id = result["id"]
                print(f"Job submitted with ID: {job_id}")
                
                # Poll for completion
                status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
                print(f"Polling status at: {status_url}")
                
                while True:
                    print("Checking job status...")
                    async with session.get(status_url, headers={"Authorization": f"Bearer {API_KEY}"}) as status_response:
                        status_data = await status_response.json()
                        
                        print(f"Current status: {status_data.get('status')}")
                        
                        if status_data.get('status') == "COMPLETED":
                            print("Job completed!")
                            output = status_data.get('output', {})
                            print(json.dumps(output, indent=2))
                            
                            if "audio_base64" in output:
                                print("Received audio data, saving to file...")
                                audio_data = base64.b64decode(output["audio_base64"])
                                
                                with open("output.wav", "wb") as f:
                                    f.write(audio_data)
                                
                                print("Audio saved to output.wav")
                                break
                            else:
                                print("No audio data in the response")
                                break
                        
                        elif status_data.get('status') == "FAILED":
                            print("Job failed:")
                            print(status_data.get('error'))
                            break
                        
                        elif status_data.get('status') in ["IN_QUEUE", "IN_PROGRESS"]:
                            print(f"Job is {status_data.get('status')}, waiting 2 seconds...")
                            await asyncio.sleep(2)
                        
                        else:
                            print(f"Unknown status: {status_data.get('status')}")
                            break
            
            # For synchronous API (if you configured it that way)
            elif "audio_base64" in result:
                print("Received audio data immediately, saving to file...")
                audio_data = base64.b64decode(result["audio_base64"])
                
                with open("output.wav", "wb") as f:
                    f.write(audio_data)
                
                print("Audio saved to output.wav")

# Run the async function
if __name__ == "__main__":
    asyncio.run(test_runpod_api())
