"""
    Roles API router.
    Provides API methods (routes) for working with roles.
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from app.database.models.user_role import UserRole


router = APIRouter()


@router.get("/roles")
async def method_roles_list(
    req: Request, db: Session = Depends(get_db)
) -> JSONResponse:
    """Returns all roles."""
    user = query_auth_data_from_request(req, db).user
    if not user.role.p_manage_roles:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    return api_success(
        {
            "roles": [
                {
                    "name": role.name,
                    "id": role.id,
                    "permisions": {
                        k: v
                        for k, v in role.__dict__.items()
                        if isinstance(k, str) and k.startswith("p_")
                    },
                }
                for role in db.query(UserRole).all()
            ]
        }
    )
