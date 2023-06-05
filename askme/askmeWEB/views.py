from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from . import models


def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def context_for_sidebar(context):
    context['top_tags'] = models.Tag.objects.get_top5()
    context['top_users'] = models.Profile.objects.get_top5()


def index(request):
    questions = models.Question.objects.new_questions()
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj, 'title': 'New Questions'}
    context_for_sidebar(context)
    return render(request, 'index.html', context)


def hot(request):
    questions = models.Question.objects.hot_questions()
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj, 'title': 'Hot Questions'}
    context_for_sidebar(context)
    return render(request, 'index.html', context)


def question(request, question_id):
    question = models.Question.objects.get_question(question_id)
    if question == None:
        raise Http404("Question does not exist")
    answers = models.Answer.objects.get_by_question(question_id)
    page_obj = paginate(answers, request, 3)
    context = {'question': question, 'page_obj':page_obj}
    context_for_sidebar(context)
    return render(request, "question.html", context)


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def singup(request):
    return render(request, "singup.html")


def tag(request, tag):
    questions = models.Question.objects.tag_questions(models.Tag.objects.get_by_title(tag))
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj, 'title': f'Tag:{tag} Questions'}
    context_for_sidebar(context)
    return render(request, 'index.html', context)
