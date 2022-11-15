"""
    User CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.user import User


def get_by_id(db: Session, user_id: int) -> User:
    """Returns user by it`s ID."""
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, user_id: int, email: str | None = None) -> User:
    """Creates new user."""

    # Create new user.
    user = User(id=user_id, email=email)

    # Apply user in database.
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_or_create(db: Session, user_id: int, email: str | None = None) -> User:
    """Creates or returns already created user."""
    user = get_by_id(db, user_id)
    if user is None:
        return create(db, user_id=user_id, email=email)
    return 
