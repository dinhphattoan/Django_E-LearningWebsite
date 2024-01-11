import math
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save,post_delete
from django.dispatch import receiver
import pytz
from datetime import datetime, timedelta
# Create your models here.


class UserInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(blank = True)
    phone = models.TextField(blank=True)
    portrait = models.FileField(null=True,upload_to="User/")
    bio = models.TextField(blank = True)
    href_facebook = models.TextField(blank = True)
    href_twitter = models.TextField(blank = True)
    href_blog = models.TextField(blank = True)
    href_github = models.TextField(blank = True)
    def __str__(self):
       return f"{self.user.pk} User: {self.user.username}| {self.user.first_name} {self.user.last_name}" 
    

class Documentary(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=255)
    videointro = models.FileField(blank=True)
    thumbnail = models.ImageField(null=True,upload_to="Course/")
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    summary = models.TextField(null=True)
    def __str__(self):
        return self.title
    
class DocumentarySector(models.Model):
    documentary = models.ForeignKey(Documentary, on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    contentfile = models.FileField(blank=True)
    videolecture = models.FileField(blank=True)
    def __str__(self):
        return self.title

    
class UserDocumentary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    documentary = models.ForeignKey(Documentary,on_delete=models.CASCADE)
    isfinished = models.BooleanField(default=False)
    perfinished = models.IntegerField(default=0)
    datemodified = models.DateTimeField(default = datetime.now, blank=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self):
        return self.user.username + " - " + self.documentary.title + " | process: " + str(self.perfinished)
    def update_per_state(self):
        list_sections = DocumentarySector.objects.filter(documentary = self.documentary).all()
        list_sectionquizes =list(list_sections)
        list_userds = list()
        for section in list_sectionquizes:
            if Quiz.objects.filter(documentarysector__pk = section.pk).first():
                list_userds.append(UserDocumentSection.objects.get(documentarysector=section,userdocumentary = self))
        list_finishedsection = [x for x in list_userds if x.completed]
        list_unfinishedsection = [x for x in list_userds if not x.completed]
        # Avoid division by zero by checking if total_sections_count is not zero
        if len(list_unfinishedsection) != 0:
            self.perfinished = (len(list_finishedsection) / (len(list_unfinishedsection)+len(list_finishedsection))) * 100
        else:
            # Handle the case where list_unfinishedsection is empty to avoid division by zero
            self.perfinished = 0

        self.save(force_update=True)

    def get_process_percent_value(self):
        return self.perfinished
    

    

    
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    documentarysector = models.ForeignKey(DocumentarySector, on_delete=models.CASCADE, null=True, blank=True)
    nrepeat = models.IntegerField(default = -1)
    scorerequirement = models.IntegerField(default=0)
    def __str__(self):
        return f"Kiểm tra: {self.documentarysector.title}| thông tin: {self.description} | số lần thi lại: {'Vô hạn' if self.nrepeat == -1 else str(self.nrepeat)}"
    def getnQuestion(self):
        return Question.objects.filter(quizz = self).count()

class Question(models.Model):
    QUESTION_TYPE = [
        ('multiple choice', 'Multiple Choice'),
        ('trueorfalse', 'True, False'),
        ('fillintheblank', 'Fill in the blank'),
        ('onechoice', "One choice answer")
    ]
    quizz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20,choices=QUESTION_TYPE)  # e.g., multiple_choice, true_false, fill_in_the_blank
    def __str__(self):
        return self.text
    
class Answer(models.Model):
    ANSWER_ORDER = [
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, "D")
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    answerorder = models.IntegerField(default=-1,choices =ANSWER_ORDER)
    is_correct = models.BooleanField()
    def __str__(self):
        return f"{self.answerorder}. {self.question.text} | {self.text} | {'Đúng' if self.is_correct else 'Sai'}"


class UserDocumentSection(models.Model):
    documentarysector = models.ForeignKey(DocumentarySector, on_delete=models.CASCADE, null=False)
    userdocumentary = models.ForeignKey(UserDocumentary, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quiz_score = models.IntegerField(null=True, blank=True, default=-1)
    #By default the score is 70% of total for requirement
    scorerequirement = models.IntegerField(default=0)
    datemodified = models.DateTimeField(blank=True, default=datetime.now)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return f"{self.userdocumentary.user.username} - {self.documentarysector.title}"
    def nquiztaken(self):
        return Quiz.objects.filter(userdocumentsection=self).count()
    def update_score_requirement(self):
        nqestion =Question.objects.filter(quizz = Quiz.objects.get(documentarysector =self.documentarysector)).all().count()
        self.scorerequirement = math.floor((nqestion/100)*70)
        self.save(force_update=True)
    def update_quizzuserdoc_state(self):
        self.quiz_score= UserQuiz.objects.filter(userdocumentsection = self).order_by('quizscore').first().quizscore
        self.completed = self.quiz_score >= self.scorerequirement

class UserQuiz(models.Model):
    userdocumentsection = models.ForeignKey(UserDocumentSection, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    joindate = models.DateTimeField(default=timezone.now) 
    testdate = models.DateTimeField(default=timezone.now)
    testminiutes = models.IntegerField(default=15)
    quizscore = models.IntegerField(default=0)
    quizisover = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.testdate} | {self.userdocumentsection.userdocumentary.user.username} | {self.quiz.title} | ({self.update_state()})"

    def update_state(self):
        self.quizscore = QuestionAnswer.objects.filter(userquiz=self).filter(answer__is_correct=1).count()
        self.quizisover=True
        return self.quizscore

    def isover(self):
        if not self.quizisover:
            print((self.testdate+timedelta(minutes=15)).timestamp() , datetime.now().timestamp())
            print(self.testdate,datetime.now())
            print((self.testdate+timedelta(minutes=15)).replace(tzinfo=None) < datetime.now())
            return (self.testdate+timedelta(minutes=15)).replace(tzinfo=None) < datetime.now()
        return True
    def getsecondrange(self):
        return (timedelta(minutes=15)-(self.joindate.replace(tzinfo=None) - self.testdate.replace(tzinfo=None))).total_seconds()
    
class QuestionAnswer(models.Model):
    userquiz = models.ForeignKey(UserQuiz,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete= models.CASCADE)
    question = models.ForeignKey(Question,on_delete= models.CASCADE)

#storing temporary data for user taking the test
class tmp_UserQuizQuestionAnswer(models.Model):
    #user taken with quiz
    userquiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE)
    #question index current working on
    questionindex = models.IntegerField(default=0)  # Start with 0 as the first question index
    related_questions = models.ManyToManyField('tmp_UQ_QuestionUser', related_name='related_answers', blank=True)
class tmp_UQ_QuestionUser(models.Model):
    UQ_Question = models.ForeignKey(tmp_UserQuizQuestionAnswer,models.CASCADE)
    question = models.ForeignKey(Question,models.CASCADE)
    answer = models.ForeignKey(Answer,models.CASCADE,null=True)
    questionindex = models.IntegerField(default=-1)

@receiver(post_save, sender=Question)
def question_post_save(sender, instance, created, **kwargs):
    """
    This function will be called after an instance of Question is saved.
    'created' argument indicates whether the instance was created or updated.
    """
    if created:
        # Assuming you have a ForeignKey from Question to Quizz and Quizz to DocumentarySector
        documentary_sector = instance.quizz.documentarysector
        listuserdocumentationsection =  UserDocumentSection.objects.filter(documentarysector=documentary_sector).all()
        for userdocumentationsection in listuserdocumentationsection:
            userdocumentationsection.update_score_requirement()
            
@receiver(post_delete, sender=Question)
def question_post_save(sender, instance, **kwargs):
    """
    This function will be called after an instance of Question is saved.
    'created' argument indicates whether the instance was created or updated.
    """
    documentary_sector = instance.quizz.documentarysector
    listuserdocumentationsection =  UserDocumentSection.objects.filter(documentarysector=documentary_sector).all()
    for userdocumentationsection in listuserdocumentationsection:
        userdocumentationsection.update_score_requirement()
@receiver(post_save,sender=Quiz)
def quiz_post_save(sender, instance, created, **kwargs):
    """
    This function will be called after an new instance of Quiz is saved.
    All the user process with document will be update with including unfinished quiz
    """
    if created:
        documentarysector = instance.documentarysector
        documentary = documentarysector.documentary
        list_userdocument = UserDocumentary.objects.filter(documentary= documentary).all()
        for ud in list_userdocument:
            ud.update_per_state()
@receiver(post_delete,sender=Quiz)
def quiz_post_save(sender, instance, **kwargs):
    """
    This function will be called after an new instance of Quiz is saved.
    All the user process with document will be update with including unfinished quiz
    """
    documentarysector = instance.documentarysector
    documentary = documentarysector.documentary
    list_userdocument = UserDocumentary.objects.filter(documentary= documentary).all()
    for ud in list_userdocument:
        ud.update_per_state()