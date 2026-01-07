#different security rules to different endpoints using FastAPI
from fastapi import FastAPI, HTTPException
app = FastAPI()
 
users = {
    "GVV": {"password": "pwd1", "role": "user"},
    "GVV2": {"password": "pwd2", "role": "admin"}
}
def authenticate(username: str, password: str):
    user = users.get(username)
    if user and user["password"] == password:
        return user
 
@app.get("/public-info")
def public_info():
    return {"Everyone can access"}
 
@app.get("/user")
def user_info(username: str, password: str):
    user = authenticate(username, password)
    if not user:
        raise HTTPException(401, "Unauthorized")
    return {"Hello user"}
 
@app.get("/admin")
def admin(username: str, password: str):
    user = authenticate(username, password)
    if not user:
        raise HTTPException(401, "Unauthorized")
    if user["role"] != "admin":
        raise HTTPException(403, "Admin only")
    return {"Hello admin"}
 
 