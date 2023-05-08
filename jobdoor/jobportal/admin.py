from django.contrib import admin
from .models import User, ApplicantUser, Company, Job, Application, Review, Salary, AddInterview, Keyword, Notification
# Register your models here.


admin.site.register(User)
admin.site.register(ApplicantUser)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Review)
admin.site.register(Salary)
admin.site.register(AddInterview)
admin.site.register(Keyword)
admin.site.register(Notification)
