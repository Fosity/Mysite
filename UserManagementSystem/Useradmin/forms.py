from django.forms import Form,fields,widgets
from django.core.exceptions import ValidationError
from Useradmin import models
class UserForm(Form):
	username=fields.CharField(widget=widgets.TextInput(attrs={'class':'form-control','type':'text','placeholder':"姓名"}),
	                          error_messages={
		                          'required':'姓名未填',
		                          'max_length':'名字长度太长',
								  'min_length':'名字长度太短'
	                          }
	                          )
	password=fields.CharField(widget = widgets.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':"密码"}))
	session_time=fields.CharField(
		widget=widgets.CheckboxInput(attrs={'value':'1'}))


class RegisterUserForm(Form):
	username = fields.CharField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "姓名"}),
		error_messages={
			'required': '姓名未填',
			'max_length': '名字长度太长',
			'min_length': '名字长度太短'
		}
		)
	password = fields.CharField(
		widget=widgets.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': "密码"}))
	password2 = fields.CharField(
		widget=widgets.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': "密码"}))
	email = fields.EmailField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "邮箱"}))
	avatar = fields.FileField(widget=widgets.FileInput(attrs={'id': 'imgSelect', 'class': 'f1'}))
	code = fields.CharField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "验证码"})
	)
	
	def __init__(self, request, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.request = request
	
	def clean(self):
		password = self.request.POST.get('password')
		password2 = self.request.POST.get('password2')
		if password == password2:
			return self.cleaned_data
		else:
			self.add_error("password2", ValidationError('密码不一致'))
	
	def clean_code(self):
		input_code = self.cleaned_data['code']
		session_code = self.request.session.get('code')
		if input_code.upper() == session_code.upper():
			return input_code
		raise ValidationError('验证码错误')
	
class UserinfoForm(Form):
	username = fields.CharField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "姓名"}),
		error_messages={
			'required': '姓名未填',
			'max_length': '名字长度太长',
			'min_length': '名字长度太短'
		}
		)
	password = fields.CharField(
		widget=widgets.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': "密码"}))
	email = fields.EmailField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "邮箱"}))
	group=fields.IntegerField(
		widget=widgets.Select(choices=models.Group.objects.values_list('id','name'),attrs={'class': 'form-control'}))
	
class GroupForm(Form):
	name= fields.CharField(
		widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': "名称"}),
		error_messages={
			'required': '名称未填',
			'max_length': '名称长度太长',
			'min_length': '名称长度太短'
		}
		)