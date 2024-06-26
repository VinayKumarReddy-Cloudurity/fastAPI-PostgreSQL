from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

import models
import schemas

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/survey_tool"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = models.Base

app = FastAPI()

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.post("/questions/", response_model=schemas.Question)
async def create_question(question: schemas.QuestionCreate, db: AsyncSession = Depends(get_db)):
    db_question = models.Question(text=question.text)
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question

@app.post("/responses/", response_model=schemas.Response)
async def create_response(response: schemas.ResponseCreate, db: AsyncSession = Depends(get_db)):
    db_response = models.Response(user_id=response.user_id, question_id=response.question_id, response=response.response)
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

@app.post("/survey/", response_model=schemas.User)
async def submit_survey(survey: schemas.SurveyResponse, db: AsyncSession = Depends(get_db)):
    try:
        # Create user
        db_user = models.User(name=survey.user.name, email=survey.user.email)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        # Create responses
        for response in survey.responses:
            db_response = models.Response(user_id=db_user.id, question_id=response.question_id, response=response.response)
            db.add(db_response)
        
        await db.commit()

        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error saving survey response")

