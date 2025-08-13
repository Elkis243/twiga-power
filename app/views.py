from django.shortcuts import render

def home(request):
    page = "Home"
    context = {
        'page': page
    }
    return render(request, 'app/home.html', context)

def contact(request):
    page = "Contact"
    context = {
        'page': page
    }
    return render(request, 'app/contact.html', context)


def employment(request):
    page = "Emploi"
    context = {
        'page': page
    }
    return render(request, 'app/employment.html', context)