from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite를 임시로 사용하지만, PostgreSQL로 쉽게 변경 가능합니다.
# PostgreSQL을 사용하려면 URLdmf 'postgresql://user:password@host:port/dbname' 형식으로 변경하세요.
SQLALCHEMY_DATABASE_URL = "sqlite:///./spa.db"  # 로컬 파일에 DB 생성

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB 모델 정의 (테이블 스키마)
class Spa(Base):
    __tablename__ = "spas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    operating_hours = Column(String)
    price = Column(String)
    phone_number = Column(String)
    description = Column(Text)
    image_url = Column(String)

    reviews = relationship("Review", back_populates="spa")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    reviews = relationship("Review", back_populates="user")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)

    # 외래 키 설정
    user_id = Column(Integer, ForeignKey("users.id"))
    spa_id = Column(Integer, ForeignKey("spas.id"))

    # 관계 설정
    user = relationship("User", back_populates="reviews")
    spa = relationship("Spa", back_populates="reviews")

