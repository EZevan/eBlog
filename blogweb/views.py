from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from blogweb.utils.gen_captcha import gen_captcha
from django import forms


# Create your views here.
def index(request):
    return render(request, "index.html")


def news(request):
    return render(request, "news.html")


def article(request):
    return render(request, "article.html")


def about(request):
    return render(request, "about.html")


# CFV Class base view
class LoginForm(forms.Form):
    """
    CFV - form validation
    """
    username = forms.CharField(max_length=150, error_messages={"required": "请输入用户名", "max_length": "超过最大字符限制"})
    password = forms.CharField(max_length=128,  error_messages={"required": "请输入密码", "max_length": "超过最大字符限制"})
    captcha = forms.CharField(max_length=4, error_messages={"required": "请输入验证码", "max_length": "超过最大字符限制"})


def login(request):
    """
    Login logic
    """
    if request.method == "POST":
        res = {
            "code": 0,
            "msg": "登录成功",
            "arguments": None
        }
        data = request.data

        form = LoginForm(data)

        if not form.is_valid():
            errors: dict = form.errors
            error_field = list(errors.keys())[0]

            res["msg"] = errors[error_field][0]
            res["arguments"] = error_field
            res["code"] = -1

            return JsonResponse(res)

        return JsonResponse(data)

    captcha = request.session.get("captcha")

    return render(request, "login.html")


def get_captcha(request):
    data, captcha = gen_captcha()
    request.session["captcha"] = captcha

    return HttpResponse(data)


def register(request):
    return render(request, "register.html")
