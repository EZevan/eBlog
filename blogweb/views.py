from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from blogweb.utils.gen_captcha import gen_captcha


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
    if request.method == "POST":
        data = request.data
        return JsonResponse(data)

    captcha = request.session.get("captcha")

    return render(request, "login.html")


def get_captcha(request):
    data, captcha = gen_captcha()
    request.session["captcha"] = captcha

    return HttpResponse(data)


def register(request):
    return render(request, "register.html")
