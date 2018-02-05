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
			'tpl': "<a href='/User/groupinfo/{n1}/'/>{n1}</a>",
			'kwargs': {'n1': '@id'}
		},
		'attrs': {'name': 'id', 'edit-enable': 'true', 'origin': '@id',
		          'edit-type': 'input','class':'col-md-3'}
	},
	{
		'q': 'name',
		'title': '名称',
		'display': True,
		'text': {
			'tpl': "<a href='/User/groupinfo/{n1}/'/>{n2}</a>",
			'kwargs': {'n1': '@id','n2': '@name'}
		},
		'attrs': {'name': 'name', 'edit-enable': 'true', 'origin': '@name',
		          'edit-type': 'input','class':'col-md-3'}
	},]

search_config=[
	{'name': 'name__contains', 'text': '名称', 'search_type': 'input'},
	{'name': 'id__contains', 'text': '编号', 'search_type': 'input'},
 ]