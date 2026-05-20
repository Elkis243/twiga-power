from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Authentifie avec le nom d'utilisateur CLI (ex. admin) ou l'e-mail du compte.
    Nécessaire car l'inscription du site utilise l'e-mail comme username,
    alors que createsuperuser définit souvent un username distinct.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        login = username.strip()
        if not login:
            return None

        password_value = password.strip() if isinstance(password, str) else password

        user = None
        if "@" in login:
            user = User.objects.filter(email__iexact=login).first()
        if user is None:
            user = User.objects.filter(username__iexact=login).first()

        if user is None:
            User().set_password(password_value)
            return None

        if user.check_password(password_value) and self.user_can_authenticate(user):
            return user
        return None
