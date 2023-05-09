from flask import Flask
from flask import render_template, send_from_directory, request, redirect, url_for
import os
import time

# 全局变量 共享的文件夹路径 可以根据需求更改
DIRECTORY_PATH = r"C:\Users\Tim\mine\projects\Python\FlaskProjects\MyNas\files"

# 创建项目
app = Flask(__name__)
app.config['SECURE_KEY'] = 'mynas20220907'


# 获取文件信息的函数
def get_files_data():
    files = []
    for i in os.listdir(DIRECTORY_PATH):
        if len(i.split(".")) == 1:  # 判断此文件是否为一个文件夹
            continue

        # 拼接路径
        file_path = DIRECTORY_PATH + "/" + i
        name = i
        size = os.path.getsize(file_path)  # 获取文件大小
        ctime = time.localtime(os.path.getctime(file_path))  # 格式化创建当时的时间戳

        # 列表信息
        files.append({
            "name": name,
            "size": size,
            "ctime": "{}年{}月{}日".format(ctime.tm_year, ctime.tm_mon, ctime.tm_mday),  # 拼接年月日信息
        })
    return files


@app.route("/")
def index():
    """共享文件主页"""
    return render_template("index.html", files=get_files_data())


@app.route("/download_file/<filename>")
def file_content(filename):
    """下载文件的URL"""
    if filename in os.listdir(DIRECTORY_PATH):  # 如果需求下载文件存在
        # 发送文件 参数：文件夹路径，文件相对路径，文件名
        return send_from_directory(DIRECTORY_PATH, filename)
    else:
        # 否则返回错误页面
        return render_template("download_error.html", filename=filename)


@app.route("/upload_file", methods=['GET', 'POST'])
def upload():
    """上传文件的URL 支持GET/POST请求"""
    if request.method == "POST":
        # 获取文件 拼接存储路径并保存
        upload_file = request.files.get("upload_file")
        upload_file.save(os.path.join(DIRECTORY_PATH, upload_file.filename))

        #  返回上传成功的模板
        return render_template("upload_ok.html", filename=upload_file.filename)

        # 上传的网页
    return render_template("upload.html")


if __name__ == '__main__':
    # 在局域网上开启端口
    app.run()
