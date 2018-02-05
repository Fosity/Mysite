table_config = [
	{
		'q': None,  # 数据查询字段
		'title': '选择',  # 显示标题
		'display': True,  # 是否显示
		'text': {  # 显示内容
			'tpl': "<input type='checkbox' value='{n1}' />",  # 显示内容
			'kwargs': {'n1': '@id'}  # @id 代表在数据列表(server_list)中找到 id的值，@@ 代表在全局变量中找到对应的值 ，然后替换tpl中的n1值
		},
		'attrs': {'nid': '@id','class':'col-md-1'}  # 在 标签里面增加 nid=@id 从数据列表中找
		
	},
	{
		'q': 'id',
		'title': '编号',
		'display': True,
		'text': {
			'tpl': "<a href='/User/usersinfo/{n1}/'/>{n1}</a>",
			'kwargs': {'n1': '@id'}
		},
		'attrs': {'name': 'id', 'edit-enable': 'true', 'origin': '@id',
		          'edit-type': 'input','class':'col-md-1'}
	},
	{
		'q': 'username',
		'title': '名字',
		'display': True,
		'text': {
			'tpl': "<a href='/User/usersinfo/{n1}/'/>{n2}</a>",
			'kwargs': {'n1': '@id','n2': '@username'}
		},
		'attrs': {'name': 'username', 'edit-enable': 'true', 'origin': '@username',
		          'edit-type': 'input','class':'col-md-3'}
	},
	{
		'q': 'email',
		'title': '邮箱',
		'display': True,
		'text': {
			'tpl':"<a href='/User/usersinfo/{n1}/'/>{n2}</a>",
			'kwargs': {'n1': '@id','n2': '@email'}
		},
		'attrs': {'name': 'email', 'edit-enable': 'true', 'origin': '@email',
		          'edit-type': 'input','class':'col-md-4'}
	},
	{
		'q': 'user2group__group__name',
		'title': '用户组名',
		'display': True,
		'text': {
			'tpl': "{n1}",
			'kwargs': {'n1': '@user2group__group__name'}
		},
		'attrs': {'name': 'user2group__group_id', 'edit-enable': 'true', 'origin': '@user2group__group__name',
		          'edit-type': 'select','global_key':'Group_name','class':'col-md-3'}
	},
 ]

search_config=[
	{'name': 'username__contains', 'text': '用户名', 'search_type': 'input'},
	{'name': 'email__contains', 'text': '邮箱', 'search_type': 'input'},
    {'name': 'user2group__group_id', 'text': '用户组名', 'search_type': 'select', 'global_name': 'Group_name'},
]