import os
import uuid

from flask import Flask, request, render_template

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path,'uploads')
ALLOWED_EXTENSIONS = set(['txt','png', 'jpg','cs', 'jpeg', 'gif','docx','js','html','dox','xlsx','xls','exe','pdf','rar'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def random_file(filename):
    ext = os.path.splitext(filename)[1]     # 获取文件后缀
    new_filename = uuid.uuid4().hex+ext     # 使用uuid生成随机字符
    return new_filename

@app.route('/upload',methods=['GET','POST'])
def upload():
    """

    头像上传表单页面
    :return:
    """
    if request.method == 'POST':
        # 接受头像字段
        avatar = request.files['avatar']
        print(avatar)             # <FileStorage: 'index.html' ('text/html')>
        print(type(avatar))       # <class 'werkzeug.datastructures.FileStorage'>
        print(avatar.filename)    # index.html
        print(os.path.splitext(avatar.filename)[1] )  # .html
        # 判断文件是否上传，已经上传文件类型是否正确
        if avatar and allowed_file(avatar.filename):
            # 生成一个随机文件名
            filename = random_file(avatar.filename)
            # 保存文件
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('保存成功.')
            return '保存成功'
        else :
            return "文件不合要求。"
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
