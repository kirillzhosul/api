"""
    Mailing API router.
    Provides API methods (routes) for working with admin mailing.
"""

from app.services.api.response import api_error, ApiErrorCode, api_success
from app.services.request.auth import try_query_auth_data_from_request
from app.database.dependencies import get_db, Session
from app.database import crud
from app.email.messages import send_custom_email
from fastapi import APIRouter, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/appeals/submit")
async def method_appeals_submit(
    req: Request, background_tasks: BackgroundTasks,
    text: str = "", email: str = "",
    db: Session = Depends(get_db)
) -> JSONResponse:
    """Creates new mailing task (Permitted only)."""

    is_authenticated, auth_data = try_query_auth_data_from_request(req, db)
    system_user_id = auth_data.user_id if is_authenticated else None

    # Doing database requests like that is not good!
    recepients = [user.email for user in crud.user.get_all(db, admins_only=True)]
    notification_subject = "New appeal submitted!"
    notification_message = \
        "New appeal has been submitted!" \
        f"{'UID: ' + str(system_user_id) if system_user_id else ''} " \
        f"{'Email: ' + email if email else ''} Text: {text};"

    for recepient in recepients:
        # Bad!
        background_tasks.add_task(
            send_custom_email, 
            [recepient], 
            notification_subject,
            notification_message
        )

    return api_success({})

