from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import pytz
from datetime import datetime, timedelta
# Create your models here.




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
    def get_process_percent_value(self):
        return self.perfinished
    

    

    
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    documentarysector = models.ForeignKey(DocumentarySector, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ManyToManyField('Question',blank=True)
    nrepeat = models.IntegerField(default = -1)
    def getnQuestion(self):
        return self.questions.count()
    def __str__(self):
        return f"Kiểm tra: {self.documentarysector.title} | Số câu: {self.questions.count()} | thông tin: {self.description} | số lần thi lại: {'Vô hạn' if self.nrepeat == -1 else str(self.nrepeat)}"


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
    scorerequirement = models.IntegerField(default=0)
    datemodified = models.DateTimeField(blank=True, default=datetime.now)
    def __str__(self):
        
        return f"{self.userdocumentary.user.username} - {self.documentarysector.title}"
    
    def nquiztaken(self):
        return Quiz.objects.filter(userdocumentsection=self).count()
    def update_static(self):
        userquiz = UserQuiz.objects.filter(userdocumentsection=self).first()
        if userquiz:
            questionanswers = QuestionAnswer.objects.filter(userquiz=userquiz)
            self.nquizz = questionanswers.count()
            self.quiz_score = questionanswers.filter(answer__is_correct=True).count()
            self.update_quizzuserdoc_state()
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
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.testdate} | {self.userdocumentsection.userdocumentary.user.username} | {self.quiz.title} | ({self.update_state()}/{self.getnumberquestion()})"

    def update_state(self):
        self.quizscore = QuestionAnswer.objects.filter(userquiz=self).filter(answer__is_correct=1).count()
        return self.quizscore

    def isover(self):
        print((self.testdate+timedelta(minutes=15)).timestamp() , datetime.now().timestamp())
        print(self.testdate,datetime.now())
        print((self.testdate+timedelta(minutes=15)).replace(tzinfo=None) < datetime.now())
        return (self.testdate+timedelta(minutes=15)).replace(tzinfo=None) < datetime.now()

    def getsecondrange(self):
        return (timedelta(minutes=15)-(self.joindate.replace(tzinfo=None) - self.testdate.replace(tzinfo=None))).total_seconds()

    def getnumberquestion(self):
        return self.quiz.questions.count()
    
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
    #get all answers on question index
    def get_answer_on_question_index(self):
        current_question = self.questions.all()[self.questionindex]
        return QuestionAnswer.objects.filter(userquiz=self.userquiz, answer__question=current_question)
    #proccesing submit answer for the question on index
    def submit_question(self, answer):
        current_question = self.q.all()[self.questionindex]
        question_answer = QuestionAnswer.objects.create(userquiz=self.userquiz, answer=answer, question=current_question)

        # Move to the next question
        self.questionindex += 1
        self.save()
        
class tmp_UQ_QuestionUser(models.Model):
    UQ_Question = models.ForeignKey(tmp_UserQuizQuestionAnswer,models.CASCADE)
    question = models.ForeignKey(Question,models.CASCADE)
    answer = models.ForeignKey(Answer,models.CASCADE,null=True)
    questionindex = models.IntegerField(default=-1)
    