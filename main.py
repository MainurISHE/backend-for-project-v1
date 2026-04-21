from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

# Создаем таблицы при старте
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bug Tracker API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для получения доступа к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "Working", "docs": "/docs"}

@app.post("/api/bugs", response_model=schemas.BugReportResponse)
def create_bug(bug: schemas.BugReportCreate, db: Session = Depends(get_db)):
    db_bug = models.BugReport(**bug.model_dump())
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug

@app.get("/api/bugs", response_model=List[schemas.BugReportResponse])
def get_bugs(db: Session = Depends(get_db)):
    return db.query(models.BugReport).all()