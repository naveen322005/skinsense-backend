from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from schemas.auth_schema import UserCreate, UserOut, Token
from core.security import verify_password, get_password_hash, create_access_token
from database import get_database
from models.user import UserModel
from core.dependencies import get_current_user

router = APIRouter()

# ================================
# 🔹 REQUEST SCHEMA (NEW)
# ================================
class UpdateProfileRequest(BaseModel):
    name: str
    email: EmailStr


# ================================
# 🔹 REGISTER
# ================================
@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate):
    db = get_database()

    existing_user = await db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    hashed_password = get_password_hash(user_in.password)

    user_model = UserModel(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password
    )

    result = await db.users.insert_one(
        user_model.model_dump(by_alias=True)
    )

    created_user = await db.users.find_one(
        {"_id": result.inserted_id}
    )

    return UserOut(
        id=str(created_user["_id"]),
        name=created_user["name"],
        email=created_user["email"]
    )


# ================================
# 🔹 LOGIN
# ================================
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()

    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(subject=str(user["_id"]))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================================
# 🔹 GET PROFILE
# ================================
@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: dict = Depends(get_current_user)):
    return UserOut(
        id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"]
    )


# ================================
# 🔹 UPDATE PROFILE (NEW)
# ================================
@router.put("/me")
async def update_profile(
    payload: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()

    # 🔹 Check if email already exists (excluding current user)
    existing_user = await db.users.find_one({
        "email": payload.email,
        "_id": {"$ne": current_user["_id"]}
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already in use"
        )

    # 🔹 Update user data
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {
            "$set": {
                "name": payload.name,
                "email": payload.email
            }
        }
    )

    return {
        "message": "Profile updated successfully"
    }