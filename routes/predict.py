from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from core.dependencies import get_current_user
from schemas.prediction_schema import PredictionOut
from models.prediction import PredictionModel
from database import get_database
from utils.validators import validate_image_file
from services.vision_service import run_vision_inference, generate_explanation

router = APIRouter()

# ================================
# 🔹 POST: Predict Disease
# ================================
@router.post("/", response_model=PredictionOut)
async def predict_disease(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        validate_image_file(file.filename)
    except HTTPException as e:
        raise e

    image_bytes = await file.read()

    # 🔹 Step 1: Run ML model
    inference_result = await run_vision_inference(image_bytes)

    # 🔹 Step 2: Generate explanation using AI
    explanation_result = await generate_explanation(
        inference_result["primary_disease"]
    )

    db = get_database()

    # 🔹 Step 3: Create DB object
    prediction_model = PredictionModel(
        user_id=str(current_user["_id"]),
        primary_disease=inference_result["primary_disease"],
        confidence_score=inference_result["confidence_score"],
        top_3_predictions=inference_result["top_3_predictions"],
        explanation=explanation_result["explanation"],
        recommendations=explanation_result["recommendations"],
        avoid_ingredients=explanation_result["avoid_ingredients"],
        safe_ingredients=explanation_result["safe_ingredients"]
    )

    # 🔹 Step 4: Save to DB
    result = await db.predictions.insert_one(
        prediction_model.model_dump(by_alias=True)
    )

    created_prediction = await db.predictions.find_one(
        {"_id": result.inserted_id}
    )

    # 🔹 Step 5: Return response
    return PredictionOut(
        id=str(created_prediction["_id"]),
        user_id=created_prediction["user_id"],
        primary_disease=created_prediction["primary_disease"],
        confidence_score=created_prediction["confidence_score"],
        top_3_predictions=created_prediction["top_3_predictions"],
        explanation=created_prediction["explanation"],
        recommendations=created_prediction["recommendations"],
        avoid_ingredients=created_prediction["avoid_ingredients"],
        safe_ingredients=created_prediction["safe_ingredients"],
        created_at=str(created_prediction["created_at"])
    )


# ================================
# 🔹 GET: Prediction History
# ================================
@router.get("/history")
async def get_prediction_history(
    current_user: dict = Depends(get_current_user)
):
    db = get_database()

    predictions_cursor = db.predictions.find(
        {"user_id": str(current_user["_id"])}
    ).sort("created_at", -1)  # ✅ latest first

    results = []

    async for p in predictions_cursor:
        results.append({
            "id": str(p["_id"]),
            "primary_disease": p.get("primary_disease"),
            "confidence_score": p.get("confidence_score"),
            "top_3_predictions": p.get("top_3_predictions"),
            "explanation": p.get("explanation"),
            "recommendations": p.get("recommendations"),
            "avoid_ingredients": p.get("avoid_ingredients"),
            "safe_ingredients": p.get("safe_ingredients"),
            "created_at": str(p.get("created_at")),
        })

    return results