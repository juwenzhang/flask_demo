from hashlib import md5
import re
import json
from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
from werkzeug.routing import BaseConverter
import settings
import time

# 自定义正则表达式转换器集合
class RegexConverter(BaseConverter):
    """基础正则表达式转换器"""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

class MobileConverter(BaseConverter):
    """手机号转换器（中国大陆）"""
    regex = r'1[3-9]\d{9}'

class EmailConverter(BaseConverter):
    """邮箱地址转换器"""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class ChineseConverter(BaseConverter):
    """中文字符转换器"""
    regex = r'[\u4e00-\u9fa5]+'

class DateConverter(BaseConverter):
    """日期转换器 (YYYY-MM-DD 格式)"""
    regex = r'\d{4}-\d{2}-\d{2}'

class TimeConverter(BaseConverter):
    """时间转换器 (HH:MM:SS 格式)"""
    regex = r'\d{2}:\d{2}:\d{2}'

class IPConverter(BaseConverter):
    """IP地址转换器 (IPv4)"""
    regex = r'((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)'

"""
FLASK 的初始化参数
1. `import_name`：应用的导入名，通常使用 `__name__`，一般就是模块的名称。
2. `static_url_path`：静态文件的 URL 路径，默认是 `/static`。
3. `static_folder`：静态文件的文件夹，默认是 `static` 文件夹。
4. `template_folder`：模板文件的文件夹，默认是 `templates` 文件夹。
5. `instance_relative_config`：是否使用实例文件夹中的配置文件，默认是 `False`。
6. `root_path`：应用的根路径，默认是应用所在的文件夹。
"""
app = Flask(
    import_name=__name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='src/templates',
    instance_relative_config=False,
    root_path=None,
)

# 注册自定义转换器到Flask应用
app.url_map.converters['regex'] = RegexConverter
app.url_map.converters['mobile'] = MobileConverter
app.url_map.converters['email'] = EmailConverter
app.url_map.converters['chinese'] = ChineseConverter
app.url_map.converters['date'] = DateConverter
app.url_map.converters['time'] = TimeConverter
app.url_map.converters['ip'] = IPConverter

# 通过配置文件加载配置信息
try:
    app.config.from_pyfile('./settings.py')
    print(f"成功加载配置文件: HOST={app.config.get('HOST')}, PORT={app.config.get('PORT')}")
except Exception as e:
    print(f"加载配置文件失败: {e}")
    # 设置默认值
    app.config['HOST'] = '127.0.0.1'
    app.config['PORT'] = 5000

# 通过类名加载配置信息
app.config.from_object(settings.Config)
print(f"通过类名加载配置信息: HOST={app.config.get('HOST')}, PORT={app.config.get('PORT')}")

# 添加路由的方式：装饰器模式:@app.route
@app.route('/')
def index():
    # 使用字符串键名获取配置
    host_config = app.config.get('HOST')
    port_config = app.config.get('PORT')
    print(f"配置信息 - HOST: {host_config}, PORT: {port_config}")
    return f"Hello World! Running on {host_config}:{port_config}", 200

# 通过加载函数来实现: app.add_url_rule
def index_1():
    return "Hello, World!", 200
app.add_url_rule( # 一般用lambda表达式来实现
    rule='/hello',
    endpoint='hello',
    view_func=index_1,
    methods=['GET']
)

# 渲染模板: render_template request.method request.values
@app.route('/template', methods=['GET', 'POST'])
def template():
    # 根据用户的请求返回不同的东西
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.values.get('USERNAME')
        password = request.values.get('PASSWORD')
        if username and password:
            return f"POST - 用户名: {username}, 密码: {password}"
        elif not username:
            return "POST - 用户名不能为空"
        elif not password:
            return "POST - 密码不能为空"
        return "POST - 其他错误"
    else:
        return "其他请求方法"

# 反向解析 url_for redirect
@app.route('/order', endpoint='order')
def order():
    return "订单页面", 200
@app.route('/url_for')
def url_for_example():
    # 反向解析 order 路由的 URL
    order_url = url_for('order')  # 主要是为了在服务端内生成对应的后端路由吧
    # 重定向到 order 路由
    user_agent = request.user_agent
    if re.search(r'bot|spider|mac', user_agent.string, re.IGNORECASE):
        return redirect(order_url)
    elif re.search(r'android|ios', user_agent.string, re.IGNORECASE):
        return f"URL for order: {order_url}"
    elif user_agent != None:
        return "你是不是真人呀😭"
    else:
        return "你是个机器人吗？"


# 动态路由：根据用户的请求，动态的生成路由：也就是一部分是固定的，但是有些部分是需要进行匹配的
# 默认的类型是字符串
# 此时就需要使用路由转换器了
# 1. 类型转换器：默认是字符串，但是可以指定其他的类型：int | float | path | uuid
# 2. 自定义正则转换器： werkzeug.routing.PathConverter
@app.route('/user/<username>/<int:user_id>')
def user_profile(username, user_id):
    if type(username) == str and type(user_id) == int:
        return f"用户 {username} 的个人资料, 用户ID: {user_id}"
    else:
        return "参数错误"
# 自定义正则转换器使用示例
# 1. 使用基础正则转换器定义自定义模式
@app.route('/regexp/<regex(r"\d{3}-\d{3,8}"):phone>')
def regexp_phone(phone):
    """使用基础正则转换器匹配固定电话格式"""
    return f"匹配到的固定电话: {phone}"

# 2. 使用预定义的专用转换器
@app.route('/user/mobile/<mobile:phone>')
def user_mobile(phone):
    """使用手机号转换器"""
    return f"用户手机号: {phone}"

@app.route('/user/email/<email:email>')
def user_email(email):
    """使用邮箱转换器"""
    return f"用户邮箱: {email}"

@app.route('/search/chinese/<chinese:keyword>')
def search_chinese(keyword):
    """使用中文转换器"""
    return f"中文搜索关键词: {keyword}"

@app.route('/event/date/<date:event_date>')
def event_date(event_date):
    """使用日期转换器"""
    return f"事件日期: {event_date}"

@app.route('/event/time/<time:event_time>')
def event_time(event_time):
    """使用时间转换器"""
    return f"事件时间: {event_time}"

@app.route('/server/ip/<ip:ip_address>')
def server_ip(ip_address):
    """使用IP地址转换器"""
    return f"服务器IP地址: {ip_address}"

# 3. 组合使用多个转换器
@app.route('/meeting/<date:meeting_date>/<time:meeting_time>/<chinese:title>')
def meeting_detail(meeting_date, meeting_time, title):
    """组合使用多个转换器"""
    return f"会议信息 - 日期: {meeting_date}, 时间: {meeting_time}, 标题: {title}"

"""
1. request.method : 获取请求的方法
2. request.values : 获取请求中的参数
3. request.args : 获取GET请求中的参数
4. request.cookies : 获取请求中的cookie
5. request.form : 获取POST请求中的参数
6. request.json : 获取JSON格式的请求数据
7. request.files : 获取上传的文件
8. request.user_agent : 获取用户代理信息
9. request.remote_addr : 获取客户端的IP地址
10. request.path : 获取请求的路径
11. request.full_path : 获取请求的完整路径
12. request.url : 获取请求的URL
13. request.base_url : 获取请求的基础URL
14. request.url_root : 获取请求的根URL
15. request.script_root : 获取请求的脚本根URL
"""

@app.route(rule="/upload_single_file", methods=['POST'])
def upload_single_file():
    # 开始实现书写上传文件的接口
    FILE_VOLUMN = 'file'
    if request.method == 'POST':
        if FILE_VOLUMN not in request.files:
            return "请选择上传的文件"
        file = request.files.get(FILE_VOLUMN)
        md5_filename = md5(file.filename.encode('utf-8')).hexdigest()
        # 保存文件
        file.save(os.path.join(settings.UPLOAD_FOLDER, md5_filename))
        return f"文件 {file.filename} 上传成功"
@app.route(rule="/upload_multi_files", methods=['POST'])
def upload_multi_files():
    # 开始实现书写上传多个文件的接口
    FILE_VOLUMN = 'files'
    if request.method == 'POST':
        if FILE_VOLUMN not in request.files:
            return "请选择上传的文件"
        files = request.files.getlist(FILE_VOLUMN)
        for file in files:
            md5_filename = md5(file.filename.encode('utf-8')).hexdigest()
            # 保存文件
            file.save(os.path.join(settings.UPLOAD_FOLDER, md5_filename))
        return f"文件 {[file.filename for file in files]} 上传成功"

# 开始实现书写类似的响应字符串的形式吧
@app.route(rule='/response/<type>', methods=['GET'])
def response(type):
    # 获取得到客户端想要的响应类型
    TYPE = type
    if TYPE == 'str':
        return "响应了一个字符串"  # 响应状态码中的的类型是： text/html，对应的响应头字段是： Content-Type: text/html
    elif TYPE == 'json':
        return jsonify({
            "message": "响应了一个JSON字符串",
            "code": 200,
            "data": {
                "name": "张三",
                "age": 18
            }
        })  # 响应状态码中的的类型是： application/json
        # 在前后端的分离开发架构中，从数据库或者 redis 缓存中获取得到的数据就使用的是 json 吧
    elif TYPE == 'html':
        return render_template('index.html')  # 响应状态码中的的类型是： text/html
    elif TYPE == 'tuple':
        return "响应了一个元组", 200  # 响应状态码中的的类型是： text/html
    elif TYPE == 'make_response':
        # 用标准的构建响应对象来实现吧
        """
        是一个响应对象
        """
        """
        一般的话请求对象包含四个部分
            1. 请求行
            2. 空白行
            3. 请求头
            4. 请求体
        一般的话响应对象包含四个部分
            1. 状态行
            2. 空白行
            3. 响应头
            4. 响应体
        一般进行操作的是请求体，对于传递查询参数的那种的话
        一般我们的请求体的类型含有
            json 格式的字符串 application/json  --- 一般用户传递 json 格式的数据的提交
            form 格式的字符串 application/x-www-form-urlencoded --- 一般用户表单数据的上传提交
            二进制数据 multipart/form-data  --- 一般用户上传文件的提交
            文本数据 text/plain
        一般的话响应体的类型含有
            json 格式的字符串 application/json
            form 格式的字符串 application/x-www-form-urlencoded
            二进制数据 multipart/form-data
            文本数据 text/plain
        常见的 content-type 的类型，并且不会引起跨域的类型是
            text/plain
            application/x-www-form-urlencoded
            multipart/form-data  -- 学习如何对文件进行处理，md5 | zip | zstd | br 等等压缩算法
        其他常见的 content-type 类型，但是会引发跨域
            application/json
            text/html
            image/*  -- 学习如何对图片进行处理
            video/*  -- 学习如何对视频进行处理
            audio/*  -- 学习如何对音频进行处理
        后端设置强缓存
            Cache-Control: max-age=3600
            Expires: Mon, 26 Jul 2024 05:00:00 GMT
            Pragma: no-cache
            Vary: Accept-Encoding
            Server: Flask/1.1.2
            Date: Mon, 26 Jul 2024 05:00:00 GMT
            Connection: keep-alive
            Transfer-Encoding: chunked
            Content-Type: application/json
        后端设置协商缓存
            基于内容的协商缓存
            ETag: "1234567890"
            Last-Modified: Mon, 26 Jul 2024 05:00:00 GMT
            基于时间的协商缓存
            If-Modified-Since: Mon, 26 Jul 2024 05:00:00 GMT
            If-None-Match: "1234567890"
        对于现在的钱后端分离架构而言的话，实际上动态参数都是在前端路由中进行处理了
        而不是在后端路由中进行处理了，后端常见的就是这种获取得到前端的查询参数 + 请求头的实现形式
        以及重定向的话后端也是用得不是很多了的呢
        """
        # 创建JSON数据字典
        json_data = {
            "message": "响应了一个JSON字符串",
            "code": 200,
            "data": {
                "name": "张三",
                "age": 18
            }
        }
        response = make_response(json.dumps(json_data))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Server'] = 'Flask/1.1.2'
        response.headers['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        response.status_code = 200
        return response
    else:
        return "参数错误"
@app.route(rule='/strong_cache', methods=['GET'])
def strong_cache():
    response = make_response("响应了一个强缓存的字符串")
    response.headers['Cache-Control'] = 'max-age=3600'
    response.headers['Expires'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(time.time() + 3600))
    response.headers['Pragma'] = 'no-cache'
    response.headers['Vary'] = 'Accept-Encoding'
    response.status_code = 200
    return response
@app.route(rule='/communication_cache', methods=['GET'])
def communication_cache():
    # 给予内容的协商缓存
    response = make_response("响应了一个协商缓存的字符串")
    # 根据客户端内容生成唯一的 Etag
    etag = md5(response.get_data()).hexdigest()
    response.headers['ETag'] = f'"{etag}"'
    response.headers['If-Modified-Since'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    response.status_code = 200
    return response

"""
mysql | pgsql + redis 实现缓存的流程是
1. 每次请求的时候，先从 redis 中查询是否有缓存
2. 如果有缓存，直接返回缓存
3. 如果没有缓存，从数据库中查询
4. 如果数据库中没有数据，返回 404
5. 如果数据库中有数据，将数据缓存到 redis 中
6. 返回数据
在什么环境更新 Etag 和 Last-Modified 头
    1. 当数据库中的数据发生改变时，需要更新 Etag 和 Last-Modified 头
    2. 当客户端请求中包含 If-None-Match 头时，需要根据 Etag 进行判断
    3. 当客户端请求中包含 If-Modified-Since 头时，需要根据 Last-Modified 进行判断
在什么时候将更新的数据缓存到 redis 中
    1. 当数据库中的数据发生改变时，需要更新 redis 中的缓存
    2. 当客户端请求中包含 If-None-Match 头时，需要根据 Etag 进行判断
    3. 当客户端请求中包含 If-Modified-Since 头时，需要根据 Last-Modified 进行判断
对于协商缓存来说
    服务端响应的字段是： Etag | Last-Modified
    客户端请求的字段是： If-None-Match | If-Modified-Since
"""

if __name__ == '__main__':
    # 从配置中获取主机和端口
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    app.run(host=host, port=port)