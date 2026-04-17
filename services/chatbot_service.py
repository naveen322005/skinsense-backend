import os
import json
from groq import Groq
from config import settings

client = None

def get_groq_client():
    global client
    if client is None:
        client = Groq(api_key=settings.GROQ_API_KEY)
    return client

SYSTEM_PROMPT = """
You are a friendly AI chatbot specialized in skin care and skin diseases.
You help users with dermatological questions only.
Rules:
- Keep answers short and simple
- Answer ONLY skin-related queries.
- If the question is not skin-related, say EXACTLY: 'I am a dermatology-focused assistant and cannot answer non-skin-related queries.'
"""

async def get_chatbot_reply(user_message: str) -> str:
    groq_client = get_groq_client()
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def get_disease_explanation(disease: str) -> dict:
    groq_client = get_groq_client()
    prompt = f"""
    The user has been diagnosed with '{disease}' by our AI vision model.
    Provide an explanation formatted EXACTLY as a valid JSON object with the following keys and NO markdown wrappers:
    {{
        "explanation": "A simple explanation of the disease.",
        "recommendations": "General advice and recommendations.",
        "avoid_ingredients": "Ingredients in products to avoid.",
        "safe_ingredients": "Safe ingredients to use."
    }}
    """
    
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a precise JSON-generating dermatology AI."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        content = response.choices[0].message.content.strip()
        # Clean up in case groq adds ```json
        if content.startswith("```json"):
            content = content[7:-3]
        if content.startswith("```"):
            content = content[3:-3]
            
        return json.loads(content.strip())
    except Exception as e:
        return {
            "explanation": f"Failed to generate explanation. Error: {str(e)}",
            "recommendations": "Consult a dermatologist.",
            "avoid_ingredients": "Unknown",
            "safe_ingredients": "Unknown"
        }
