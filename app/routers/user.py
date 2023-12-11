from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from ..database import engine, SessionLocal,get_db
from .. import models, schemas , utils
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    try:
        # Yeni kullanıcı oluşturma işlemi
        new_user= models.User(
        email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
    # Eğer eşsizlik kuralı ihlal edilirse (aynı e-posta ile kayıtlı bir kullanıcı varsa)
    # HTTP 409 hatası döndürülür
        raise HTTPException(status_code=409, detail="User with this email already exists")
 
@router.get("/{id}",response_model=schemas.UserOut)
def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} was a not found")
    return user