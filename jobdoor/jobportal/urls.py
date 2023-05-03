from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserLoginAPIView, UserRegistrationView, ApplicantUserList, ApplicantUserDetail, JobList, JobDetail, JobSearchAPIView, ApplyJobView, AppliedJobList, CompanySignupView, CompanyLoginAPIView, CompanyList, CompanySearchAPIView, CompanyDetail, JobCreation, ApplicationList, ApplicationDetail, ReviewCreateAPIView, ReviewListAPIView, CompanyReviewListAPIView, AddSalaryCreateAPI, SalaryListAPIView, CompanySalaryListAPIView, AddInterviewCreateAPI, InterviewListAPIView, CompanyInterviewListAPIView


urlpatterns = [

    #User
    path('accounts/login/', UserLoginAPIView.as_view(), name='applicant_user_login'),
    path('Applicant/signup/', UserRegistrationView.as_view(), name='signup'),
    path('applicants/', ApplicantUserList.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantUserDetail.as_view(), name='applicant-detail'),
    path('jobs/', JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/apply/', ApplyJobView.as_view(), name='apply_job'),
    path('search/jobs/', JobSearchAPIView.as_view(), name='search-jobs'),
    path('applied-jobs/', AppliedJobList.as_view(), name='applied_job_list'),


    #Company
    path('company/signup/', CompanySignupView.as_view(),name='signup'),
    path('company/login/', CompanyLoginAPIView.as_view(),name='login'),
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('companies/search/', CompanySearchAPIView.as_view(), name='company-search-filter'),
    path('companies/<int:pk>/', CompanyDetail.as_view(), name='company-detail'),
    path('add_jobs/', JobCreation.as_view(), name='job_creation'),

    #Application
    path('applications/', ApplicationList.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetail.as_view(), name='application-detail'),

    #Review
    path('reviews/create/<int:company_id>/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('reviews/<int:company_id>/', ReviewListAPIView.as_view(), name='review_list_company'),
    path('reviews/company/', CompanyReviewListAPIView.as_view(), name='company_review_list'),

    #Add Salary

    path('Salary/create/<int:company_id>/', AddSalaryCreateAPI.as_view(), name='Add-salary-info'),
    path('Salary/<int:company_id>/', SalaryListAPIView.as_view(), name='salary-info'),
    path('Salary/', CompanySalaryListAPIView.as_view(), name='View-salary-info'),

    #Add Interview

    path('Interview/create/<int:company_id>/', AddInterviewCreateAPI.as_view(), name='Add-interview-info'),
    path('Interview/<int:company_id>/', InterviewListAPIView.as_view(), name='interview-info'),
    path('Interview/', CompanyInterviewListAPIView.as_view(), name='View-interview-info'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
