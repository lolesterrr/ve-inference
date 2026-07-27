import uvicorn
from fastapi import FastAPI, UploadFile
import torch
# We will use this to ensure we are loading the correct module
import clip as clip_module 
from PIL import Image
import io
import os

app = FastAPI()

print("Loading model...")
device = "cpu"
# Using the alias we defined above
model, preprocess = clip_module.load("ViT-B/32", device=device)
print("Model loaded successfully.")

@app.post("/embed")
async def embed(file: UploadFile):
    image = preprocess(Image.open(io.BytesIO(await file.read()))).unsqueeze(0).to(device)
    with torch.no_grad():
        vector = model.encode_image(image)
    return {"vector": vector.cpu().numpy().tolist()[0]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
