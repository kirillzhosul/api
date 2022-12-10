"""
    Stuff for sending messages.
"""

from fastapi import BackgroundTasks

# Libraries.
from fastapi_mail import MessageSchema, MessageType

# Core.
from .config import fastmail
from app.config import get_logger
from app.database.models.course import Course
from app.database.models.user_course import UserCourse


async def send_custom_email(recepients: list[str], subject: str, body: str):
    """Sends message to single recipient email."""
    if not fastmail:
        return  # Mail disabled.

    recepients_count = len(recepients)
    get_logger().info(
        f"Sending e-mail to {recepients[0]}. '{subject}'."
        if recepients_count == 1
        else f"Sending e-mail to {recepients_count} recepients. '{subject}'."
    )
    await fastmail.send_message(
        MessageSchema(
            subject=subject, recipients=recepients, body=body, subtype=MessageType.plain
        )
    )


def send_purchase_success_email(
    background_tasks: BackgroundTasks,
    email: str,
    course: Course,
    user_course: UserCourse,
):
    """Send purchase complete email to the user."""
    subject = f"Success purchase! `{course.title}`"
    message = f"Hello, {email}! You are purchased course `{course.title}` for {user_course.purchased_for} rubles! Purchase ID: {user_course.id}"
    background_tasks.add_task(send_custom_email, [email], subject, message)
