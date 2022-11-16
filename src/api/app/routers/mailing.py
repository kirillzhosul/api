"""
    Mailing API router.
    Provides API methods (routes) for working with admin mailing.
"""

from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import query_auth_data_from_request
from app.database.dependencies import get_db, Session
from app.database import crud
from app.email.messages import send_custom_email
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/mailing/send")
async def method_mailing_send(
    req: Request, background_tasks: BackgroundTasks,
    subject: str = "", message: str = "",
    mailing_group_id: int | None = None,
    skip_create_task: bool = False, 
    display_recepients: bool = False,
    admins_only: bool = False, 
    db: Session = Depends(get_db)
) -> JSONResponse:
    """Creates new mailing task (Permitted only)."""

    auth_data = query_auth_data_from_request(req, db)
    if not auth_data.user.is_admin:
        return api_error(ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!")
    
    if not subject or not message:
        return api_error(ApiErrorCode.API_INVALID_REQUEST, "Subject and message required!")

    if mailing_group_id:
        users = []
        return api_error(ApiErrorCode.API_ITEM_NOT_FOUND, "Mailing group is not found yet...")
    else:
        users = crud.user.get_all(db, admins_only=admins_only)
    # Doing database requests like that is not good!
    recepients = [user.email for user in users]

    if not skip_create_task:
        background_tasks.add_task(send_custom_email, recepients, subject, message)

    return api_success({
        "total_recepients": len(recepients),
        "task_created": skip_create_task
    } | {
        "recepients": recepients
    } if display_recepients else {})
