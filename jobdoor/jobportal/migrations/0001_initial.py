# Generated by Django 3.1.2 on 2023-04-15 09:25

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_user', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('logo', models.ImageField(upload_to='jobportal/static/company_img')),
                ('location', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('type', models.CharField(default='company', max_length=15)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jobportal.user')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('current_or_former_job', models.CharField(choices=[(1, '1 Current_employee'), (2, '2 Job_ending_year_2023'), (3, '3 Job_ending_year_2022'), (4, '4 Job_ending_year_2021'), (5, '5 Job_ending_year_2020'), (6, '6 Job_ending_year_2019')], max_length=255)),
                ('employee_status', models.CharField(choices=[(1, '1 Full_time'), (2, '2 Part_time'), (3, '3 Contract'), (4, '4 Internship')], max_length=255)),
                ('salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('bonus', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('total_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('experience', models.CharField(choices=[(1, '1 year'), (2, '2 year'), (3, '3 year'), (4, '4 year'), (5, '5 year'), (6, '6 year'), (7, '7 year'), (8, '8 year'), (9, '9 year'), (10, '10 year'), (11, '11 year'), (12, '12 year')], max_length=255)),
                ('gender', models.CharField(choices=[(1, 'Male'), (2, 'Female')], max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Salary', to='jobportal.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(choices=[(1, '1 Full_time'), (2, '2 Part_time'), (3, '3 Contract'), (4, '4 Internship')], max_length=255)),
                ('Employment_Date', models.CharField(choices=[(1, '1 Current_employee'), (2, '2 Last_year_with_Company_2023'), (3, '3 Last_year_with_Company_2022'), (4, '4 Last_year_with_Company_2021'), (5, '5 Last_year_with_Company_2020'), (6, '6 Last_year_with_Company_2019')], max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('comments', models.TextField()),
                ('pros', models.TextField()),
                ('cons', models.TextField()),
                ('Advice_to_management', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='jobportal.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='jobportal.user')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('salary', models.FloatField()),
                ('image', models.ImageField(upload_to='jobportal/static/job_img')),
                ('description', models.TextField(max_length=400)),
                ('experience', models.CharField(choices=[(1, '1 year'), (2, '2 year'), (3, '3 year'), (4, '4 year'), (5, '5 year'), (6, '6 year'), (7, '7 year'), (8, '8 year'), (9, '9 year'), (10, '10 year'), (11, '11 year'), (12, '12 year')], max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=200)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.company')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='jobportal/static/resume')),
                ('apply_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.user')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='jobportal/static/applicant_img')),
                ('gender', models.CharField(choices=[(1, 'Male'), (2, 'Female')], max_length=255)),
                ('type', models.CharField(default='applicant', max_length=255)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobportal.user')),
            ],
        ),
        migrations.CreateModel(
            name='AddInterview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rate', models.CharField(choices=[(1, '1 Positive'), (2, '2 Negative'), (3, '3 Natural')], max_length=20)),
                ('job_title', models.CharField(max_length=255)),
                ('process', models.CharField(max_length=255)),
                ('questions', models.CharField(max_length=255)),
                ('answers', models.CharField(max_length=255)),
                ('outcome_offer', models.CharField(choices=[(1, '1 Yes, and I accepted'), (2, '2 Yes, but I declined'), (3, '3 No, offer')], max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Interview', to='jobportal.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportal.user')),
            ],
        ),
    ]
