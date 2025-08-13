from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail


def send_contact_email(request, *args, **kwargs):
    recipient = kwargs.get("email")
    objet = kwargs.get("objet")
    message = kwargs.get("message")
    sender = settings.EMAIL_HOST_USER

    try:
        send_mail(
            subject=objet,
            message=message,
            from_email=sender,
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(
            request,
            "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
        )
    except Exception as e:
        messages.error(
            None,
            f"Une erreur s'est produite lors de l'envoi de votre message : {str(e)}",
        )
