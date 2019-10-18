from django.contrib import admin
from bug.models import Bug
#import xadmin

# Register your models here.

class BugAdmin(admin.ModelAdmin):

	list_display = ['bugname ', 'bugdetail ', ' bugstatus', ' buglevel', ' bugcreater', ' bugassign',
	'create_time','id']

#xadmin.site.unregister(Bug)
admin.site.register(Bug)

#xadmin.site.register(Bug)         #在管理后台注册Bug管理模块
