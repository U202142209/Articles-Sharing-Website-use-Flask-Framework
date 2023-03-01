//管理元页面的tab栏切换
var admin_menu = document.querySelector('#admin_menu').querySelectorAll('li');
var admin_options = document.getElementById('admin_options').querySelectorAll('li');
admin_options[0].style.display = 'block';
for (var i = 0; i < admin_menu.length; i++) {
    admin_menu[i].onmouseover = function () {
        for (var i = 0; i < admin_menu.length; i++) {
            admin_menu[i].className = 'none';
            admin_options[i].style.display = 'none';
        }
        var index = this.getAttribute('data-index');
        admin_options[index].style.display = 'block';
        this.className = 'admin_hover';
    }
}

//表格试图效果,将需要视图的表格设置为class="view_table";
var view_table = document.querySelectorAll('.view_table');
console.log(view_table.length)
for (var i = 0; i < view_table.length; i++) {
    var view_table_trs = view_table[i].querySelectorAll('tr');
    for (var i = 0; i < view_table_trs.length; i++) {
        view_table_trs[i].onmouseover = function () {
            for (var i = 0; i < view_table_trs.length; i++) {
                view_table_trs[i].className = 'none';
            }
            this.className = 'trhover';
        }
    }
}

//表格试图效果,将需要视图的表格设置为class="view_table";
var view_table_2 = document.querySelectorAll('.view_table_2');
for (var i = 0; i < view_table_2.length; i++) {
    // 获取每个表格,每个表格的tr标签
    var view_table_trs_2 = view_table_2[i].querySelectorAll('tr');
    for (var j = 0; j < view_table_trs_2.length; j++) {
        // 给每个tr注册事件
        view_table_trs_2[j].onmouseover = function () {
            for (var k = 0; k < view_table_trs_2.length; k++) {
                view_table_trs_2[k].className = 'none';
            }
            this.className = 'trhover';
        }
    }
}
var view_table_3 = document.querySelectorAll('.view_table_3');
for (var i = 0; i < view_table_3.length; i++) {
    // 获取每个表格,每个表格的tr标签
    var view_table_trs_3 = view_table_3[i].querySelectorAll('tr');
    for (var j = 0; j < view_table_trs_3.length; j++) {
        // 给每个tr注册事件
        view_table_trs_3[j].onmouseover = function () {
            for (var k = 0; k < view_table_trs_3.length; k++) {
                view_table_trs_3[k].className = 'none';
            }
            this.className = 'trhover';
        }
    }
}

// 删除文章，确定提示框
function delete_check() {
    var r = confirm("你确定要删除吗，删除后将不可恢复");
    if (r == true) {
        return true;
    } else {
        return false;
    }
}
//表格视图效果
var view_table_trs_4 = document.getElementById('view_table_4').querySelectorAll('tr');
for (var i = 0; i < view_table_trs_4.length; i++) {
    view_table_trs_4[i].onmouseover = function () {
        for (var i = 0; i < view_table_trs_4.length; i++) {
            view_table_trs_4[i].className = 'none';
        }
        this.className = 'trhover';
    }
}
//表格视图效果
var view_table_trs_5 = document.getElementById('view_table_5').querySelectorAll('tr');
for (var i = 0; i < view_table_trs_5.length; i++) {
    view_table_trs_5[i].onmouseover = function () {
        for (var i = 0; i < view_table_trs_5.length; i++) {
            view_table_trs_5[i].className = 'none';
        }
        this.className = 'trhover';
    }
}
