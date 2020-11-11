from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('acrp/index', views.index, name='index'),
    path('acrp/evaluator/search', views.search, name='search'),
    path('acrp/evaluator/saved_application/<int:Applicant_id>/', views.saved_application, name='saved_application'),
    path('acrp/evaluator/submit', views.submit, name='submit'),
    path('acrp/evaluator/submit_application/<int:Applicant_id>/', views.submit_application, name='submit_application'),
    path('acrp/advisor/<str:cheque_no>/<int:ref_num>', views.advisor, name='advisor'),
    path('acrp/', TemplateView.as_view(template_name='polls/urls.html')),
    path('acrp/elog/',views.user,name='user'),
    # path('', TemplateView.as_view(template_name='polls/mainpage.html')),
    path('acrp/support/process', views.process, name='process'),
    path('acrp/support/process_detail/<int:Applicant_id>/', views.process_detail, name='process_detail'),
    path('acrp/support/processed', views.processed, name='processed'),
    path('acrp/support/processed_detail/<int:Applicant_id>/', views.processed_detail, name='processed_detail'),
    path('acrp/recom/<str:cheque_no>/<int:ref_num>', views.getrecommendations, name='getrecommendations'),
    path('acrp/support/', views.support,name='support'),
    path('acrp/openview', views.RecommendationsAllInternal, name=' RecommendationsAllInternal'),
    path('acrp/evaluators', views.evaluators,name='evaluators'),
    path('acrp/EvaluateSubmissions', views.EvaluateSubmissions, name='EvaluateSubmissions'),
    path('acrp/EvaluateSubmissions_detail/<int:Applicant_id>/', views.EvaluateSubmissions_detail, name='EvaluateSubmissions_detail'),
    path('acrp/EvaluateSubmissionsSaved_detail/<int:Applicant_id>/', views.EvaluateSubmissionsSaved_detail, name='EvaluateSubmissionsSaved_detail'),
    path('acrp/CompletedSubmissions', views.CompletedSubmissions, name='CompletedSubmissions'),
    path('acrp/compute_average_detail/<int:a_id>/', views.compute_average_detail, name='compute_average_detail'),
    path('acrp/log/',views.user_prof,name='user_prof'),
    path('acrp/support/compute_average', views.compute_average, name='compute_average'),
    path('acrp/support/compute_average_detail/<int:a_id>/', views.compute_average_detail, name='compute_average_detail'),
    path('acrp/support/enable',views.enableCompleteSubmissions,name='enableCompleteSubmissions')
    # path('acrp/login/', views.login, name ='login'), 



]