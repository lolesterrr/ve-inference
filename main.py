import uvicorn
from fastapi import FastAPI, UploadFile
import torch
import clip
from PIL import Image
import io
import os

app = FastAPI()

# Load the model once when the container starts
print("Loading model...")
device = "cpu"
# This will now correctly find the 'load' attribute from openai-clip
model, preprocess = clip.load("ViT-B/32", device=device)
print("Model loaded successfully.")

@app.post("/embed")
async def embed(file: UploadFile):
    # Read the image bytes and prepare it for CLIP
    image = preprocess(Image.open(io.BytesIO(await file.read()))).unsqueeze(0).to(device)
    
    # Generate the vector
    with torch.no_grad():
        vector = model.encode_image(image)
        
    # Return as a list of numbers
    return {"vector": vector.cpu().numpy().tolist()[0]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
