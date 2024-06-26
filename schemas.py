from pydantic import BaseModel
from typing import List

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ResponseBase(BaseModel):
    response: str
    question_id: int

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class SurveyResponse(BaseModel):
    user: UserCreate
    responses: List[ResponseCreate]
