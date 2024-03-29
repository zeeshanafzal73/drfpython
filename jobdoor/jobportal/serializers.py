from .models import Job, Application, Keyword, Notification
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from .models import ApplicantUser, Company, Review, Salary, AddInterview
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CompanySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ApplicantUserSignupSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    phone = serializers.CharField(required=True)
    # image = serializers.ImageField(required=True)
    gender = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        extra_data = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
            # 'image': self.validated_data.get('image', ''),
            'gender': self.validated_data.get('gender', ''),

        }
        data.update(extra_data)
        return data

    def save(self, request):
        user = super().save(request)
        user.is_user = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        abs_user = ApplicantUser(user=user, phone=self.cleaned_data.get('phone'),
                                 gender=self.cleaned_data.get('gender'), )
        abs_user.save()
        return user


class ApplicantUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='applicantuser.phone')
    gender = serializers.CharField(source='applicantuser.gender')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'phone', 'gender']

    def update(self, instance, validated_data):
        # Update User fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update related ApplicantUser fields if available
        if hasattr(instance, 'applicantuser'):
            applicantuser = instance.applicantuser
            applicantuser.phone = validated_data.get('applicantuser', {}).get('phone', applicantuser.phone)
            applicantuser.gender = validated_data.get('applicantuser', {}).get('gender', applicantuser.gender)
            applicantuser.save()

        # Save User instance with updated fields
        instance.save()

        return instance


class CompanyRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    phone = serializers.CharField(required=True)
    # logo = serializers.ImageField(required=True)
    location = serializers.CharField(required=True)
    company_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        extra_data = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
            # 'logo': self.validated_data.get('logo', ''),
            'location': self.validated_data.get('location', ''),
            'company_name': self.validated_data.get('company_name', ''),


        }
        data.update(extra_data)
        return data

    def save(self, request):
        user = super().save(request)
        user.is_company = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        company = Company(
            company=user,
            phone=self.cleaned_data.get('phone'),
            # logo=self.cleaned_data.get('logo'),
            location=self.cleaned_data.get('location'),
            company_name=self.cleaned_data.get('company_name'),
        )
        company.save()
        return user


class CompanyLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class CompanyUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='company.phone')
    logo = serializers.ImageField(source='company.logo')
    location = serializers.CharField(source='company.location')
    company_name = serializers.CharField(source='company.company_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'phone', 'logo', 'location', 'company_name']

    def update(self, instance, validated_data):
        company_data = validated_data.pop('company', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if company_data is not None:
            company = instance.company
            for attr, value in company_data.items():
                setattr(company, attr, value)
            company.save()
        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    company_id = serializers.CharField(source='company.id')
    company_username = serializers.CharField(source='company.username')

    class Meta:
        model = Company
        fields = ['company_id', 'company_username', 'company_name', 'logo']


class JobSerializer(serializers.ModelSerializer):
    # company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    company_name = serializers.CharField(
        source='company.company_name', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'company_name', 'start_date', 'end_date', 'title', 'salary',
                  'image', 'description', 'experience', 'location', 'skills', 'creation_date']


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title')
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = Application
        fields = ['id', 'job_title', 'user_name', 'apply_date', 'resume']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'rating',  'job_type', 'Employment_Date', 'job_title', 'user',
                  'comments', 'pros', 'cons', 'Advice_to_management', 'date_created')
        read_only_fields = ('user', 'date_created')


class CompanyRevDet(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comments', 'date_created']


class CompanyReviewSerializer(serializers.ModelSerializer):
    company_username = serializers.CharField(source='company.username')

    class Meta:
        model = Company
        fields = ['id', 'company_username', 'company_name', 'logo']


class SalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ['total_salary']


class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddInterview
        fields = ['id', 'Rate', 'job_title', 'process',
                  'questions', 'answers', 'outcome_offer', 'user']


class KeywordSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Keyword
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    job_id = serializers.CharField(source='job.id')
    created_start = serializers.CharField(source='job.start_date')
    created_end = serializers.CharField(source='job.end_date')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'job_id', 'message', 'created_start', 'created_end']