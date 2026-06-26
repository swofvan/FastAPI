from fastapi import FastAPI, Header

from database import engine

from models import Base


import os

from fastapi import FastAPI, Form, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, User

from crud import get_user_by_email, get_user_by_mobile, create_user, get_user_by_email_login, get_user_by_id
from forms import check_image

from jwt_token import create_access_token

from security import hash_password, verify_password, verify_token


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():

    return {
        "message": "Welcome to User Management System"
    }


UPLOAD_FOLDER = "uploads/users"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/api/auth/register")
def register(
    fullname: str = Form(...),
    email: str = Form(...),
    mobilenumber: str = Form(...),
    password: str = Form(...),
    profileimage: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if len(password) < 8:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Password must contain at least 8 characters"
            }
        )

    if get_user_by_email(db, email):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Email already exists"
            }
        )

    if get_user_by_mobile(db, mobilenumber):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Mobile number already exists"
            }
        )

    if not check_image(profileimage):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Image must be jpg, jpeg or png and maximum size is 2 MB"
            }
        )

    profileimage.file.seek(0)

    image_path = os.path.join(
        UPLOAD_FOLDER,
        profileimage.filename
    )

    with open(image_path, "wb") as file:
        file.write(profileimage.file.read())

    print(password)
    print(type(password))
    print(len(password))

    new_user = User(
        fullname=fullname,
        email=email,
        mobilenumber=mobilenumber,
        password=hash_password(password),
        profileimage=image_path
    )

    user = create_user(db, new_user)


    return JSONResponse(
        status_code=201,
        content={
            "message": "User created successfully",
            "data": {
                "userid": user.userid,
                "fullname": user.fullname,
                "email": user.email,
                "mobilenumber": user.mobilenumber,
                "profileimage": user.profileimage,
                "isactive": user.isactive
            }
        }
    )


@app.post("/api/auth/login")
def login(

    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)

):

    user = get_user_by_email_login(
        db,
        email,
    )

    if not user:
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid email or password"
            }
        )
    if not verify_password(password, user.password):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid email or password"
            }
        )

    token = create_access_token(
        {
            "userid": user.userid,
            "email": user.email
        }
    )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "token": token,
            "userId": user.userid,
            "fullname": user.fullname
        }
    )


@app.get("/api/auth/profile")
def profile(

    authorization: str = Header(...),
    db: Session = Depends(get_db)

):
    token = authorization.replace("Bearer ", "")

    payload = verify_token(token)

    if not payload:
        return JSONResponse(
            status_code=401,
            content={
                "message": "Invalid token"
            }
        )

    userid = payload["userid"]

    user = get_user_by_id(db, userid)

    if not user:
        return JSONResponse(
            status_code=404,
            content={
                "message": "User not found"
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Profile details",
            "data": {
                "userid": user.userid,
                "fullname": user.fullname,
                "email": user.email,
                "mobilenumber": user.mobilenumber,
                "profileimage": user.profileimage,
                "isactive": user.isactive
            }
        }
    )