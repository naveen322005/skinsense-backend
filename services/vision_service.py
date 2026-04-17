import io
import sys
import os
import numpy as np
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ai-model')))
from inference.predict import predict_single_image_array
from services.chatbot_service import get_disease_explanation

async def run_vision_inference(image_bytes: bytes) -> dict:
    # 1. Load image and resize to target dimension (224x224)
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img)
    
    # Expand array dimensions to match batch format (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    primary_disease, confidence_score, top_3 = predict_single_image_array(img_array)
    
    return {
        "primary_disease": primary_disease,
        "confidence_score": confidence_score,
        "top_3_predictions": top_3
    }

async def generate_explanation(disease: str) -> dict:
    explanation = await get_disease_explanation(disease)
    # The prompt should enforce json output or we parse it
    # For robust handling, we parse expected structure from Groq
    return explanation
