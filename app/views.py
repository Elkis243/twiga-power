from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse


def home(request):
    page = "Home"
    context = {"page": page}
    return render(request, "app/home.html", context)


def contact(request):
    page = "Contact"
    context = {"page": page}

    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            send_mail(
                subject,
                message,
                email,  # l'expéditeur = email de l'utilisateur
                [settings.EMAIL_HOST_USER],  # le destinataire = ton email
                fail_silently=False,
            )
            messages.success(
                request,
                "Votre message a été envoyé avec succès. Nous vous répondrons bientôt !",
            )
            return HttpResponseRedirect("/contact/")  # redirection après envoi réussi

        except Exception as e:
            messages.error(
                request,
                f"Une erreur s'est produite lors de l'envoi de votre message : {str(e)}",
            )
            return HttpResponseRedirect("/contact/")  # redirection après échec

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
