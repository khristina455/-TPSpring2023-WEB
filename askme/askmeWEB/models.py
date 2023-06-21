from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist


class ProfileManager(models.Manager):
    def get_top5(self):
        return self.order_by('-rating')[:5]

    def get_user_by_username(self, username):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None
        return user

    def get_profile_by_user_id(self, uid):
        try:
            user = User.objects.get(id=uid)
        except ObjectDoesNotExist:
            return None
        profile = Profile.objects.get(user=user)
        return profile

    def set_rating(self, profile):
        print("fssfk")
        profile.rating = profile.questions.all().aggregate(sum=Sum('rating'))['sum']
        print(profile.rating)
        if profile.rating == None:
            profile.rating = 0
        profile.save()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/%d/', default='index.jpeg')
    rating = models.IntegerField(default=0)

    objects = ProfileManager()

    def __str__(self):
        return f'({self.id}) {self.user.username}'

    def liked_questions(self):
        liked = [el.to_question for el in self.likes.filter(type="+")]
        print("like")
        print(liked)
        return liked

    def disliked_questions(self):
        disliked = [el.to_question for el in self.likes.filter(type="-")]
        print(disliked)
        return disliked


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-create_date')

    def hot_questions(self):
        return self.order_by('-rating')

    def tag_questions(self, tag):
        return self.filter(tags=tag).order_by('-rating')

    def get_question(self, qid):
        try:
            q = self.get(pk=qid)
        except:
            return None
        return q

    def get_rating(self, qid):
        question = self.get_question(qid)
        question.rating = question.likes.filter(type="+").count()
        question.rating -= question.likes.filter(type="-").count()
        question.save()
        Profile.objects.set_rating(question.author)
        return question.rating


class Question(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return f'({self.id}) {self.author.user.username}: {self.title}'


class TagManager(models.Manager):
    def get_top5(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:5]

    def get_by_question(self, question):
        return self.filter(questions=question)

    def get_by_title(self, current_title):
        return self.filter(title=current_title)[0]


class Tag(models.Model):
    title = models.CharField(max_length=20)

    objects = TagManager()

    def __str__(self):
        return f'({self.id}) {self.title}'


class AnswerManager(models.Manager):
    def get_by_question(self, current_question):
        return self.filter(question=current_question)

    def set_correct(self, answer_id):
        answer = self.get(pk=answer_id)
        answer.is_correct = answer.is_correct ^ True
        answer.save()



class Answer(models.Model):
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', default=0, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'({self.id}) {self.author.user.username} commented question {self.question.title}'


class LikeManager(models.Manager):
    def set_like(self, question_id, user_id, type_of_vote):
        profile = Profile.objects.get_profile_by_user_id(user_id)
        question = Question.objects.get_question(question_id)
        try:
            like = Like.objects.get(from_user=profile, to_question=question)
            if like.type != type_of_vote:
                like.type = type_of_vote
                like.save()
            else:
                like.delete()
            print("like exist")
        except ObjectDoesNotExist:
            print("like doesnt exist")
            like = Like(from_user=profile, to_question=question, type=type_of_vote)
            like.save()
        print(profile)
        return Question.objects.get_rating(question_id)


class Like(models.Model):
    from_user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes')
    to_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')
    type = models.CharField(choices=(("-", "dislike"), ("+", "like"),), null=True)

    objects = LikeManager()

    class Meta:
        unique_together = ('from_user', 'to_question',)

    def __str__(self):
        return f'({self.id}) {self.from_user.user.username} like question {self.to_question.title}'
