(function (jq) {
    var CREATE_SEARCH_CONDITION = true;
    var GLOBAL_DICT = {};
    //创建format方法
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function getSearchCondition() {
        var condition = {};
        $('.search-list').find('input[type="text"],select').each(function () {

            /* 获取所有搜索条件 */
            var name = $(this).attr('name');
            var value = $(this).val();
            if (condition[name]) {
                condition[name].push(value);
            } else {
                condition[name] = [value];
            }

        });
        return condition;
    }

    //初始化时发送ajax获得数据
    function initial(url) {
        var searchCondition = getSearchCondition();
        $.ajax({
            url: url,
            type: "GET",
            data: {condition: JSON.stringify(searchCondition)},
            dataType: 'JSON',
            success: function (arg) {
                //{'global_dict':{},   全局
                //'table_config':{},  所有配置
                //'server_list':{},   所有数据
                // }
                $.each(arg.global_dict, function (k, v) {
                    GLOBAL_DICT[k] = v
                });
                //把全局存放在 浏览器上

                initTableHeader(arg.table_config);  //生成头部
                initTableBody(arg.server_list, arg.table_config);  //填入数据
                initSearch(arg.search_config);  //初始化搜索框
            }
        })

    }

    function initSearch(searchConfig) {
        if (searchConfig && CREATE_SEARCH_CONDITION) {

            CREATE_SEARCH_CONDITION = false;
            // 找到searchArea ul，
            $.each(searchConfig, function (k, v) {
                var li = document.createElement('li');
                $(li).attr('search_type', v.search_type);
                $(li).attr('name', v.name);
                if (v.search_type == 'select') {
                    $(li).attr('global_name', v.global_name);
                }

                var a = document.createElement('a');
                a.innerHTML = v.text;
                $(li).append(a);
                $('.searchArea ul').append(li);
            });

            // 初始化默认搜索条件
            // searchConfig[0],进行初始化
            // 初始化默认选中值
            $('.search-item .searchDefault').text(searchConfig[0].text);
            if (searchConfig[0].search_type == 'select') {
                var sel = document.createElement('select');
                $(sel).attr('class', 'form-control');
                $.each(GLOBAL_DICT[searchConfig[0].global_name], function (k, v) {
                    var op = document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op)
                });
                $('.input-group').append(sel);
            } else {
                // <input type="text" class="form-control" aria-label="...">
                var inp = document.createElement('input');
                $(inp).attr('name', searchConfig[0].name);
                $(inp).attr('type', 'text');
                $(inp).attr('class', 'form-control');
                $('.input-group').append(inp);
            }


        }
    }

    //生成table 表头
    function initTableHeader(tableConfig) {
        /*
         [
         {'q':'id','title':'ID'},
         {'q':'hostname','title':'主机名'},
         ]
         */
        $('#tbHead').empty(); //清空表头
        var tr = document.createElement('tr'); //生成tr
        $.each(tableConfig, function (k, v) {
            if (v.display) {
                var tagTh = document.createElement('th'); // 生成th
                tagTh.innerHTML = v.title;              //在<th>中插入值，表名用title
                $(tr).append(tagTh);  //把<th>插入到<tr>中
            }
        });
        $('#tbHead').append(tr);  //把tr插入tbHead中
    }

    //生成table 内容
    function initTableBody(serverList, tableConfig) {
        $('#tbBody').empty();    //清空表内容
        //对数据进行循环 例如{'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
        $.each(serverList, function (datek, daterow) {
            var tr = document.createElement('tr'); //定义tr标签
            tr.setAttribute('nid', daterow.id); //在tr标签中增加nid=xx
            //对配置进行循环
            $.each(tableConfig, function (configk, configrow) {
                if (configrow.display) {
                    var td = document.createElement('td');

                    // 在td中添加内容
                    var newKwargs = {};
                    $.each(configrow.text.kwargs, function (configTextKwargsk, configTextKwargsrow) {
                        var newconfigText = configTextKwargsrow;
                        //如果 text.kwargs中存在@@xxxx值，则用global中xxxx的数据代替。
                        if (configTextKwargsrow.substring(0, 2) == '@@') {
                            var global_dict_key = configTextKwargsrow.substring(2, configTextKwargsrow.length);
                            var dateNid = daterow[configrow.q];
                            $.each(GLOBAL_DICT[global_dict_key], function (gk, gv) {
                                //gk 为位置，gv为元素
                                if (gv[0] == dateNid) {
                                    newconfigText = gv[1];
                                }
                            })
                        }
                        //如果 text.kwargs中存在@xxx值，则用数据中的 xxx的数据代替。
                        else if (configTextKwargsrow[0] == '@') {
                            newconfigText = daterow[configTextKwargsrow.substring(1, configTextKwargsrow.length)];
                        }
                        newKwargs[configTextKwargsk] = newconfigText;
                    });
                    var newText = configrow.text.tpl.format(newKwargs);
                    td.innerHTML = newText;

                    // 在td标签中添加属性
                    $.each(configrow.attrs, function (configAttrk, configAttrrow) {
                        //如果 attr中存在 @xxx的值，则从用户提供的数据中找到xxx的数据代替
                        if (configAttrrow[0] == '@') {
                            td.setAttribute(configAttrk, daterow[configAttrrow.substring(1, configAttrrow.length)])
                        } else {
                            td.setAttribute(configAttrk, configAttrrow)
                        }

                    });

                    $(tr).append(td);//把td插入tr中
                }
            });
            $('#tbBody').append(tr);
        })
    }

    //切换成输入状态
    function trIntoEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                //找到下拉框的数据源
                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global_key')];

                //添加下拉菜单
                var selectTag = document.createElement('select');
                $(selectTag).attr('class','form-control');
                var origin = $(this).attr('origin');

                $.each(deviceTypeChoices, function (k, v) {
                    var option = document.createElement('option');
                    $(option).text(v[1]);
                    $(option).val(v[0]);
                    if (v[1] == origin) {
                        $(option).prop('selected', true);
                    }
                    $(selectTag).append(option);
                });
                $(this).html(selectTag);  //把td变成select标签
            } else {
                //如果不是select，就是input
                var oldtext = $(this).text();
                var inputTag = document.createElement('input');
                $(inputTag).val(oldtext);
                $(inputTag).attr('class','col-md-10 form-control');
                $(this).html(inputTag);
            }
        });
    }

    //切换成完成状态
    function trOutEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                var option = $(this).find('select')[0].selectedOptions;
                $(this).attr('new-origin', $(option).val());
                $(this).html($(option).text());
            } else {
                var inputVal = $(this).find('input').val();
                $(this).html(inputVal);
            }
        })
    }

    jq.extend({
        showTable: function (url) {
            initial(url);

            //checkbox绑定事件  ：点击进入编辑模式，在点退出编辑模式
            $('#tbBody').on('click', ':checkbox', function () {
                if ($('#inOutEditMode').hasClass('EditMode')) {
                    var $tr = $(this).parent().parent();
                    if ($(this).prop('checked')) {
                        $(this).parent().parent().css('background-color','#EEDC82');
                        trIntoEdit($tr);

                    } else {
                        $(this).parent().parent().css('background-color','');
                        trOutEdit($tr);
                    }
                }
            });

            //所有按钮绑定事件
            //进入或退出编辑模式 class=EditMode时为编辑模式。
            $('#inOutEditMode').click(function () {
                if ($(this).hasClass('EditMode')) {
                    // 退出编辑模式
                    $(this).removeClass('EditMode');
                    $(this).text('进入编辑模式');
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                             $(this).parent().parent().css('background-color','');
                            trOutEdit($tr);
                        }
                    })
                } else {
                    // 进入编辑模式
                    $(this).addClass('EditMode');
                    $(this).text('退出编辑模式');

                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            $(this).parent().parent().css('background-color','#EEDC82');
                            trIntoEdit($tr);
                        }
                    })
                }
            });
            // 如果 处于编辑模式，checkbox全选则变成编辑模式，否则只是选中
            $('#checkAll').click(function () {
                if ($('#inOutEditMode').hasClass('EditMode')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        //把没有 选中的checkbox 变成选中状态
                        if (!$(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            $(this).parent().parent().css('background-color','#EEDC82');
                            trIntoEdit($tr);
                            $(this).prop('checked', true);
                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').prop('checked', true); //把所有的checked 变成true
                }
            });
            // 反转模式
            $('#checkReverse').click(function () {
                if ($('#inOutEditMode').hasClass('EditMode')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                             $(this).parent().parent().css('background-color','');
                            trOutEdit($tr);
                            $(this).prop('checked', false);
                        } else {
                            $(this).parent().parent().css('background-color','#EEDC82');
                            trIntoEdit($tr);
                            $(this).prop('checked', true);
                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false);
                        } else {
                            $(this).prop('checked', true);
                        }
                    })
                }
            });
            //全部取消
            $('#checkCancel').click(function () {
                if ($('#inOutEditMode').hasClass('EditMode')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        //把选中的都变成取消状态，并且退出编辑
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                             $(this).parent().parent().css('background-color','');
                            trOutEdit($tr);
                            $(this).prop('checked', false);
                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').prop('checked', false);
                }
            });
            //刷新
            $('#refresh').click(function () {
                initial(url)
            });
            //删除数据
            $('#multiDel').click(function () {
                // 从checkbox里面获取 要删除的 value
                var idList = [];
                $('#tbBody').find(':checked').each(function () {
                    var v = $(this).val();
                    idList.push(v)
                });
                //通过 delete 的request方法向后端传输数据
                $.ajax({
                    url: url,
                    type: 'delete',
                    data: JSON.stringify(idList),
                    success: function (arg) {
                        location.reload()
                    }
                })
            });
            //保存修改数据
            $('#save').click(function () {
                if ($('#inOutEditMode').hasClass('EditMode')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            $(this).parent().parent().css('background-color','');
                            trOutEdit($tr);
                        }
                    })
                }

                var all_list = [];
                // 获取用户修改过的数据
                $('#tbBody').children().each(function () {
                    // $(this) = tr
                    var $tr = $(this);
                    var nid = $tr.attr('nid');
                    var row_dict = {};
                    var flag = false;
                    $tr.children().each(function () {
                        if ($(this).attr('edit-enable')) {
                            if ($(this).attr('edit-type') == 'select') {
                                var newData = $(this).attr('new-origin');
                                var oldData = $(this).attr('origin');
                                if (newData) {
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        row_dict[name] = newData;
                                        flag = true;
                                    }
                                }

                            } else {
                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');
                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    flag = true;
                                }
                            }
                        }
                    });
                    if (flag) {
                        row_dict['nid'] = nid;
                    }
                    all_list.push(row_dict)
                });
                // 通过Ajax提交后台
                $.ajax({
                    url: url,
                    type: 'PUT',
                    data: JSON.stringify(all_list),
                    success: function (arg) {
                        console.log(arg);
                    }
                })
            });

            $('.search-list').on('click', 'li', function () {
                // 点击li执行函数
                var wenben = $(this).text();
                var searchType = $(this).attr('search_type');
                var name = $(this).attr('name');
                var globalName = $(this).attr('global_name');

                // 把显示替换
                $(this).parent().prev().find('.searchDefault').text(wenben);


                if (searchType == 'select') {
                    /*
                        [
                            [1,‘文本’],
                            [1,‘文本’],
                            [1,‘文本’],
                        ]
                     */
                    var sel = document.createElement('select');
                    $(sel).attr('class', 'form-control');
                    $(sel).attr('name', name);
                    $.each(GLOBAL_DICT[globalName], function (k, v) {
                        var op = document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(sel);
                } else {
                    var inp = document.createElement('input');
                    $(inp).attr('class', 'form-control');
                    $(inp).attr('name', name);
                    $(inp).attr('type', 'text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);
                }

            });

            $('.search-list').on('click', '.add-search-condition', function () {
                // 拷贝的新一搜索项
                var newSearchItem = $(this).parent().parent().clone();
                $(newSearchItem).find('.add-search-condition span').removeClass('glyphicon-plus').addClass('glyphicon-minus');
                $(newSearchItem).find('.add-search-condition').addClass('del-search-condition').removeClass('add-search-condition');
                $('.search-list').append(newSearchItem);
            });

            $('.search-list').on('click', '.del-search-condition', function () {
                $(this).parent().parent().remove();
            });

            $('#doSearch').click(function () {
                initial(url);
            })
        }
    })
})(jQuery);
