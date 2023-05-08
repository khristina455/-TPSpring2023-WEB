from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from . import models


def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    questions = models.QUESTIONS
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj, 'title': 'New Questions'}
    return render(request, 'index.html', context)


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


def tag(request, tag):
    TAGQUESTIONS = []
    for q in models.QUESTIONS:
        for t in q.get('tags'):
            if tag == t:
                TAGQUESTIONS.append(q)

    context = {"questions": TAGQUESTIONS, "title": f"Tag: {tag}"}
    return paginate(context, request)



