from django.urls import path

from UserApp import auth_views
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    # Authentication views
    path("", views.index, name="default_view"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("signup/", auth_views.signup_view, name="signup"),
    path("password_reset/", auth_views.password_reset_view, name="password_reset"),
    path("upload_document/", views.upload_document, name="upload_document"),
    path(
        "Course/<int:courseid>/documentaries/<int:sectionid>/",
        views.coursedetail,
        name="coursedetail",
    ),
    path("Course/<int:courseid>/", views.coursedetail, name="coursedetail"),
    path("Course/", views.courses, name="Courses"),
    path(
        "ajax_signincourse/<int:documentaryid>/",
        views.ajax_signincourse,
        name="ajax_signincourse",
    ),
    path(
        "ajax_searchcourse/<int:strSearch>/",
        views.ajax_signincourse,
        name="ajax_searchcourse",
    ),
    path(
        "Course/<int:courseid>/documentaries/<int:sectionid>/Test/<int:testid>/section/<int:userdocumentsectionid>", views.assigningtest, name="assigningtest"
    ),
    path("UserRank/",views.rankview,name= "rankview"),
    path("accounts/password_change/",auth_view.PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change/done/",auth_view.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("accounts/password_reset/",auth_view.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/",auth_view.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("accounts/reset/done/",auth_view.PasswordResetDoneView.as_view(),name='password_reset_complete'),
    path("User/<int:iduser>/",auth_views.userprofile,name="userprofile"),
    #ajax url
    path('ajax_edit_profile/<int:profileid>/', views.ajax_edit_profile, name='ajax_edit_profile'),
    path("Course/documentaries/Test/next/<int:idtmp>/<int:direction>", views.ajax_next_pre_question, name="ajax_next_pre_question"),
    path("Course/documentaries/Test/prev/<int:idtmp>/<int:direction>", views.ajax_next_pre_question, name="ajax_next_pre_question"),
    path("Course/documentaries/Test/<int:idtmp>/questionnavat/<int:questionindex>", views.ajax_question_nav_at_index, name="ajax_question_nav_at_index"),
    path('ajax-answer-pick/<int:idtmpUQ>/<int:idquestion>/<int:answerorder>/', views.ajax_answerpick, name='ajax_answerpick'),
    path("Course/documentaries/Test/<int:idtmp>",views.ajax_is_join_test,name="ajax_is_join_test"),
    path("Course/documentaries/Test/submit/<int:idtmpUQA>",views.finalizetest,name="finalizetest"),
]
