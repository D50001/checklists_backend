from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username_or_email = kwargs.get("username", None)
        if username_or_email is not None:
            try:
                user = get_user_model().objects.get(
                    Q(username=username_or_email) | Q(email=username_or_email)
                )
                if user.check_password(kwargs.get("password", None)):
                    return user
            except get_user_model().DoesNotExist:
                return None
        return None