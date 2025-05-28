from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from models import User
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import bcrypt


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
BASE_DIR = Path(__file__).parent.parent 
FRONTEND_DIR = BASE_DIR / "front-end"

app.mount("/front-end", StaticFiles(directory=FRONTEND_DIR), name="static")
    
@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        raise HTTPException(status_code=404, detail="Файл index.html не найден")
    
@app.get("/api/users")
async def get_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    return JSONResponse({"users": [user.username for user in users]})

@app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JSONResponse({"success": True, "message": "Вход выполнен!"})
    else:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")


@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Поля username и password обязательны")
    
    db: Session = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode('utf-8'))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return JSONResponse({"success": True, "message": "Регистрация успешна!"})
