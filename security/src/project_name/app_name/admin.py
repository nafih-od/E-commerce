from django.contrib import admin

from app_name.models import PrintClass, PingsLog,SslLog,HttpLog,SsllabsLog,CmsLog,NsLog,DtLog,CvLog


class PrintAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(PrintClass, PrintAdmin)


class PingsLogAdmin(admin.ModelAdmin):
    list_display = ['host']

admin.site.register(PingsLog, PingsLogAdmin)


class SslLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(SslLog, SslLogAdmin)

class HttplLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(HttpLog, HttplLogAdmin)


class SsllabsLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(SsllabsLog, SsllabsLogAdmin)


class CmsLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(CmsLog, CmsLogAdmin)


class NsLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(NsLog, NsLogAdmin)


class DtLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(DtLog, DtLogAdmin)


class CvLogAdmin(admin.ModelAdmin):
    list_display = ['domain']

admin.site.register(CvLog, CvLogAdmin)






