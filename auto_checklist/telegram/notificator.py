from auto_checklist.settings import(
    TELEGRAM_BOT_TOKEN
)
import requests
import logging
from orders.models import Department
from rest_framework.exceptions import ValidationError


class TelegramNotificator:
    def __init__(self):
        self.telegram_token = TELEGRAM_BOT_TOKEN

    def send_order_notification(self, attrs: dict, order_id: str):

        url = f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
        model = attrs.get("model")
        license_number = attrs.get("license_number", "")

        keyboard = self._get_order_keyboard(order_id, model, license_number)
        text = f"Автомобиль к осмотру {model} {license_number}"

        department = attrs.get("department")
        telegram_id = self._get_department_id(department)
        payload = {
            "chat_id": telegram_id,
            'text': text,
            'reply_markup': keyboard
        }
        try:
            response = requests.post(url, json=payload)
        except Exception as e:
            logging.debug(e)
            return
        if response.status_code != 200:
            logging.debug(response.content)
        else:
            logging.info(response.content)


    @staticmethod
    def _get_order_keyboard(order_id: str, model:str, license_number: str):
        return {
            "inline_keyboard": [
                [
                    {
                        "text": "Чеклист для автомобиля",
                        "callback_data": f"auto:{order_id}:{license_number}"
                    }
                ],
                [
                    {
                        "text": "Быстрый чеклист",
                        "callback_data": f"fast:{order_id}:{license_number}"
                    }
                ]
            ]
        }

    @staticmethod
    def _get_department_id(department):
        try:
            department_id = Department.objects.get(title=department).telegram_chat_id
        except Department.DoesNotExist:
            raise ValidationError(f"No department {department} found")
        return department_id
