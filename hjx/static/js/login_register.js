// 判断邮箱是否有效
function IsEmail(str) {
    var reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    return reg.test(str);
}

//注册函数
function check() {
    var email = document.getElementById("email").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var confrim_password = document.getElementById("confrim_password").value;
    var email_error = document.getElementById('email_error');
    if (!IsEmail(email)) {
        email_error.innerHTML = '请输入有效的邮箱'
        return false;
    } else {
        email_error.innerHTML = '';
        if (username == '' || username == null) {
            alert("用户名不能为空");
            return false;
        } else {
            if (username.length >= 10) {
                alert('用户名长度不能超过十个字符');
                return false;
            } else {
                console.log(confrim_password);
                console.log(password);
                if (confrim_password != password) {
                    alert("两次输入密码不正确，请重新输入");
                    return false;
                }else {
                    var rss111=document.getElementById('rss111');
                    if (rss111.getAttribute('data-cc')) {
                        return true;
                    }else {
                        alert('请完成滑块验证');
                        var drag=document.querySelector('.drag');
                        drag.style.display='block';
                        return false;
                    }
                }
            }

        }

    }

}

// 登录页面的tab兰切换
var menus = document.querySelector('#menus').querySelectorAll('li');
var opinions = document.querySelector('#opinions').querySelectorAll('li');
opinions[0].style.display = 'block';
for (var i = 0; i < menus.length; i++) {
    menus[i].onmouseover = function () {
        for (var i = 0; i < menus.length; i++) {
            menus[i].className = 'none';  //取消所有的样式
            opinions[i].style.display = 'none';
        }
        this.className = 'hover';
        var index = this.getAttribute('data-index');
        opinions[index].style.display = 'block';
    }
}
// 获取验证码函数
function get_verificate_code_check() {
    var get_email = document.getElementById('get_email').value;
    if (!IsEmail(get_email)) {
        alert(get_email + '不是有效的邮箱，请输入有效的邮箱号码');
        return false;
    }
    return true;
}



//前端图片验证码
var global = '';   //定义一个全局变量
var password_enter = document.querySelector('.password_enter');
// var div = document.getElementById('vificate_code');
var options = {
    canvasId: 'mycanvas',
    width: 200,
    height: 50,
    txt: ''
}
//生产验证码
function produceCode(options) {
    var code = "";
    var random = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
    for (var i = 0; i < 4; i++) {
        var index = Math.floor(Math.random() * 62);
        code += random[index];
    }
    options.txt = code;
    global = code;
    password_enter.setAttribute('data-content', code);
    // div.innerHTML = code;

}
//产生随机数字
function randomNum(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}
//产生随机颜色
function randomColor(min, max) {
    var r = randomNum(min, max);
    var g = randomNum(min, max);
    var b = randomNum(min, max);
    return "rgb(" + r + "," + g + "," + b + ")";
}
//生产验证码背景
function code(options) {
    produceCode(options);
    var canvas = document.getElementById(options.canvasId);
    canvas.width = options.width || 300;//画布的宽
    canvas.height = options.height || 150;//画布的高
    var ctx = canvas.getContext("2d");//创建一个canvas对象
    ctx.textBaseline = "middle";
    ctx.fillStyle = randomColor(60, 255);
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < options.txt.length; i++) {
        var txt = options.txt.charAt(i);
        ctx.font = '50px SimHei';
        ctx.fillStyle = randomColor(60, 180); /**随机生成字体颜色*/
        ctx.shadowOffsetY = randomNum(-3, 3);
        ctx.shadowBlur = randomNum(-3, 3);
        ctx.shadowColor = "rgba(0, 0, 0, 0.3)";
        var x = options.width / (options.txt.length + 1) * (i + 1);
        var y = options.height / 2;
        var deg = randomNum(-30, 30);
        /**设置旋转角度和坐标原点*/
        ctx.translate(x, y);
        ctx.rotate(deg * Math.PI / 180);
        ctx.fillText(txt, 0, 0);
        /**恢复旋转角度和坐标原点*/
        ctx.rotate(-deg * Math.PI / 180);
        ctx.translate(-x, -y);
    }

    /**1~4条随机干扰线随机出现*/
    for (var i = 0; i < randomNum(1, 4); i++) {
        ctx.strokeStyle = randomColor(40, 180);
        ctx.beginPath();
        ctx.moveTo(randomNum(0, options.width), randomNum(0, options.height));
        ctx.lineTo(randomNum(0, options.width), randomNum(0, options.height));
        ctx.stroke();
    }
    /**绘制干扰点*/
    for (var i = 0; i < options.width / 6; i++) {
        ctx.fillStyle = randomColor(0, 255);
        ctx.beginPath();
        ctx.arc(randomNum(0, options.width), randomNum(0, options.height), 1, 0, 2 * Math.PI);
        ctx.fill();
    }
}
window.onload = function () {
    code(options)
}


//判断验证码是否正确
var incode = document.getElementById('incode');

function fore_vificate() {
    if (incode.value == password_enter.getAttribute('data-content')) {
        // alert('恭喜，登录成功！');
        return true;
    } else {
        alert('图片验证码错误，无法验证通过，请重试');
        incode.value = "";
        code(options);
        return false;
    }
}



