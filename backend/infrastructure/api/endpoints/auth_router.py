from application.auth.auth import (
    authenticate_user,
    create_access_token,
    is_admin,
    generate_token_for_user,
)
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/token")
async def login_for_access_token(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # Generate token
    access_token = generate_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": user["email"],
            "role": user.get("role"),
            "fullname": user.get("fullname"),
        }
    )
    fullname = user["fullname"]
    print(f"Generated access token: {access_token}")

    return {"access_token": access_token, "token_type": "bearer", "fullname": fullname}
