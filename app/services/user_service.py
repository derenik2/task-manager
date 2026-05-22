from ..extensions import db
from ..models.user import User


def get_all_users() -> list[User]:
    return db.session.execute(db.select(User)).scalars().all()


def get_user_by_id(user_id: int) -> User | None:
    return db.session.get(User, user_id)


def create_user(username: str, email: str) -> User:
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(user_id: int) -> bool:
    user = get_user_by_id(user_id)
    if user is None:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
