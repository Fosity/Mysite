# _*_coding:utf-8_*_
# Author:xupan
import json
from datetime import date, datetime


class JsonCustomEncoder(json.JSONEncoder):
	"""
	让时间能够json
	"""
	def default(self, value):
		if isinstance(value, datetime):
			return value.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(value, date):
			return value.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, value)


def get_data_list(request, model_cls, table_config):
	"""
	查找方法
	:param request:
	:param model_cls:
	:param table_config:
	:return:
	"""
	values_list = []
	for row in table_config:
		if not row['q']:
			continue
		values_list.append(row['q'])
	
	from django.db.models import Q
	
	condition = request.GET.get('condition')
	condition_dict = json.loads(condition)
	
	con = Q()
	for name, values in condition_dict.items():
		ele = Q()
		ele.connector = 'OR'
		for item in values:
			ele.children.append((name, item))
		con.add(ele, 'AND')
	
	server_list = model_cls.objects.filter(con).values(*values_list)
	return server_list
