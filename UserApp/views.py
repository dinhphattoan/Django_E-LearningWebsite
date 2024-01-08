from datetime import datetime
import json
from django.core.serializers import serialize
from bs4 import BeautifulSoup, Comment
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import pypandoc
from . import models
import mammoth
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    recent_userdocumentary = recent_quizz = None
    if request.user.is_authenticated:
        try:
            recent_userdocumentary = models.UserDocumentary.objects.latest(
                "datemodified"
            )
        except models.UserDocumentary.DoesNotExist:
            recent_userdocumentary = None
        recent_quizz = models.UserDocumentSection.objects.filter(
            userdocumentary__user=request.user
        ).order_by("-datemodified")[:5]
    return render(
        request,
        "index.html",
        {"userdocumentary": recent_userdocumentary, "5quizz:": recent_quizz},
    )


from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import DocumentForm, DocumentaryForm  # Replace with your forms
from .models import Documentary  # Replace with your models

# Create your views here.


def documentary_list(request):
    documentaries = Documentary.objects.all()
    context = {
        "documentaries": documentaries,
    }
    return render(request, "adminapp/index.html", context)


def documentary_detail(request, pk):
    documentary = Documentary.objects.get(pk=pk)
    context = {
        "documentary": documentary,
    }
    return render(request, "adminapp/detail.html", context)


def documentary_create(request):
    if request.method == "POST":
        form = DocumentaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("documentary_list")
    else:
        form = DocumentaryForm()
    context = {
        "form": form,
    }
    return render(request, "adminapp/create.html", context)


# Similar views for other model creation and update with appropriate forms
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            # Convert Word to HTML using pypandoc
            html = pypandoc.convert_file(file, "html", format="docx")

            # Store the HTML content (or do something else with it)
            # ...

            return redirect("success_page")  # Redirect to a success page
    else:
        form = DocumentForm()
    return render(request, "upload_document.html", {"form": form})


def courses(request):
    courses = list(models.Documentary.objects.all())
    listassignedcourse = None
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Access the logged-in user
        logged_in_user = request.user
        listassignedcourse = list(
            models.UserDocumentary.objects.filter(user=logged_in_user)
        )
        for assigned in listassignedcourse:
            courses.remove(assigned.documentary)
    return render(
        request,
        "course.html",
        {"Courses": courses, "AssignedCourses": listassignedcourse},
    )


def ajax_searchcourse(request, strSearch):
    documentaries = Documentary.objects.filter(title__icontains=strSearch.lower())

    # Serialize the QuerySet to JSON
    serialized_data = serialize("json", documentaries)

    # Convert the serialized data to a Python list
    json_data = serialized_data.decode("utf-8")
    result_list = [item["fields"] for item in json.loads(json_data)]

    data = {"models": result_list}

    return JsonResponse(data)


def ajax_signincourse(request, documentaryid):
    documentary = get_object_or_404(Documentary, id=documentaryid)
    data = ""

    if documentary and request.user.is_authenticated:
        if not models.UserDocumentary.objects.filter(
            user=request.user, documentary=documentary
        ).exists():
            userdocumentary = models.UserDocumentary(
                user=request.user,
                documentary=documentary,
                isfinished=False,
                perfinished=0,
            )
            userdocumentary.save()
            data = "Đăng ký khóa học thành công, tải lại trang..."

    return HttpResponse(data)


def coursedetail(request, courseid, sectionid=None):
    documentary = get_object_or_404(models.Documentary, pk=courseid)
    sections = models.DocumentarySector.objects.filter(documentary=documentary)
    userdocumentary = None
    userquizzesa = runningquizz = None
    sectionquizz = UserDocumentSection = userquizzes = nquestions = None

    if request.user.is_authenticated:
        userdocumentary = models.UserDocumentary.objects.filter(
            user=request.user, documentary=documentary
        ).first()

    if sectionid:
        firstsection = sections.filter(id=sectionid).first()

        if firstsection:
            content_path = os.path.join(
                settings.MEDIA_ROOT, firstsection.contentfile.path
            )

            with open(content_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file).value
                soup = BeautifulSoup(result, "html.parser")

    else:
        firstsection = None
        metadata = None
        result = None

    if firstsection:
        sectionquizz = models.Quiz.objects.filter(
            documentarysector=firstsection
        ).first()
        if request.user.is_authenticated:
            if (
                userdocumentary
                and not models.UserDocumentSection.objects.filter(
                    documentarysector=firstsection, userdocumentary=userdocumentary
                ).first()
            ):
                tmpUserDocumentSection = models.UserDocumentSection(
                    documentarysector=firstsection,
                    userdocumentary=userdocumentary,
                    completed=False,
                )
                tmpUserDocumentSection.save()

        if sectionquizz:
            nquestions = sectionquizz.getnQuestion()

        UserDocumentSection = models.UserDocumentSection.objects.filter(
            documentarysector=firstsection, userdocumentary=userdocumentary
        ).first()

        if UserDocumentSection:
            userquizzes = models.UserQuiz.objects.filter(
                userdocumentsection=UserDocumentSection
            ).order_by("testdate")
            if userquizzes:
                runningquizz = (
                    None if userquizzes.last().isover() else userquizzes.last()
                )
            userquizzesa = None
            userquizzesa = [quiz for quiz in userquizzes if quiz.isover()]
    return render(
        request,
        "coursedetail.html",
        {
            "documentary": documentary,
            "sections": sections,
            "cursection": firstsection,
            "sectorcontent": result,
            "userdocumentary": userdocumentary,
            "sectionquizz": sectionquizz,
            "nquestions": nquestions,
            "userDocumentsection": UserDocumentSection,
            "userquizz": userquizzesa,
            "runningquizz": runningquizz,
        },
    )


@login_required
def assigningtest(request, courseid, sectionid, testid, userdocumentsectionid):
    userdocumentsection = models.UserDocumentSection.objects.filter(
        pk=userdocumentsectionid
    ).first()
    quiz = models.Quiz.objects.get(pk=testid)
    userquiz = None
    tmp = None
    listuserquiz = models.UserQuiz.objects.filter(
        userdocumentsection=userdocumentsection
    ).order_by("testdate")
    runninguserquiz = listuserquiz.last()
    if runninguserquiz:
        runninguserquiz.save()
        runninguserquiz = None if runninguserquiz.isover() else runninguserquiz

    # check if user quiz is exist
    if runninguserquiz:
        # if do check the latest user quiz running is over.
        # get the latest user quiz when it's still running
        runninguserquiz.joindate = datetime.now()
        runninguserquiz.save(force_update=True)
    # all conditions if user quiz is not exist or any that require to create new record.
    # new test taking, or first time taking.
    else:
        if listuserquiz.count() < (quiz.nrepeat + 1):
            userquiz = models.UserQuiz(
                userdocumentsection=userdocumentsection, quiz=quiz
            )
            userquiz.joindate = datetime.now()
            userquiz.testdate=datetime.now()
            userquiz.save(force_insert=True)
            runninguserquiz = userquiz
        else:
            return HttpResponse("Vượt quá số lần thi")
    tmp = models.tmp_UserQuizQuestionAnswer.objects.filter(userquiz=runninguserquiz).last()

    # initialize new tmp quiz
    if not tmp:
        # Assuming you have a valid UserQuiz instance named userquiz
        tmp = models.tmp_UserQuizQuestionAnswer.objects.create(userquiz=runninguserquiz)
        tmp.save()
        filtered_question = models.Question.objects.filter(quizz=tmp.userquiz.quiz)
        index = 0
        for ques in filtered_question:
            tmp_ques = models.tmp_UQ_QuestionUser(
                UQ_Question=tmp, question=ques, questionindex=index
            )
            index += 1
            tmp_ques.save()
        tmp = models.tmp_UserQuizQuestionAnswer.objects.filter(userquiz=runninguserquiz).last()

    tmp_QU = models.tmp_UQ_QuestionUser.objects.filter(UQ_Question=tmp)
    tmp.related_questions.set(models.tmp_UQ_QuestionUser.objects.filter(UQ_Question=tmp))
    return render(
        request,
        "test.html",
        {
            "userquiz": runninguserquiz,
            "courseid": courseid,
            "sectionid": sectionid,
            "quiztmp": {
                "tmp": tmp,
                "tmp_QU": tmp_QU,
                "timequiz": runninguserquiz.getsecondrange(),
            },
        },
    )

@login_required
def ajax_next_pre_question(request, idtmp, flag=True):
    tmpUQQA = get_object_or_404(models.tmp_UserQuizQuestionAnswer, pk=idtmp)
    
    if flag:
        tmpUQQA.questionindex += 1
    else:
        tmpUQQA.questionindex = max(0, tmpUQQA.questionindex - 1)
    
    tmpUQQA.save(force_update=True)
    
    # Fetch a single instance of tmp_UQ_QuestionUser using get_object_or_404
    tmp = get_object_or_404(models.tmp_UQ_QuestionUser, UQ_Question=tmpUQQA, questionindex=tmpUQQA.questionindex)
    
    answers = models.Answer.objects.filter(question=tmp.question)
    
    # Serialize tmp and answers to JSON
    tmp_json = serialize('json', [tmp])
    answers_json = serialize('json', answers)

    data = {"tmp": tmp_json, "answeroptions": answers_json}
    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def ajax_submittest(request, courseid, userquizid):
    userquiz = get_object_or_404(models.UserQuiz, pk=userquizid)
    userquiz.update_state()
    userquiz.save(force_update=True)
    return redirect(coursedetail, courseid, userquizid)

@login_required
def ajax_answerpick(request, idtmp, answerorder):
    pass