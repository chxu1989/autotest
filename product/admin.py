from django.contrib import admin
from product.models import Product
from apitest.models import Apis
from  apptest.models import Appcase
from  webtest.models import Webcase
#import xadmin

# Register your models here.

class ApisAdmin(admin.TabularInline):
	list_display = ['apiname','apiurl','apiparamvalue','apimethod','apiresult','apiresponse','apistatus','create_time',
					'id','product']
	model = Apis
	extra = 1


class AppcaseAdmin(admin.TabularInline):
	list_display = ['appcasename', 'apptestresult','create_time','id','product']
	model = Appcase
	extra = 1


class Webcase_Admin(admin.TabularInline):
	list_display = ['webcasename', 'webtestresult','create_time','id','product']
	model = Webcase
	extra = 1


class ProductAdmin(admin.ModelAdmin):
	list_display = ['productname','productdesc','producter','create_time','id']
	inlines = [ApisAdmin,AppcaseAdmin,Webcase_Admin]

#xadmin.site.unregister(Product)     #把产品模块注册到Django admin 后台并能显示
admin.site.register(Product)     #把产品模块注册到Django admin 后台并能显示