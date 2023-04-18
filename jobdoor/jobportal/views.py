from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_auth.registration.views import RegisterView
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404, CreateAPIView
from .models import ApplicantUser, Company, Job, Application, Review, Salary, AddInterview
from .serializers import ApplicantUserSerializer, UserLoginSerializer, CompanySerializer, CompanyRegistrationSerializer, CompanyUserSerializer, JobSerializer, ApplicationSerializer, ApplicantUserSignupSerializer, CompanyLoginSerializer, ReviewSerializer, CompanyReviewSerializer, SalarySerializer, InterviewSerializer
from rest_framework import generics, status, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationView(RegisterView):
    serializer_class = ApplicantUserSignupSerializer


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user.is_active and user.is_user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'Login Successfully' + ' ' + 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class ApplicantUserList(generics.ListAPIView):
    queryset = User.objects.filter(is_user=True)
    serializer_class = ApplicantUserSerializer
    permission_classes = [IsAuthenticated]


class ApplicantUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ApplicantUserSerializer
    permission_classes = [IsAuthenticated]


class CompanyLoginAPIView(generics.GenericAPIView):
    serializer_class = CompanyLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active and user.is_company:
              login(request, user)
              token, created = Token.objects.get_or_create(user=user)
            return Response({'Login Successfully' + ' ' + 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class CompanySignupView(RegisterView):
    serializer_class = CompanyRegistrationSerializer


class CompanySearchAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company_name', 'location']
    search_fields = ['company_name', 'location']


class CompanyList(generics.ListAPIView):
    serializer_class = CompanyUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.filter(is_company=True)
        return queryset.filter(company__status=True)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_company=True)
    serializer_class = CompanyUserSerializer
    permission_classes = [IsAuthenticated]


class JobList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_company:
            return Job.objects.filter(company=user.company, status=True)
        else:
            raise PermissionDenied(detail='Only company users can see their job list')


@method_decorator(login_required, name='dispatch')
class JobCreation(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the company field to the authenticated user
        serializer.validated_data['company'] = self.request.user.company
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not user.is_company:
            raise PermissionDenied(detail='Only company users can see their applications list')
        company = user.company
        applications = Application.objects.filter(job__company=company)
        if applications.exists():
            return applications
        else:
            raise PermissionDenied(detail='No applications found for this company')


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated and not user.is_company:
            raise PermissionDenied(detail='Only company users can see their applications details')


@method_decorator(login_required, name='dispatch')
class ApplyJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        job_id = kwargs['job_id']
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'The specified job does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        date_today = date.today()
        if job.end_date < date_today:
            return Response({'error': 'The specified job has already closed.'}, status=status.HTTP_400_BAD_REQUEST)
        elif job.start_date > date_today:
            return Response({'error': 'The specified job has not yet opened.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            try:
                application = Application.objects.get(job=job, user=user)
                return Response({'error': 'The user has already applied to this job.'}, status=status.HTTP_400_BAD_REQUEST)
            except Application.DoesNotExist:
                pass

            serializer.save(job=job, user=user, apply_date=date_today, status=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(detail='Only Applicant users can submit reviews.')
        existing_review = Review.objects.filter(company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        return Review.objects.filter(company=company)


class CompanyReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            raise PermissionDenied(detail='Only Company can check reviews.')
        company = self.request.user.company
        return company.reviews.all()


class AddSalaryCreateAPI(generics.CreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(detail='Only Applicant users can submit Salary reviews.')
        existing_review = Salary.objects.filter(company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class SalaryListAPIView(generics.ListAPIView):
    serializer_class = SalarySerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        return Salary.objects.filter(company=company)


class CompanySalaryListAPIView(generics.ListAPIView):
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            raise PermissionDenied(detail='Only Company can check Salary review.')
        company = self.request.user.company
        return company.Salary.all()


class AddInterviewCreateAPI(generics.CreateAPIView):
    queryset = AddInterview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(detail='Only Applicant users can submit Interview reviews.')
        existing_review = AddInterview.objects.filter(company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class InterviewListAPIView(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        return AddInterview.objects.filter(company=company)


class CompanyInterviewListAPIView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            raise PermissionDenied(detail='Only Company can check Interview review.')
        company = self.request.user.company
        interviews = company.Interview.all()
        if not interviews.exists():
            return Response({'detail': 'No interviews available.'}, status=status.HTTP_404_NOT_FOUND)
        return interviews