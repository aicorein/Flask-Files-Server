from flask import Flask, abort
from flask import request, session, redirect, flash
from flask import render_template, send_from_directory
from files import get_files_data, DEFAULT_PATH, DRIVERS_LIST, \
    get_current_path
import os
import re
from random import randint


# 创建项目以及初始化一些关键信息
app = Flask(__name__, template_folder='templates', static_folder='static', \
                static_url_path='/static')
# 这里是预先将值存储在系统环境变量中了
app.secret_key = os.getenv('SECRET_KEY')
# 匹配移动端设备的正则表达式
MATCH_EXP = 'Android|webOS|iPhone|iPod|BlackBerry'
# 设置登录用户名和密码
SPECIFY_UNAME = ''
SPECIFY_UPWD = ''



def verify():
    """
    验证登录状态
    """
    if ('uname' in session and 'upwd' in session \
            and session['uname'] == SPECIFY_UNAME \
            and session['upwd'] == SPECIFY_UPWD):
        return True
    else:
        return False


def mobile_check():
    """
    设备类型检查
    """
    try:
        if session.mobile == 'yes':
            return True
        elif session.mobile == 'no':
            return False
    except AttributeError:
        if re.search(MATCH_EXP, request.headers.get('User-Agent')):
            session.mobile = 'yes'
            return True
        else: 
            session.mobile = 'no'
            return False
    


def url_format(device_isMobile, default_load_url):
    """
    根据设备类型返回对应的资源 url
    """
    if device_isMobile:
        return './h5/m_' + default_load_url
    else:
        return default_load_url


def url_random_arg():
    """
    url添加一个随机参数，防止浏览器缓存
    """
    return randint(100000, 1000000)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    共享文件主页
    """
    # 判断是否已经在登录状态上
    device_isMobile = mobile_check()
    if verify():
        # 已经登录了，返回文件夹内文件信息（此时为默认路径）
        if request.method == 'GET':
            return render_template(url_format(device_isMobile, "index.html"), \
                    data = {
                        "files": get_files_data(DEFAULT_PATH),
                        "drivers": DRIVERS_LIST,
                        "currentPath": DEFAULT_PATH,
                    },
                    randomArg = url_random_arg())
        else:
            # POST 请求下获取传递的路径信息，并返回相应数据
            if request.form.get('pathText'):
                path_text = request.form.get('pathText')
                return render_template(url_format(device_isMobile, "index.html"), \
                    data = {
                        "files": get_files_data(path_text),
                        "drivers": DRIVERS_LIST,
                        "currentPath": get_current_path(),
                    },
                    randomArg = url_random_arg())
            else:
                abort(404)
    else:
        # 之前没有登录过,返回登录页
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页
    """
    device_isMobile = mobile_check()
    if request.method == 'GET':
        if verify():
            return redirect('/')
        else:
            # 之前没有登录过,返回一个登录页
            return render_template(url_format(device_isMobile, 'login.html'),
                    randomArg = url_random_arg())
    else:
        # 先保存才能验证
        uname = request.form.get('uname')
        upwd = request.form.get('upwd')
        session['uname'] = uname
        session['upwd'] = upwd
        if verify():
            # 重定向到首页
            return redirect('/')
        else:
            # 登录失败的情况
            flash("该用户名和密码不存在，请重试")
            return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    注销
    """
    if verify():
        # 声明重定向对象
        resp = redirect('/')
        # 删除值
        resp.delete_cookie('uname')
        resp.delete_cookie('upwd')
        session.pop('uname', None)
        session.pop('upwd', None)
        return resp
    else:
        # 没有登录过,返回登录页
        return redirect('/login')


@app.route("/download_file/<filename>")
def file_content(filename):
    """
    下载文件
    """
    if verify():
        # 若文件存在
        if filename in os.listdir(get_current_path()):
            # 发送文件 参数：路径，文件名
            return send_from_directory(get_current_path(), filename)
        else:
            # 否则返回错误页面
            device_isMobile = mobile_check()
            return render_template(url_format(device_isMobile, "download_error.html"), 
                    filename=filename,
                    randomArg = url_random_arg())
    else:
        return redirect('/login')


@app.route("/upload_file", methods=['GET', 'POST'])
def upload():
    """
    上传文件
    """
    if verify():
        if request.method == "POST":
            # 获取文件 拼接存储路径并保存
            upload_file = request.files['file']
            upload_file.save(os.path.join(get_current_path(), upload_file.filename))

            # 返回上传成功的消息给前端
            return '提示：上传的%s已经存储到了服务器中!' %upload_file.filename

        # 如果是 GET 方法：
        device_isMobile = mobile_check()
        return render_template(url_format(device_isMobile, "upload.html"),
                randomArg = url_random_arg())
    else:
        return redirect('/login')


if __name__ == '__main__':
    # 监听在所有 IP 地址上
    app.run(host='0.0.0.0', port=5000)
