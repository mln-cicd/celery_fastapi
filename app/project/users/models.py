from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from app.project.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    
    def __init__(self, username, email, *args, **kwargs):
        self.username = username
        self.email = email
        
        
    