from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """Authentifie uniquement avec l'adresse e-mail du compte."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        email = username.strip()
        if not email or "@" not in email:
            return None

        password_value = password.strip() if isinstance(password, str) else password

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            User().set_password(password_value)
            return None

        if user.check_password(password_value) and self.user_can_authenticate(user):
            return user
        return None
