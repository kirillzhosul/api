"""
    User CRUD utils for the database.
"""

from sqlalchemy.orm import Session
from app.database.models.user import User


def get_by_id(db: Session, user_id: str) -> User:
    """Returns user by it`s ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_by_sso_oauth_user_id(db: Session, sso_oauth_user_id: str) -> User:
    """Returns user by OAuth SSO ID."""
    return db.query(User).filter(User.sso_oauth_user_id == sso_oauth_user_id).first()


def get_all(db: Session) -> list[User]:
    """Returns all users."""
    return db.query(User).all()


def create(db: Session, sso_oauth_user_id: int, email: str | None = None) -> User:
    """Creates new user."""

    # Create new user.
    user = User(sso_oauth_user_id=sso_oauth_user_id, email=email)

    # Apply user in database.
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_or_create(db: Session, user_id: str, email: str | None = None) -> User:
    """Creates or returns already created user."""
    user = get_by_id(db, user_id)
    if user is None:
        return create(db, user_id=user_id, email=email)
    return user
