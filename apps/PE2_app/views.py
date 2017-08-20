from django.shortcuts import render, redirect
# from .models import User, Plan
from django.contrib import messages

#create views here
def index(request):
    return render(request, "PE2_app/index.html")
