from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from .utils import send_contact_email



def home(request):
    page = "Home"
    context = {"page": page}
    return render(request, "app/home.html", context)


def contact(request):
    page = "Contact"
    context = {"page": page}
    if request.method == "POST":
        recipient = request.POST.get("email")
        objet = request.POST.get("objet")
        message = request.POST.get("message")

        send_contact_email(
            request,
            email=recipient,
            objet=objet,
            message=message,
        )
        print(recipient, objet, message)
        return HttpResponseRedirect("/contact/")
    return render(request, "app/contact.html", context)


def employment(request):
    page = "Emploi"
    context = {"page": page}
    return render(request, "app/employment.html", context)
