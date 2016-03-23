from django.shortcuts import render

# Create your views here.

def notice_index(req):
    return render(req, 'notice_main.html')