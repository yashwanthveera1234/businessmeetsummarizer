from django.urls import path

from . import views

app_name = "Summarize"

urlpatterns = [
    path('', views.summarizeHomeView, name = 'summarizeHomeView'),
    path('record/', views.recordView, name = 'recordView'),
    path('upload/', views.uploadView, name = 'uploadView'),
    path('details/<int:id>', views.detailsView, name = 'detailsView'),
    path('summarize-text/<int:id>', views.summarizeTextView, name = 'summarizeTextView'),
    path('recognize-text/<int:id>', views.recognizeTextView, name = 'recognizeTextView'),
    path('send-emails/<int:id>', views.sendMailsView, name = 'sendMailsView'),
    path('del/<int:id>' , views.delAudioView, name = 'delAudioView'),
]