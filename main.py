import uvicorn
from fastapi import FastAPI, UploadFile
import torch
import clip
from PIL import Image
import io
import os

app = FastAPI()

# Load the model once on startup
print("Loading model...")
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
print("Model loaded.")

@app.post("/embed")
async def embed(file: UploadFile):
    # Read the uploaded image
    image = preprocess(Image.open(io.BytesIO(await file.read()))).unsqueeze(0).to(device)
    
    # Generate the vector
    with torch.no_grad():
        vector = model.encode_image(image)
        
    return {"vector": vector.cpu().numpy().tolist()[0]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
