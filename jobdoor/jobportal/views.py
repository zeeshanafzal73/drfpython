from allauth.account.views import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_auth.registration.views import RegisterView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.views import APIView
from .models import Company, Job, Application, Review, Salary, AddInterview, Keyword, Notification
from .serializers import ApplicantUserSerializer, UserLoginSerializer, CompanySerializer, CompanyRegistrationSerializer, \
    CompanyUserSerializer, JobSerializer, ApplicationSerializer, ApplicantUserSignupSerializer, CompanyLoginSerializer, \
    ReviewSerializer, SalarySerializer, InterviewSerializer, KeywordSerializer, NotificationSerializer
from rest_framework import generics, status, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta


User = get_user_model()


class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = [TokenAuthentication]

    def get(self, request):
        try:
            if request.user.is_user:
                user_profile = request.user.applicantuser
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'User profile fetched successfully',
                    'data': [{
                        'id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'phone_number': user_profile.phone,
                        'image_url': user_profile.image.url if user_profile.image else None,
                        'gender': user_profile.gender,
                    }]
                }
            elif request.user.is_company:
                user_profile = request.user.company
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'Company profile fetched successfully',
                    'data': [{
                        'id': request.user.id,
                        'username': request.user.username,
                        'email': request.user.email,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'phone_number': user_profile.phone,
                        'logo_url': user_profile.logo.url if user_profile.logo else None,
                        'location': user_profile.location,
                        'company_name': user_profile.company_name,
                    }]
                }
            elif request.user.is_superuser:
                user_profile = request.user
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'Admin profile fetched successfully',
                    'data': [{
                        'email': user_profile.email,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exist',
                'error': str(e)
            }
        return Response(response, status=status_code)


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


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'detail': 'No company found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class AllJobs(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.all()


class JobList(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_company:
            return Job.objects.filter(company=user.company, status=True)
        else:
            raise PermissionDenied(
                detail='Only company users can see their job list')


@method_decorator(login_required, name='dispatch')
class JobCreation(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the company field to the authenticated user
        serializer.validated_data['company'] = self.request.user.company
        serializer.save()

        # Check if there are any matching keywords
        keywords = Keyword.objects.filter(name__icontains=serializer.validated_data['description'])
        if keywords:
            # Get the jobs posted in the last 30 minutes
            time_threshold = datetime.now() - timedelta(minutes=30)
            jobs = Job.objects.filter(creation_date__gte=time_threshold)

            # Find jobs that match the keywords
            matching_jobs = []
            for job in jobs:
                for keyword in keywords:
                    if keyword.name in job.description:
                        matching_jobs.append(job)

            # Send notification to user
            for matching_job in matching_jobs:
                Notification.objects.create(
                    user=self.request.user,
                    job=matching_job,
                    message=f"A new job has been posted matching your keyword: {matching_job.title}"
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobSearchAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'company', 'location']
    search_fields = ['title', 'company', 'location', 'description']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({'detail': 'No jobs found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ApplicationList(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not user.is_company:
            raise PermissionDenied(
                detail='Only company users can see their applications list')
        company = user.company
        applications = Application.objects.filter(job__company=company)
        if applications.exists():
            return applications
        else:
            raise PermissionDenied(
                detail='No applications found for this company')


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated or not user.is_company:
            raise PermissionDenied(detail='Only company users can see their applications details')

        # Get the requested application id from the URL parameter
        application_id = self.kwargs.get('pk')

        # Filter the queryset by the requested application id
        queryset = Application.objects.filter(id=application_id)
        print(queryset)
        return queryset


@method_decorator(login_required, name='dispatch')
# class ApplyJobView(generics.CreateAPIView):
#     serializer_class = ApplicationSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         job_id = kwargs['job_id']
#         print(job_id)
#         try:
#             job = Job.objects.get(id=job_id)
#         except Job.DoesNotExist:
#             return Response({'error': 'The specified job does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#
#         date_today = date.today()
#         if job.end_date < date_today:
#             return Response({'error': 'The specified job has already closed.'}, status=status.HTTP_400_BAD_REQUEST)
#         elif job.start_date > date_today:
#             return Response({'error': 'The specified job has not yet opened.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = ApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             try:
#                 application = Application.objects.get(job=job, user=user)
#                 return Response({'error': 'The user has already applied to this job.'}, status=status.HTTP_400_BAD_REQUEST)
#             except Application.DoesNotExist:
#                 application = None
#
#             serializer.save(job=job, user=user,
#                             apply_date=date_today, status=False)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
                application = None

            serializer.save(job=job, user=user,
                            apply_date=date_today, status=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppliedJobList(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        applications = Application.objects.filter(user=user)
        if applications.exists():
            return applications
        else:
            raise PermissionDenied(
                detail='No applied jobs found for this user')


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(
                detail='Only Applicant users can submit reviews.')
        existing_review = Review.objects.filter(company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
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
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(
                detail='Only Applicant users can submit Salary reviews.')
        existing_review = Salary.objects.filter(company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class SalaryListAPIView(generics.ListAPIView):
    serializer_class = SalarySerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        return Salary.objects.filter(company=company)


class CompanySalaryListAPIView(generics.ListAPIView):
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            raise PermissionDenied(
                detail='Only Company can check Salary review.')
        company = self.request.user.company
        return company.Salary.all()


class AddInterviewCreateAPI(generics.CreateAPIView):
    queryset = AddInterview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        user = self.request.user
        if not user.is_user:
            raise PermissionDenied(
                detail='Only Applicant users can submit Interview reviews.')
        existing_review = AddInterview.objects.filter(
            company=company, user=user)
        if existing_review.exists():
            raise ValidationError('You have already reviewed this company.')
        serializer.save(company=company, user=user)


class InterviewListAPIView(generics.ListAPIView):
    serializer_class = InterviewSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company_user = get_object_or_404(
            User.objects.filter(is_company=True), pk=company_id)
        company = company_user.company
        return AddInterview.objects.filter(company=company)


class CompanyInterviewListAPIView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_company:
            raise PermissionDenied(
                detail='Only Company can check Interview review.')
        company = self.request.user.company
        interviews = company.Interview.all()
        if not interviews.exists():
            return Response({'detail': 'No interviews available.'}, status=status.HTTP_404_NOT_FOUND)
        return interviews


def get_jobs_by_keyword(keyword):
    jobs = Job.objects.filter(title__icontains=keyword)
    job_ids = [job.id for job in jobs]
    print(job_ids)

    return job_ids


class KeywordCreation(generics.CreateAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user to the current authenticated user
        serializer.validated_data['user'] = self.request.user
        serializer.save()

        # Get any matching jobs
        jobs = get_jobs_by_keyword(serializer.validated_data['name'])

        if jobs:
            # Create a notification for the first matching job
            Notification.objects.create(
                user=self.request.user,
                job_id=jobs[0],
                message=f"A new job has been posted matching your keyword: {serializer.validated_data['name']}"
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


