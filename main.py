from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from os import path

pth = path.dirname(__file__)

app = FastAPI()

SECRET = "965d46a450c5d9752606fb0164d3a998e65748b3efe4047e"
manager = LoginManager(SECRET, token_url= '/auth/login', use_cookie=True)
manager.cookie_name="api-names"


DB = {
    "username":{
        "password":"qwertyuiop"
    }
}

@manager.user_loader()
def load_user(username:str):
    user= DB.get(username)
    return user

@app.get("/auth/login")
async def login(data: OAuth2PasswordRequestForm =Depends()):
    username = data.username
    password = data.password
    
    user = load_user(username)
    
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={
            "sub": username
        }
    )
    resp = RedirectResponse(url='/private', status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get("/private")
async def getPrivatePoint(_=Depends(manager)):
    return "You are an authenticated user"




@app.get("/", response_class=HTMLResponse)
async def loginwithCreds(request:Request):
    with open(path.join(pth, "templates/login.html")) as f:
        return HTMLResponse(content=f.read())