"""
    User database model serializer.
"""


from app.database.models.user import User


def serialize(user: User, in_list: bool = False):
    """Returns dict object for API response with serialized user data."""

    serialized_user = {"id": user.id, "email": user.email}

    if in_list:
        return serialized_user

    return {"user": serialized_user}


def serialize_list(users: list[User]) -> dict:
    """Returns dict object for API response with serialized users list data."""

    return {"users": [serialize(user=user, in_list=True) for user in users]}


serialize_users = serialize_list
serialize_user = serialize
