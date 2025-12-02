from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    balance = Column(Float, default=0)
    referred_by = Column(BigInteger, nullable=True)
    total_games = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True)
    referrer_id = Column(BigInteger, nullable=False)
    referred_id = Column(BigInteger, nullable=False)
    bonus_given = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    amount = Column(Float, nullable=False)
    phone = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending / approved / rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending / approved / denied
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    status = Column(String, default="waiting")  # waiting / active / finished
    pool = Column(Float, default=0)
    winner_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    user_id = Column(BigInteger)
    cart_number = Column(Integer)  # 1–100
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
