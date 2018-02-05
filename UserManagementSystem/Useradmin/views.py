import os
import json
from django.views import View
from django.shortcuts import render,redirect,HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Useradmin.forms import UserForm,RegisterUserForm,UserinfoForm,GroupForm
from Useradmin import models
from Useradmin.page_config import user_info ,group_info
from Useradmin.utils.con_tool import get_data_list

def init(fuc):
	"""
	判断是否为登录用户。装饰器
	:param fuc:
	:return:
	"""
	def wrapper(request, *args, **kwargs):
		if request.session.get('user_info'):
			ret = fuc(request, *args, **kwargs)
			return ret
		else:
			return redirect('/User/login.html')
	
	return wrapper


def login(request):
	"""
	登录。首先判断用户验证码输入，然后判断用户输入是否符合要求。最后判断密码是否正确。
	:param request:
	:return:
	"""
	ret = {'login_status': False, 'login_error': ''}
	if request.method=="GET":
		obj=UserForm()
		return render(request,'login.html',{'obj': obj, 'check_code': ret})
	else:
		obj=UserForm(request.POST)
		input_code=request.POST.get('code').upper()if(request.POST.get('code')) else None
		session_code=request.session.get('code').upper()
		if input_code==session_code:
			if obj.is_valid():
				session_time=obj.cleaned_data.get('session_time')
				obj.cleaned_data.pop('session_time')
				user_obj=models.UserInfo.objects.filter(**obj.cleaned_data).first()
				if user_obj:
					request.session['user_info'] = {'username': user_obj.user.username, 'nid': user_obj.id}
					request.session.set_expiry(1209600) if session_time else  request.session.set_expiry(0)
					return redirect('/User/usersinfo/')
				else:
					ret['login_error'] = '密码错误'
					return render(request, 'login.html', {'obj': obj, 'check_code': ret})
			else:
				return render(request, 'login.html', {'obj': obj, 'check_code': ret})
		else:
			ret['login_error'] = '验证码错误'
			return render(request, 'login.html', {'obj': obj, 'check_code': ret})
	
def check_code(request):
	"""
	随机生成验证码，验证码图片保存在内存中，然后传到前端，验证码的值保存在session的code里面
	:param request:
	:return:
	"""
	from io import BytesIO
	from utils.random_check_code import rd_check_code
	img, code = rd_check_code(width=150, char_length=5, font_file='static/fonttype/Monaco.ttf')
	stream = BytesIO()
	img.save(stream, 'png')
	request.session['code'] = code
	return HttpResponse(stream.getvalue())


def register(request):
	if request.method == "GET":
		form_list = RegisterUserForm(request)
		return render(request, 'register.html', {'form_list': form_list})
	else:
		form_list = RegisterUserForm(request, request.POST,request.FILES)
		if form_list.is_valid():
			form_list.cleaned_data.pop('code')
			form_list.cleaned_data.pop('password2')
			print(form_list.cleaned_data)
			models.UserInfo.objects.create(**form_list.cleaned_data)
			return redirect('/User/login.html')
		else:
			return render(request, 'register.html', {'form_list': form_list})
	
def avator_input(request):
	"""
	前端上传图片，保存在静态文件夹中
	:param request:
	:return:
	"""
	if request.method == "POST":
		file_obj = request.FILES.get('avator')
		file_path = os.path.join('static', 'imags', 'avator',file_obj.name)
		with open(file_path, 'wb') as f:
			for chunk in file_obj.chunks():
				f.write(chunk)
		return HttpResponse(file_path)
	
def users_infos(request,n):
	"""
	用户详细页
	:param request: 
	:param n: 
	:return: 
	"""
	ret='第{0}编号人'.format(n)
	return render(request,'onlyone.html',{'ret':ret})
def users_info(request):
	"""
	用户列表页
	:param request: 
	:return: 
	"""
	form_list=UserinfoForm()
	return render(request,'usersinfo.html',{'form_list':form_list})

@method_decorator(csrf_exempt,name='dispatch')
class Usersinfo(View):
	"""
	用户列表页，ajax请求
	"""
	def get(self,request):
		server_list=get_data_list(request, models.UserInfo, user_info.table_config)
		ret={
			'server_list':list(server_list),
			'table_config':user_info.table_config,
			'global_dict':{
				'Group_name':list(models.Group.objects.values_list('id','name'))
			},
			'search_config':user_info.search_config
		}
		return  HttpResponse(json.dumps(ret))
	
	def post(self,request):
		form_list = {
			'username':request.POST.get('username'),
		'password':request.POST.get('password'),
		'email':request.POST.get('email'),
		'group':request.POST.get('group'),
		}
		group_dict={}
		group_dict['group']=int(form_list['group'])
		del form_list['group']
		with transaction.atomic():
			num=models.UserInfo.objects.create(**form_list)
			models.User2Group.objects.create(user_id=num.id,group_id=group_dict['group'])
		return HttpResponse('')

	
	def delete(self,request):
		id_list = json.loads(str(request.body, encoding='utf-8'))
		models.UserInfo.objects.filter(id__in=id_list).delete()
		return HttpResponse('')
	
	def put(self,request):
		all_list = json.loads(str(request.body, encoding='utf-8'))
		for row in all_list:
			if row:
				nid = row['nid']
				group_id=row.get('user2group__group_id')
				user_new_id=row.get('id') if row.get('id') else nid
				del row['nid'],row['user2group__group_id']
				with transaction.atomic():
					models.UserInfo.objects.filter(id=nid).update(**row)
					models.User2Group.objects.filter(user_id=nid).update(group_id=group_id,user_id=user_new_id)
		return HttpResponse('')


def groups_infos(request,n):
	"""
	组详细页
	:param request: 
	:param n: 
	:return: 
	"""
	ret='第{0}编号组'.format(n)
	return render(request, 'onlyone.html', {'ret': ret})

def groups_info(request):
	"""
	组列表页
	:param request: 
	:return: 
	"""
	form_list = GroupForm()
	return render(request, 'groupinfo.html', {'form_list': form_list})

@method_decorator(csrf_exempt,name='dispatch')
class Groupinfo(View):
	"""
	组列表页，ajax请求
	"""
	def get(self, request):
		server_list = get_data_list(request, models.Group, group_info.table_config)
		ret = {
			'server_list': list(server_list),
			'table_config': group_info.table_config,
			'global_dict': {
				'Group_name': list(models.Group.objects.values_list('id', 'name'))
			},
			'search_config': group_info.search_config
		}
		return HttpResponse(json.dumps(ret))
	
	def post(self, request):
		form_list = {
			'name': request.POST.get('name'),
		}
		with transaction.atomic():
			models.Group.objects.create(**form_list)
		return HttpResponse('')
	
	def delete(self, request):
		id_list = json.loads(str(request.body, encoding='utf-8'))
		models.Group.objects.filter(id__in=id_list).delete()
		return HttpResponse('')
	
	def put(self, request):
		all_list = json.loads(str(request.body, encoding='utf-8'))
		print(all_list)
		for row in all_list:
			if row:
				nid = row['nid']
				del row['nid']
				with transaction.atomic():
					models.Group.objects.filter(id=nid).update(**row)
					models.User2Group.objects.filter(group_id=nid).update(group_id=row['id'])
		return HttpResponse('')