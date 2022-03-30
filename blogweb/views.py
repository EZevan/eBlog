from django.shortcuts import render


# Create your views here.
def index(request):
    header_img_list = [
        "/static/assets/img/header/g-class1.png",
        "/static/assets/img/header/g-class2.png",
        "/static/assets/img/header/g-class3.png",
        "/static/assets/img/header/g-class4.png"
    ]
    return render(request, 'index.html', {"img_list": header_img_list})
