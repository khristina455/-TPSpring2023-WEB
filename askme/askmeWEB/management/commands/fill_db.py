from django.core.management.base import BaseCommand
from askmeWEB.models import Like, Tag, User, Profile, Question, Answer
from random import randint, choice
from faker import Faker
import random
from django.db.models import Sum


class Command(BaseCommand):
    help = '''Set ratio and fill DB
            - ratio tags
            - ratio users
            - ratio*10 questions
            - ratio*100 answers
            - ratio*200 likes'''

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='bd filling coefficient')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        USERS = ratio
        QUESTIONS = ratio * 10
        ANSWERS = ratio * 100
        TAGS = ratio
        LIKES = ratio * 200

        fake = Faker()

        tags = [Tag(title=f"tag{i}") for i in range(TAGS)]
        Tag.objects.bulk_create(tags)
        tags = Tag.objects.all()
        self.stdout.write("Tags filled\n")

        avatars = ["1.png", "2.jpeg", "3.png", "4.jpg", "5.jpg"]
        avatars = [f"static/img/avatar/user{avatar}" for avatar in avatars]
        User.objects.create_user(**self.cleaned_data)
        users = [User.objects.create_user(id=i + 2, username=f"username{i + 2}", first_name=fake.first_name(), last_name=fake.last_name(),
                      password=fake.password()) for i in range(USERS)]
        User.objects.bulk_create(users)
        users = User.objects.exclude(is_superuser=True)

        profiles = [Profile(user=user, avatar=random.choice(avatars)) for user in users]
        Profile.objects.bulk_create(profiles)
        profiles = Profile.objects.all()
        self.stdout.write("Profiles filled\n")

        questions = [Question(author=random.choice(profiles),
                              title=f"Question{i}",
                              content=fake.text()[:150],
                              create_date=fake.date_time(),
                              ) for i in range(QUESTIONS)]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()
        for i in range(QUESTIONS):
            questions[i].tags.set([tags[i * randint(1, 10) % TAGS] for _ in range(randint(1, 4))])

        questions = Question.objects.all()
        self.stdout.write("Questions filled\n")

        likes = [Like(to_question=random.choice(questions), from_user=random.choice(profiles)) for _ in range(LIKES)]
        Like.objects.bulk_create(likes)
        self.stdout.write("Likes filled\n")

        for i in range(QUESTIONS):
            q = Question.objects.get(pk=questions[i].id)
            q.rating = q.likes.all().count()
            q.save()

        for i in range(USERS):
            p = Profile.objects.get(pk=profiles[i].id)
            p.rating = p.questions.all().aggregate(sum=Sum('rating'))['sum']
            if p.rating == None:
                p.rating = 0
            p.save()

        answers = [Answer(author=random.choice(profiles),
                          question=random.choice(questions),
                          content=fake.text()[:150],
                          create_date=fake.date_time(),
                          ) for i in range(ANSWERS)]
        Answer.objects.bulk_create(answers)

        self.stdout.write("Answers filled\n")
