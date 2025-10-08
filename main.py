from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, Spa as SpaModel, Review as ReviewModel, User as UserModel


# DB 세션 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# 데이터 유효성 검사/응답을 위한 Pydantic 모델
class SpaBase(BaseModel):

    name: str
    address: str
    latitude: float
    longitude: float
    operating_hours: str
    price: str
    phone_number: str
    description: str
    image_url: str

class Spa(SpaBase):
    id: int
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    user_id: int
    spa_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    spa_id: int
    created_at: datetime
    class Config:
        orm_mode = True


# --- 온천(Spa) 관련 API ---
@app.get("/spas/", response_model=List[Spa])
def get_spas(db: Session = Depends(get_db)):
    spas = db.query(SpaModel).all()
    return spas

@app.get("/spas/{spa_id}", response_model=Spa)
def get_spa(spa_id: int, db: Session = Depends(get_db)):
    spa = db.query(SpaModel).filter(SpaModel.id == spa_id).first()
    if spa is None:
        raise HTTPException(status_code=404, detail="Spa not found")
    return spa

# -- 리뷰(Review) 관련 API (CRUD) ---
@app.post("/reviews/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # user_id와 spa_id 유효성 확인 (실제로는 인증 로직이 필요)
    user = db.query(UserModel).filter(UserModel.id == review.user_id).first()
    if not user:
            raise HTTPException(status_code=404, detail="User not found")
    spa = db.query(SpaModel).filter(SpaModel.id == review.spa_id).first()
    if not spa:
        raise HTTPException(status_code=404, detail="Spa not found")

    db_review = ReviewModel(
        rating=review.rating,
        comment=review.comment,
        user_id=review.user_id,
        spa_id=review.spa_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/spas/{spa_id}/reviews/", response_model=List[Review])
def get_spa_reviews(spa_id: int, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.spa_id == spa_id).all()
    return reviews

@app.put("/reviews/{review_id}", response_model=Review)
def update_review(review_id: int, review_data: ReviewBase, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # 예시: 현재는 user_id 검증 생략, 실제로는 로그인한 사용자와 비교해야 함

    db_review.rating = review_data.rating
    db_review.comment = review_data.comment
    db.commit()
    db.refresh(db_review)
    return db_review

@app.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return None


@app.get("/")
def read_root():
    return {"Hello": "World"}