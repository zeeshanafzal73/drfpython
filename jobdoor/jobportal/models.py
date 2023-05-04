from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    #Boolean fields to select the type of account.
  is_user = models.BooleanField(default=False)
  is_company = models.BooleanField(default=False)


class ApplicantUser(models.Model):
    gen_Types = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to="jobportal/static/applicant_img")
    gender = models.CharField(max_length=255, choices=gen_Types)
    type = models.CharField(max_length=255, default='applicant')

    def __str__(self):
        return self.user.username


class Company(models.Model):
    company = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to="jobportal/static/company_img", blank=True)
    location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=100)
    # status = models.CharField(max_length=20, default='pending')
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=15, default='company')

    def __str__(self):
        return self.company.username


class Job(models.Model):

    ex_Types = (
        (1, '1 year'),
        (2, '2 year'),
        (3, '3 year'),
        (4, '4 year'),
        (5, '5 year'),
        (6, '6 year'),
        (7, '7 year'),
        (8, '8 year'),
        (9, '9 year'),
        (10, '10 year'),
        (11, '11 year'),
        (12, '12 year'),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    image = models.ImageField(upload_to="jobportal/static/job_img")
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100, choices=ex_Types)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)
    # status = models.CharField(max_length=20, default='pending')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="jobportal/static/resume")
    apply_date = models.DateField(default=now)
    # status = models.CharField(max_length=20, default='pending')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    Job_Types = (
        (1, '1 Full_time'),
        (2, '2 Part_time'),
        (3, '3 Contract'),
        (4, '4 Internship'),
        )
    Dates = (
        (1, '1 Current_employee'),
        (2, '2 Last_year_with_Company_2023'),
        (3, '3 Last_year_with_Company_2022'),
        (4, '4 Last_year_with_Company_2021'),
        (5, '5 Last_year_with_Company_2020'),
        (6, '6 Last_year_with_Company_2019'),
    )

    job_type = models.CharField(max_length=255, choices=Job_Types)
    Employment_Date = models.CharField(max_length=255, choices=Dates)
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    Advice_to_management = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}'s review for {self.company.company_name}"


class Salary(models.Model):
    Job_Types = (
        (1, '1 Current_employee'),
        (2, '2 Job_ending_year_2023'),
        (3, '3 Job_ending_year_2022'),
        (4, '4 Job_ending_year_2021'),
        (5, '5 Job_ending_year_2020'),
        (6, '6 Job_ending_year_2019'),
    )
    status_Types = (
        (1, '1 Full_time'),
        (2, '2 Part_time'),
        (3, '3 Contract'),
        (4, '4 Internship'),
    )
    ex_Types = (
        (1,  '1 year'),
        (2,  '2 year'),
        (3,  '3 year'),
        (4,  '4 year'),
        (5,  '5 year'),
        (6,  '6 year'),
        (7,  '7 year'),
        (8,  '8 year'),
        (9,  '9 year'),
        (10, '10 year'),
        (11, '11 year'),
        (12, '12 year'),
    )
    gen_Types = (
        (1, 'Male'),
        (2, 'Female'),
    )

    company = models.ForeignKey(Company, related_name='Salary',  on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    current_or_former_job = models.CharField(max_length=255, choices=Job_Types)
    employee_status = models.CharField(max_length=255, choices=status_Types)
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    experience = models.CharField(max_length=255, choices=ex_Types)
    gender = models.CharField(max_length=255, choices=gen_Types)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_salary = self.salary + self.bonus
        super(Salary, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}\'s salary'


class AddInterview(models.Model):
    Rate_Types = (
        (1, '1 Positive'),
        (2, '2 Negative'),
        (3, '3 Natural'),
    )
    outcome_Types = (
        (1, '1 Yes, and I accepted'),
        (2, '2 Yes, but I declined'),
        (3, '3 No, offer'),
    )

    company = models.ForeignKey(Company, related_name='Interview', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Interview', on_delete=models.CASCADE)
    Rate = models.CharField(max_length=20, choices=Rate_Types)
    job_title = models.CharField(max_length=255)
    process = models.CharField(max_length=255)
    questions = models.CharField(max_length=255)
    answers = models.CharField(max_length=255)
    outcome_offer = models.CharField(max_length=255, choices=outcome_Types)

    def __str__(self):

        return f"{self.user.username}'s interview for {self.company.company_name}"
