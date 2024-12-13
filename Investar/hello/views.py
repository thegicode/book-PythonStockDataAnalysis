from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def sayHello(request, name):
    html = f"<h1>Hello, {name}</h1>"
    return HttpResponse(html)