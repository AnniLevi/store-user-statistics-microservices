from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import auth_schemas
from ..utils import jwt

auth_router = APIRouter()


@auth_router.post("/", response_model=auth_schemas.Token)
def login(api_key: str = Body(embed=True), db: Session = Depends(get_db)):
    access_token = jwt.authenticate_consumer(db=db, api_key=api_key)
    return {"access_token": access_token, "token_type": "Bearer"}
