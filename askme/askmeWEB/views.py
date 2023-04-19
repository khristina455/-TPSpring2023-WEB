from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from . import models


def index(request):
    context = {"questions": models.QUESTIONS, "title": "New Questions"}
    return paginate(context, request)


def hot(request):
    context = {"questions": models.HOTQUESTIONS, "title": "Hot Questions"}
    return paginate(context, request)


def question(request, question_id):
    try:
        context = {'question': models.QUESTIONS[question_id]}
    except:
        raise Http404("Question does not exist")
    return render(request, "question.html", context)


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def singup(request):
    return render(request, "singup.html")


def tag(request, tag_name):
    TAGQUESTIONS = []
    for q in models.QUESTIONS :
        for t in q.get('tags'):
            if tag_name == t:
                TAGQUESTIONS.append(q)

    context = {"questions": TAGQUESTIONS, "title": f"Tag: {tag_name}"}
    return paginate(context, request)


def paginate(context, request, per_page=3):
    paginator = Paginator(context.get("questions"), per_page)
    page_number = request.GET.get("page")
    context["questions"] = paginator.get_page(page_number)
    page = render(request, "index.html", context)
    return page
