from django.shortcuts import render
from . import models
def index(request):
    context = {"questions": models.QUESTIONS}
    return render(request, "index.html", context)


def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, "question.html", context)


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def singup(request):
    return render(request, "singup.html")
