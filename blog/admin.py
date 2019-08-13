from django.contrib import admin

# Register your models here.
from .models import Meeting, UserNorm, PhoneCalls, Activity, ActivityType, Company, MeetingStatus

admin.site.register(Meeting)
admin.site.register(PhoneCalls)
admin.site.register(UserNorm)
admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(Company)
admin.site.register(MeetingStatus)