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
    req: Request,
    background_tasks: BackgroundTasks,
    subject: str = "",
    message: str = "",
    mailing_group_id: int | None = None,
    skip_create_task: bool = False,
    display_recepients: bool = False,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Creates new mailing task (Permitted only)."""

    user = query_auth_data_from_request(req, db).user
    if not user.role.p_manage_mailings:
        return api_error(
            ApiErrorCode.API_FORBIDDEN, "You have no access to call this method!"
        )

    if not subject or not message:
        return api_error(
            ApiErrorCode.API_INVALID_REQUEST, "Subject and message required!"
        )

    if mailing_group_id:
        users = []
        return api_error(
            ApiErrorCode.API_ITEM_NOT_FOUND, "Mailing group is not found yet..."
        )
    else:
        users = crud.user.get_all(db)
    # Doing database requests like that is not good!
    recepients = [user.email for user in users]

    if not skip_create_task:
        for recepient in recepients:
            # Bad!
            background_tasks.add_task(send_custom_email, [recepient], subject, message)

    response = {
        "total_recepients": len(recepients),
        "task_created": not skip_create_task,
    }
    if display_recepients:
        response |= {"recepients": recepients}
    return api_success(response)
