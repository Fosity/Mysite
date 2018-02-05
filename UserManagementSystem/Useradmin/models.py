from django.db import models
class UserInfo(models.Model):
	username=models.CharField('用户名',max_length=32)
	password=models.CharField('密码',max_length=64)
	email=models.EmailField('邮箱')
	avatar = models.ImageField(verbose_name='头像',default=None)
	def __str__(self):
		return self.username
	
class Group(models.Model):
	name=models.CharField('用户组名',max_length=32)
	def __str__(self):
		return self.name
	
class User2Group(models.Model):
	user=models.ForeignKey(UserInfo,verbose_name='用户')
	group=models.ForeignKey(Group,verbose_name='用户组')
	
	def __str__(self):
		return "{0}-{1}".format(self.user.username,self.group.name)
	
