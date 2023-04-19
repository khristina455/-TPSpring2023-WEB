from django.db import models

QUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question {i}',
        'text': f'Lorem ipsum dolor sit, amet consectetur '
                 f'adipisicing elit.Modi maiores tempore doloremque '
                 f'provident animi numquam,commodi rerum voluptatibus soluta neque?',
        'rating': f'{i + 10}',
        'tags': ['C++', 'SQL']
    } for i in range(12)
]

HOTQUESTIONS = [
    {
        'id': f'{i}',
        'title': f'Question {i}',
        'text': f'Lorem ipsum dolor sit, amet consectetur '
                 f'adipisicing elit.Modi maiores tempore doloremque '
                 f'provident animi numquam,commodi rerum voluptatibus soluta neque?'
    } for i in range(12)
]


