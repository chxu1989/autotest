from django.contrib import admin
from apitest.models import Apistep,Apitest,Apis
#import xadmin
#from xadmin import views

# Register your models here.

 #class GlobalSetting(object):
# 	site_title='自动化测试平台管理后台'
# 	site_footer='Sam'
# 	menu_style = "accordion"
#
# xadmin.site.register(views.CommAdminView, GlobalSetting)


class Apistepadmin(admin.TabularInline):
	list_display=['apiname','apiurl','apiparamvalue','apimethod','apiresult','apiresponse','apistatus',
				  'create_time','id','apitest']
	model = Apistep
	extra = 1

class ApitestAdmin(admin.ModelAdmin):
	list_display = ['apitestname', 'apitester','apitestresult','create_time','id']
	inlines = [Apistepadmin]

#xadmin.site.unregister(Apitest)
admin.site.register(Apitest,ApitestAdmin)


class ApisAdmin(admin.ModelAdmin):
	list_display = ['apiname','apiurl','apiparamvalue','apimethod','apiresult','apiresponse','apistatus','create_time',
					'id','product']


#xadmin.site.unregister(Apis)
admin.site.register(Apis)
