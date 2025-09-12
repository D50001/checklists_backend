import os
from uuid import UUID

from celery import shared_task
import logging

from orders.models import Order
from .models import Check, Element
from open_ai.manager import OpenAIManager
from auto_checklist.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)



@shared_task
def transcribe_call_and_add_comment(
        order_id: UUID,
        element_id: int,
        file_path: str
) -> None:
    openai_manager = OpenAIManager()
    try:
        transcript = openai_manager.transcribe(os.path.join(MEDIA_ROOT, file_path))
        logging.info(transcript)
    except Exception as e:
        logging.warning(e)
        transcript = "Не удалось распознать аудио"

    check, _ = Check.objects.update_or_create(
        order=Order.objects.get(id=order_id),
        element=Element.objects.get(id=element_id),
        defaults={
            'state': 'NOT_OK',
            'comment': transcript,
        }
    )
    return None