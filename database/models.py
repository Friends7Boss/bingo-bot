# database/models.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    balance = Column(Numeric(10,2), default=0)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    referral_code = Column(String, unique=True, nullable=True)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    referrals = relationship("User", remote_side=[id])

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(10,2))
    transaction_id = Column(String, index=True)
    sender_phone = Column(String)
    status = Column(String, default="pending")  # pending|approved|rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(10,2))
    phone_number = Column(String)
    status = Column(String, default="pending")  # pending|approved|rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    entry_price = Column(Integer)
    total_pool = Column(Numeric(12,2), default=0)
    status = Column(String, default="open")  # open|running|closed
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Cartela(Base):
    __tablename__ = "cartelas"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    cartela_number = Column(Integer)  # 1..100
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ReferralLog(Base):
    __tablename__ = "referral_logs"
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_id = Column(Integer, ForeignKey("users.id"))
    bonus_amount = Column(Numeric(10,2))
    granted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
