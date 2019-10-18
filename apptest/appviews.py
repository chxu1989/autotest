from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import  login_required
from django.contrib import  auth
from apptest.models import Appcasestep,Appcase
from django.contrib.auth import authenticate,login

# Create your views here.

#app用例管理
@login_required
def appcase_manage(request):

	appcase_list=Appcase.objects.all()
	username=request.session.get('user','')
	return render(request,'appcase_manage.html',{'user':username,'appcases':appcase_list})

#app用例步骤管理
@login_required
def appcasestep_manage(request):
	appcasestep_list = Appcasestep.objects.all()
	username = request.session.get( 'user', '' )
	return render( request, 'appcasestep_manage.html', {'user': username, 'appcasesteps': appcasestep_list} )
