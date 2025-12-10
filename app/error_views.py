from django.shortcuts import render


def handler400(request, exception):
    """Vue personnalisée pour l'erreur 400"""
    return render(request, "400.html", status=400)


def handler403(request, exception):
    """Vue personnalisée pour l'erreur 403"""
    return render(request, "403.html", status=403)


def handler404(request, exception):
    """Vue personnalisée pour l'erreur 404"""
    return render(request, "404.html", status=404)


def handler500(request):
    """Vue personnalisée pour l'erreur 500"""
    return render(request, "500.html", status=500)
