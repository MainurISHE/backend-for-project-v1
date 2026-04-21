from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Добавили для связи с фронтом
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

# Автоматическое создание базы данных и таблиц при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bug Tracker API",
    description="API для системы регистрации багов (тестовый проект)",
    version="1.0.0"
)

# Настройка CORS, чтобы React мог делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешить все адреса (для теста это ок)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency для базы
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API is running. Go to /docs to see the UI"}

@app.post("/api/bugs", response_model=schemas.BugReportResponse)
def create_bug_report(bug: schemas.BugReportCreate, db: Session = Depends(get_db)):
    new_bug = models.BugReport(
        email=bug.email,
        author=bug.author,
        release_build_no=bug.release_build_no,
        fixed_by=bug.fixed_by,
        open_date=bug.open_date,
        close_date=bug.close_date,
        description=bug.description,
        priority=bug.priority.value,
        severity=bug.severity.value,
        defect_types=bug.defect_types
    )
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug

@app.get("/api/bugs")
def get_all_bugs(db: Session = Depends(get_db)):
    return db.query(models.BugReport).all()