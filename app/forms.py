from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TwigaAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Adresse e-mail ou mot de passe incorrect. Veuillez réessayer."
        ),
        "inactive": _("Ce compte est inactif."),
    }


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        label=_("Nom complet"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "contact-page__input form-control",
                "placeholder": _("Votre nom complet"),
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Adresse e-mail"),
        widget=forms.EmailInput(
            attrs={
                "class": "contact-page__input form-control",
                "placeholder": _("Votre adresse e-mail"),
                "autocomplete": "email",
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "class": "contact-page__input form-control",
                "placeholder": _("Choisissez un mot de passe"),
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Confirmer le mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "class": "contact-page__input form-control",
                "placeholder": _("Confirmez votre mot de passe"),
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_full_name(self):
        full_name = (self.cleaned_data.get("full_name") or "").strip()
        if len(full_name) < 2:
            raise ValidationError(_("Veuillez saisir votre nom complet."))
        return full_name

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(
            email=email
        ).exists():
            raise ValidationError(
                _("Un compte existe déjà avec cette adresse e-mail.")
            )
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                _("Les mots de passe ne correspondent pas."),
            )
        return cleaned_data

    def save(self):
        full_name = self.cleaned_data["full_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        parts = full_name.split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        return User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
