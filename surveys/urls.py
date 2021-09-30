from django.urls import path

from surveys.views import SurveyView, SymptomView, SurveyResultView

urlpatterns = [
    path('/survey', SurveyView.as_view()),
    path('/symptom', SymptomView.as_view()),
    path('/result', SurveyResultView.as_view())
]
