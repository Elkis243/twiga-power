from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse


def home(request):
    page = "Home"
    context = {"page": page}
    return render(request, "app/home.html", context)


def contact(request):
    page = "Contact"
    context = {"page": page}

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("telephone")
        address = request.POST.get("address")
        message = request.POST.get("message")

        subject = f"Nouveau message de {name}"
        body = (
            f"Nom: {name}\n"
            f"Email: {email}\n"
            f"Téléphone: {phone}\n"
            f"Adresse: {address}\n\n"
            f"Message:\n{message}"
        )

        try:
            mail = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,   # ✅ ton mail hostinger
                to=[settings.EMAIL_HOST_USER],         # ✅ destinataire (toi-même)
                reply_to=[email],                      # ✅ pour pouvoir répondre au visiteur
            )
            mail.send(fail_silently=False)

            messages.success(
                request,
                "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
            )
            return HttpResponseRedirect("/contact/")

        except Exception as e:
            messages.error(
                request,
                f"Une erreur est survenue lors de l'envoi du message : {e}",
            )
            return HttpResponseRedirect("/contact/")

    return render(request, "app/contact.html", context)


def employment(request):
    page = "Emploi"
    context = {"page": page}
    return render(request, "app/employment.html", context)


def about(request):
    page = "A propos"
    context = {"page": page}
    return render(request, "app/about.html", context)


def robots_txt(request):
    content = """
User-agent: *
Disallow: /admin/
Sitemap: https://www.twigapower.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
