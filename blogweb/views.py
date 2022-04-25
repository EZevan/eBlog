import json

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
    password = forms.CharField(max_length=128, error_messages={"required": "请输入密码", "max_length": "超过最大字符限制"})
    captcha = forms.CharField(max_length=4, error_messages={"required": "请输入验证码", "max_length": "超过最大字符限制"})

    # overwrite __init__ method to deliver http request object
    def __init__(self, *args, **kwargs):
        # Here we can use the pop method to get http request object which won't be passed to base class
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        form global hooks - to validate multiple fields
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # TODO: test data to validate username and password
        if username != "test" or password != "test":
            # add incorrect field
            self.add_error("username", "用户名或密码错误")

        return self.cleaned_data

    def clean_captcha(self):
        """
        form partial hook - to validate specified field
        """
        captcha: str = self.cleaned_data.get("captcha")
        session_captcha: str = self.request.session.get("captcha")
        print(captcha, session_captcha)

        if captcha.lower() != session_captcha.lower():
            self.add_error("captcha", "验证码输入错误")

        return self.cleaned_data


def form_validation(form):
    if form is not None:
        # all form validation errors
        errors: dict = form.errors
        # the first error field of all error fields
        error_field = list(errors.keys())[0]
        # the first error message of the first error field
        error_msg = errors[error_field][0]

        return error_field, error_msg


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

        form = LoginForm(data, request=request)

        if not form.is_valid():
            error_field, error_msg = form_validation(form)

            res["arguments"] = error_field
            res["msg"] = error_msg
            res["code"] = -1

            return JsonResponse(res)

        return JsonResponse(res)

    return render(request, "login.html")


def get_captcha(request):
    data, captcha = gen_captcha()
    print("captcha: " + captcha)
    request.session["captcha"] = captcha

    return HttpResponse(data)


def register(request):
    return render(request, "register.html")
