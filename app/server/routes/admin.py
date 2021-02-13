from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from app.server.database.database import admin_collection
#from app.server.auth.admin import validate_login
from app.server.auth.jwt_handler import signJWT
from app.server.database.database import add_admin
from app.server.models.admin import AdminModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: HTTPBasicCredentials = Body(...)):
    admin_user = await admin_collection.find_one({"email": admin_credentials.username}, {"_id": 0})
    if (admin_user):
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"])
        if (password):
            return signJWT(admin_credentials.username)

        return "Incorrect email or password"

    return "Incorrect email or password"

    # OLD CODE
    # if validate_login(admin):
    #     return {
    #         "email": admin.username,
    #         "access_token": signJWT(admin.username)
    #     }
    # return "Invalid Login Details!"


@router.post("/")
async def admin_signup(admin: AdminModel = Body(...)):
    admin_data = admin_collection.find_one({"email":  admin.email})
    if(admin_data):
        return "Email already exists"

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(jsonable_encoder(admin))
    return new_admin
