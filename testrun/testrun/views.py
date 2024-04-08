from django.shortcuts import render

def home(request):
    return render(request,'index.html')

def basic(request):
    return render(request,'basic.html')

def advanced(request):
    return render(request,'advanced.html')

