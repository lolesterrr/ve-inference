import uvicorn
from fastapi import FastAPI, UploadFile
import torch
import clip
from PIL import Image
import io
import os

app = FastAPI()

# FORCE low memory mode
device = "cpu"
print("Loading model in half-precision...")

# Load model, then convert to float16 to save huge amounts of RAM
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval() 
model.half() # Convert weights to 16-bit to cut memory usage by 50%
print("Model loaded successfully.")

@app.post("/embed")
async def embed(file: UploadFile):
    # Process image, convert to half-precision to match model
    image = preprocess(Image.open(io.BytesIO(await file.read()))).unsqueeze(0).to(device)
    image = image.half() 
    
    with torch.no_grad():
        vector = model.encode_image(image)
        
    return {"vector": vector.cpu().float().numpy().tolist()[0]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
