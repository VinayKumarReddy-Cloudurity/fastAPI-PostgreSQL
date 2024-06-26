from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import User, Question, Response
from schemas import UserCreate, QuestionCreate, ResponseCreate

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_question(db: AsyncSession, question: QuestionCreate):
    db_question = Question(text=question.text)
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question

async def create_response(db: AsyncSession, response: ResponseCreate):
    db_response = Response(user_id=response.user_id, question_id=response.question_id, answer=response.answer)
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

async def get_questions(db: AsyncSession):
    result = await db.execute(select(Question))
    return result.scalars().all()
