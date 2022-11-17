"""
    User database model serializer.
"""


from app.database.models.user import User


def serialize(user: User, allow_display_is_admin: bool = False, in_list: bool = False):
    """Returns dict object for API response with serialized user data."""

    serialized_user = {
        "id": user.id,
        "email": user.email
    }

    if allow_display_is_admin and user.is_admin:
        serialized_user |= {
            "is_admin": user.is_admin
        }
    
    if in_list:
        return serialized_user

    return {"user": serialized_user}


def serialize_list(users: list[User], allow_display_is_admins: bool = False) -> dict:
    """Returns dict object for API response with serialized users list data."""

    return {
        "users": [
            serialize(
                user=user, 
                allow_display_is_admin=allow_display_is_admins, 
                in_list=True
            ) 
            for user in users
        ]
    }


serialize_users = serialize_list
serialize_user = serialize