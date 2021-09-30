from django.urls import path

from surveys.views import SurveyView, SymptomView, SurveyResultView, UserSurveyListView, UserSurveyResultView

urlpatterns = [
    path('/survey', SurveyView.as_view()),
    path('/symptom', SymptomView.as_view()),
    path('/result', SurveyResultView.as_view()),
    path('/resultlist', UserSurveyListView.as_view()),
    path('/user-result', UserSurveyResultView.as_view())
]
