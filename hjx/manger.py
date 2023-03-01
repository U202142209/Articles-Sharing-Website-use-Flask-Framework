from flask import Flask,render_template,url_for,redirect,request,flash,session
from send_email import *
from sql import Mydatabase
import time
from functools import wraps
import os
import uuid


app=Flask(__name__,template_folder='tenplates')
app.config['SECRET_KEY']='zhaoweijia_haijixing'   # 使用CSRF认证
app.secret_key='zhaoweijia_haijixing'
UPLOAD_FOLDER = os.path.join(app.root_path,'static','uploads')
ALLOWED_EXTENSIONS = set(['txt','png', 'jpg','cs', 'jpeg', 'gif','docx','doc','xlsx','xls','exe','pdf','rar'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def show_date(arg):
    return arg[0:11]
def show_5(arg):
    if len(arg)>=5:
        return arg[0:5]
    else:return arg
def show_20(arg):
    if len(arg)>=30:
        return arg[0:29]+'....'
    else:return arg
app.add_template_filter(show_20,'show_20')    # 添加模板过滤函数
app.add_template_filter(show_5,'show_5')
app.add_template_filter(show_date,'show_date')


# 装饰器，判断用户是否登录
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session or 'administrator' in session:     # 判断用户是否登录，或者管理员登录
            return f(*args, **kwargs)  # 如果登录，继续执行被装饰的函数
        else:                          # 如果没有登录，提示无权访问
            flash('无权访问，请先登录', 'error')
            return redirect(url_for('login'))       # 跳转到登录页面
    return wrap


@app.route('/')
def index():
    database = Mydatabase()    # 查询所有的文章
    arts = database.fetchall('select id ,title,create_time,author from articles where public="%s" order by create_time desc'%'True')
    database=Mydatabase()       # 查询所有的热榜链接
    hots=database.fetchall('select * from recommends where attribute="%s"   order by create_time desc '%"hot")
    database=Mydatabase()
    techs=database.fetchall('select * from recommends where attribute="%s"  order by create_time desc'%"tech")
    database=Mydatabase()
    recs=database.fetchall('select * from recommends where attribute="%s"  order by create_time desc '%"rec")
    return render_template('index.html',arts=arts,hots=hots,recs=recs,techs=techs)

# 全部文章列表
@app.route('/getlist/<string:attribute>')
def getlist(attribute):
    if attribute=='hot':
        database = Mydatabase()  # 查询所有的文章
        hots = database.fetchall('select * from recommends where attribute="%s"   order by create_time desc ' % "hot")
        return render_template('getlist.html',hots=hots,title='热门推荐')
    elif attribute=='rec':
        database = Mydatabase()
        recs = database.fetchall('select * from recommends where attribute="%s"  order by create_time desc ' % "rec")
        return render_template('getlist.html',title='站长推荐',recs=recs)
    elif attribute=='tech':
        database = Mydatabase()
        techs = database.fetchall('select * from recommends where attribute="%s"  order by create_time desc' % "tech")
        return render_template('getlist.html',techs=techs,title='技术分享')
    elif attribute=='art':
        database = Mydatabase()  # 查询所有的文章
        arts = database.fetchall(
            'select id ,title,create_time,author from articles where public="%s" order by create_time desc' % 'True')
        return render_template('getlist.html',arts=arts,title='所有博客')

# 反馈
@app.route('/feedback.html',methods=['POST','GET'])
def feedback():
    if request.method=='POST':
        email = request.values.get('email')
        content = request.values.get('content')
        print('email;',email,'content',content)
        database = Mydatabase()
        reuslt = database.insert('insert into feedback (email, content, ip, create_time) values("%s","%s","%s","%s")' % (email,content,request.remote_addr, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
        if reuslt :
            session['feedback']=True
            try:
                now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                send_email("2869210303@qq.com", '【消息提醒】。邮箱 %s 在好记性博客网站上给您留下了反馈，反馈内容；%s，反馈时间； %s。请查收。' %(email,content,now_time) )
            except:
                print('error；邮箱发送失败')
    return render_template('feedback.html')

# 注册
@app.route('/register.html')
def register():
    return render_template('register.html')

# 用户注册
@app.route('/registerin', methods=['GET','POST'])
def registerin():
    if request.method=='POST':
        email=request.values.get('email')
        username = request.values.get('username')
        password = request.values.get('password')
        confrim_password=request.values.get('confrim_password')
        if len(username)>=10:
            flash('用户名的长度不能超过十个字符','error')
        else:
             if confrim_password !=password:
                 flash('两次密码输入不正确，请重新输入','error')
             else:
                database = Mydatabase()
                fetchone=database.fetchhone('select email from user where email= "%s" '%email)
                if fetchone!=None:
                    flash('邮箱  '+email+'  已经注册了账号，不能重复注册','error')
                    return render_template('register.html')
                else:
                    database=Mydatabase()
                    resule=database.fetchall('select username from user where username = "%s" '%username)
                    if resule!=[]:
                        flash('用户名 '+username+' 已经存在，请重新设置','error')
                        print('用户名 '+username+' 已经存在，请重新设置')
                    else:
                        database=Mydatabase()
                        sql='insert into user(id,username,email,password,create_time,create_ip,verificated) values("%s","%s","%s","%s","%s","%s","%s")'%(time.time(),username,email,password,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),request.remote_addr,False)
                        result=database.insert(sql)
                        if result:
                            flash('注册成功','success')
                            return redirect(url_for('register'))
                        else :
                            flash('注册失败','error')
    return render_template('register.html')


@app.errorhandler(404)              # 错误页面
def page_not_found(e):
    return render_template('404.html'), 404

# 用户登录
@app.route('/login.html', methods=['GET','POST'])
def login():
    # 密码登录
    if request.method=='POST':
        username = request.values.get('username')
        password = request.values.get('password')
        database=Mydatabase()
        result = database.fetchhone('select email,username,password from user where username= "%s" and password="%s" ' %(username,password ))
        if result!=None:
            session['logged_in']=True
            session['username']=username
            session['email']=result[0]
            try:
                now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                send_email(result[0], '【消息提醒】。您在好记性博客网站 http://101.43.229.177  登录成功。登录时间；%s' % now_time)
            except:
                print('error；邮箱发送失败')
            return redirect(url_for('console'))
        else:
            flash('用户名或密码不正确，请重新输入','error')
    return render_template('login.html')

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#管理员登录
@app.route('/administrator.html',methods=['POST','GET'])
def administrator():
    if  'administrator' in session:
        database = Mydatabase()
        users = database.fetchall('select * from user order by create_time desc')
        database = Mydatabase()
        articles = database.fetchall('select * from articles order by create_time desc')
        database = Mydatabase()
        recommends = database.fetchall('select * from recommends order by create_time desc')
        database = Mydatabase()
        feedbacks = database.fetchall('select * from feedback  order by create_time desc')
        database=Mydatabase()
        files=database.fetchall('select id,name,attribute,create_time,type from files  order by create_time desc')
        return render_template('administrator.html', users=users, articles=articles, recommends=recommends,
                               feedbacks=feedbacks,files=files)
    if request.method=='POST':
        username = request.values.get('username')
        password = request.values.get('password')
        if username=='administrator' and password=='password':
            session['administrator']=True
            return redirect(url_for('administrator'))
        else:
            flash('账号或密码不正确.', 'error')
    return render_template('administrator_login.html')


# 管理员删除用户
@app.route('/deleteuser/<string:id>', methods=['GET','POST'])
def deleteuser(id):
    datbase=Mydatabase()
    datbase.delete('delete from user where id="%s"'%id)
    datbase=Mydatabase()
    username=request.values.get('username')
    datbase.delete('delete from articles where author="%s"'%username)
    # print('删除成功！')
    return redirect(url_for('administrator'))

# 用户控制台
@app.route('/console.html')
@is_logged_in   # 判断是否登录
def console():
    database=Mydatabase()
    articles=database.fetchall('select * from articles where author="%s" order by create_time desc '%session['username'])
    return render_template('console.html',articles=articles)

# 用户添加博客
@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
    title = request.values.get('title')
    editor= request.values.get('editor')
    public = request.values.get('public')
    database=Mydatabase()
    reuslt=database.insert('insert into articles(id,title,content,create_time,author,public,hot,love,read_num) values("%s","%s","%s","%s","%s","%s","%s","%d","%d")'%(time.time(),title,editor,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),session['username'],public,False,0,1))
    if reuslt:
        # print('新增博客成功！')
        flash('新增博客成功！','success')
    else:
        print('新增博客失败.请不要使用特殊符号')
        flash('新增博客失败.请不要使用特殊符号','error')
    return redirect(url_for('console'))

# 删除博客
@app.route('/deletearticle/<string:id>', methods=['GET','POST'])
@is_logged_in
def deletearticle(id):
    datbase=Mydatabase()
    datbase.delete('delete from articles where id="%s"'%id)
    flash('删除博客成功！','success')
    if 'administrator' in session:
        return redirect(url_for('administrator'))
    else:
        return redirect(url_for('console'))

# 添加链接
@app.route('/add_recommends', methods=['GET','POST'])
@is_logged_in
def add_recommends():
    title = request.values.get('title')
    link= request.values.get('link')
    attribute= request.values.get('attribute')
    database=Mydatabase()
    reuslt = database.insert(
        'insert into recommends(id,title,link,create_time,attribute) values("%s","%s","%s","%s","%s")' % (time.time(), title, link, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), attribute))
    if reuslt:
        flash('新增链接成功！', 'success')
    else:
        # print('新增链接失败')
        flash('新增链接失败', 'error')
    return redirect(url_for('administrator'))

# 管理员删除链接
@app.route('/deleterecommend/<string:id>', methods=['GET','POST'])
@is_logged_in
def deleterecommend(id):
    database=Mydatabase()
    database.delete('delete from recommends where id="%s"'%id)
    flash('删除链接成功！','success')
    return redirect(url_for('administrator'))

#查看文章
@app.route('/article/<string:id>')
def article(id):
    datbase=Mydatabase()
    article=datbase.fetchhone('select id ,title,content,create_time,author,love,read_num from articles where id="%s"'%id)
    return render_template('article.html',article=article)

# 编辑博客
@app.route('/edit_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    database=Mydatabase()
    article=database.fetchhone('select title,content from articles where id="%s"'%id)
    if request.method=='POST':
        title = request.values.get('title_2')
        editor = request.values.get('editor_2')
        public = request.values.get('public_2')
        print(id)
        database = Mydatabase()
        database.delete('delete from articles where id="%s"'%id)
        database = Mydatabase()
        result = database.insert(
            'insert into articles(id,title,content,create_time,author,public,hot,love,read_num) values("%s","%s","%s","%s","%s","%s","%s","%d","%d")' % (
            id, title, editor, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), session['username'],
            public, False, 0, 1))
        if result:
            flash('编辑成功！','success')
            print('编辑成功！','success')
            return redirect(url_for('console'))
        else:
            flash('编辑失败，请不要出现特殊字符。图片等','error')
            print('编辑成功！','success')
    return render_template('edit_article.html',article=article)

# 管理员删除反馈
@app.route('/deletefeedback/<string:create_time>' ,methods=['GET','POST'])
@is_logged_in
def deletefeedback(create_time):
    database = Mydatabase()
    database.delete('delete from feedback where create_time="%s"' % create_time)
    flash('删除反馈成功！', 'success')
    return redirect(url_for('administrator'))

# 管理员查看反馈意见
@app.route('/lookfeedback/<string:create_time>',methods=['POST','GET'])
@is_logged_in
def lookfeedback(create_time):
    database = Mydatabase()
    feedback=database.fetchhone('select * from feedback where create_time="%s"' % create_time)
    return render_template('lookfeedback.html',feedback=feedback)


@app.route('/websitenav')
def websitenav():
    return render_template('websitenav.html')

# 获取邮箱，并发送验证码
@app.route('/get_code',methods=['POST','GET'])
def get_code():
    if request.method=='POST':
        email = request.values.get('email')
        database=Mydatabase()
        username=database.fetchhone('select username from user where email="%s" '%email)
        if username== None:
            flash('邮箱“%s”没有在本网站注册，无法发送验证码'%email,'error')
        else:
            result=main(email)
            print(result)
            if result==False:
                flash('验证码发送失败，请检查邮箱“%s"是否是有效的邮箱' % email, 'error')
            else:
                session['email']=email
                session['username']=username[0]
                session['verificate_code']=result+'1s6e9c%s5%5%sa0@qq.com&12&'
                flash('我们已经向”%s“发送了验证码，请输入验证码完成登录'%email,'success')
    return render_template('login.html')

# 验证邮箱验证码
@app.route('/verificate_code',methods=['POST','GET'])
def verificate_code():
    if request.method=='POST':
        verificate_code = request.values.get('verificate_code')
        if verificate_code==session['verificate_code'][0:6]:
            session['logged_in'] = True
            flash('登录成功！','success')
            return redirect(url_for('console'))
        else:
            flash('验证码输入不正确','error')
    return render_template('login.html')


# 以下时文件上传的路由
# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 产生随机文件名
def random_file(filename):
    ext = os.path.splitext(filename)[1]     # 获取文件后缀
    new_filename = uuid.uuid4().hex+ext     # 使用uuid生成随机字符
    return new_filename

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        avatar = request.files['avatar']
        print(avatar.filename)    # index.html
        print(os.path.splitext(avatar.filename)[1])  # .html
        # 判断文件是否上传，已经上传文件类型是否正确
        if avatar and allowed_file(avatar.filename):
            filename = random_file(avatar.filename)
            print(filename)
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            database=Mydatabase()
            reuslt = database.insert(
                'insert into files(id,name,attribute,create_time,type) values("%s","%s","%s","%s","%s")' % (
                filename,avatar.filename ,os.path.splitext(avatar.filename)[1], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),getfiletype(os.path.splitext(avatar.filename)[1])))
            if reuslt:
                print('保存成功.')
                flash('文件上传成功','success')
            else:
                print('数据插入数据库失败')
                flash('数据插入数据库失败','error')
        else :
            flash('文件不合要求','error')
    return redirect(url_for('administrator'))

# 资源下载
@app.route('/download')
def download():
    database=Mydatabase()
    files=database.fetchall('select id,name,create_time,type from files order by create_time desc')
    return render_template('download.html',files=files)


# 删除文件
@app.route('/removefile/<string:id>/<string:filename>' ,methods=['GET','POST'])
@is_logged_in
def removefile(id,filename):
    datbase = Mydatabase()
    datbase.delete('delete from files where id="%s"' % id)
    if os.path.exists(os.path.join(app.root_path,'static','uploads',id)):
        print('目标文件存在')
        os.remove(os.path.join(app.root_path,'static','uploads',id))
        print('成功删除文件 %s'%filename)
        flash('成功删除文件 %s'%filename,'success')
    else:
        print('文件%s不存在，无法删除'%filename)
        flash('文件%s不存在，无法删除'%filename,'error')
    return redirect(url_for('administrator'))


def getfiletype(filelastname):
    if filelastname in ['.png', '.jpg','.jpeg','.gif'] :
        return 'photo'
    elif filelastname in ['.docx','.doc']:
        return 'word'
    elif filelastname in ['.xlsx','.xls']:
        return 'excel'
    elif filelastname=='.txt':
        return 'txt'
    elif filelastname=='.cs':
        return 'cs'
    elif filelastname=='.pdf':
        return 'pdf'
    elif filelastname=='.rar':
        return 'rar'
    else:
        return 'exe'


if __name__ == '__main__':
    app.run(debug=True)
    # f=open('tenplates/register.html')
