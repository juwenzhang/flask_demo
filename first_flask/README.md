## Flask 常用的第三方包
* Flask-SQLAlchemy 用于实现的是操作数据库的
* Flask-migrate 用于实现数据库的迁移
* Flask-Mail 用于实现邮件发送
* Flask-WTF 用于实现表单验证
* Flask-Login 用于实现用户登录
* Flask-script 用于实现命令行接口
* Flask-RESTful 用于实现 RESTful API
* Flask-Bootstrap 用于实现 Bootstrap 前端框架
* Flask-Moment 用于实现时间格式化
* Flask-Uploads 用于实现文件上传

## 必要依赖
* 类似于我们的 nodejs 中的 dotenv 用于加载环境变量
* 我们现在需要的就是安装我们的 dotenv 包
* uv add python-dotenv

* uv add hypercorn
* 实现的是将 wsgi 服务转换为 asgi 服务