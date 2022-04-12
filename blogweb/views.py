from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def article(request):
    return render(request, "article.html")


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")
