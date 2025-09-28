# Python 核心库使用文档

本文档详细介绍Python中最常用的核心库（标准库）的使用方法和示例，包括json、sys、os、time、hashlib等，帮助你高效地进行Python开发。

## 1. JSON库

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式。Python的`json`模块提供了处理JSON数据的功能。

### 1.1 JSON序列化（Python对象转JSON）

```python
import json

# 将Python对象转换为JSON字符串
# 基本类型转换
python_obj = {
    "name": "Alice",
    "age": 30,
    "is_student": False,
    "courses": ["Math", "Physics", "Chemistry"],
    "address": {
        "city": "New York",
        "zip_code": "10001"
    },
    "grades": (95, 87, 92)
}

# 转换为JSON字符串
json_str = json.dumps(python_obj)
print(json_str)
# 输出: {"name": "Alice", "age": 30, "is_student": false, "courses": ["Math", "Physics", "Chemistry"], "address": {"city": "New York", "zip_code": "10001"}, "grades": [95, 87, 92]}

# 格式化输出
pretty_json = json.dumps(python_obj, indent=4, sort_keys=True)
print(pretty_json)
# 输出格式化的JSON字符串

# 写入JSON文件
with open("data.json", "w") as json_file:
    json.dump(python_obj, json_file, indent=4)
```

### 1.2 JSON反序列化（JSON转Python对象）

```python
import json

# JSON字符串
json_str = '{"name": "Bob", "age": 25, "city": "Boston", "skills": ["Python", "Java", "C++"]}'

# 将JSON字符串转换为Python对象
python_obj = json.loads(json_str)
print(type(python_obj))  # 输出: <class 'dict'>
print(python_obj["name"])  # 输出: Bob
print(python_obj["skills"])  # 输出: ['Python', 'Java', 'C++']

# 从文件读取JSON
with open("data.json", "r") as json_file:
    data = json.load(json_file)
    print(data["name"])  # 输出: Alice
```

### 1.3 自定义对象的JSON序列化

```python
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 自定义编码器
class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age, "__class__": "Person"}
        return super().default(obj)

# 使用自定义编码器
person = Person("Charlie", 35)
json_str = json.dumps(person, cls=PersonEncoder)
print(json_str)  # 输出: {"name": "Charlie", "age": 35, "__class__": "Person"}

# 自定义解码器
def person_decoder(obj):
    if "__class__" in obj and obj["__class__"] == "Person":
        return Person(obj["name"], obj["age"])
    return obj

# 使用自定义解码器
decoded_person = json.loads(json_str, object_hook=person_decoder)
print(decoded_person.name)  # 输出: Charlie
print(type(decoded_person))  # 输出: <class '__main__.Person'>
```

## 2. sys库

`sys`模块提供了访问Python解释器使用或维护的变量，以及与解释器交互的函数。

### 2.1 命令行参数

```python
import sys

# 命令行参数列表
print("命令行参数:", sys.argv)
# 执行: python script.py arg1 arg2
# 输出: 命令行参数: ['script.py', 'arg1', 'arg2']

# 参数数量
print("参数数量:", len(sys.argv))

# 脚本名称
print("脚本名称:", sys.argv[0])

# 如果没有足够的参数，可以提供默认值
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = "Guest"
print(f"Hello, {name}!")
```

### 2.2 系统信息

```python
import sys

# Python版本信息
print("Python版本:", sys.version)
print("Python版本信息元组:", sys.version_info)

# 操作系统信息
print("操作系统:", sys.platform)

# 解释器可执行文件路径
print("解释器路径:", sys.executable)

# 模块搜索路径
print("模块搜索路径:", sys.path)

# 最大递归深度
print("最大递归深度:", sys.getrecursionlimit())

# 设置递归深度
sys.setrecursionlimit(1500)
print("新的递归深度:", sys.getrecursionlimit())
```

### 2.3 标准输入/输出/错误流

```python
import sys

# 标准输出
print("使用print函数输出", file=sys.stdout)
sys.stdout.write("直接写入标准输出\n")

# 标准错误
sys.stderr.write("这是一条错误信息\n")

# 标准输入
# name = sys.stdin.readline().strip()
# print(f"你好, {name}!")

# 重定向输出
with open("output.txt", "w") as f:
    sys.stdout = f
    print("这条信息会被写入文件")
    # 恢复标准输出
sys.stdout = sys.__stdout__
print("这条信息会显示在屏幕上")
```

### 2.4 退出程序

```python
import sys

# 正常退出，状态码为0
sys.exit(0)  # 程序终止

# 异常退出，状态码为非0
sys.exit(1)  # 程序终止并返回错误码1

# 在try-except块中捕获SystemExit异常
try:
    sys.exit(1)
except SystemExit as e:
    print(f"捕获到退出信号: {e.code}")
```

## 3. os库

`os`模块提供了与操作系统交互的功能，如文件和目录操作、进程管理等。

### 3.1 文件和目录操作

```python
import os

# 当前工作目录
current_dir = os.getcwd()
print("当前工作目录:", current_dir)

# 改变工作目录
os.chdir("/path/to/directory")
print("新的工作目录:", os.getcwd())

# 列出目录内容
contents = os.listdir(current_dir)
print("目录内容:", contents)

# 创建目录
os.makedirs("new_directory", exist_ok=True)  # exist_ok=True 避免目录已存在时出错

# 删除目录
os.rmdir("new_directory")  # 只能删除空目录

# 递归删除目录（包括内容）
import shutil
shutil.rmtree("directory_with_contents")

# 文件重命名
os.rename("old_name.txt", "new_name.txt")

# 删除文件
os.remove("file_to_delete.txt")
```

### 3.2 路径操作

```python
import os

# 路径拼接
path = os.path.join("directory", "subdirectory", "file.txt")
print("拼接路径:", path)

# 分割路径
dir_path, file_name = os.path.split("/path/to/file.txt")
print("目录路径:", dir_path)
print("文件名:", file_name)

# 获取文件扩展名
file_name, extension = os.path.splitext("file.txt")
print("文件名:", file_name)
print("扩展名:", extension)

# 检查路径是否存在
print("路径是否存在:", os.path.exists("/path/to/check"))

# 检查是否为文件
print("是否为文件:", os.path.isfile("file.txt"))

# 检查是否为目录
print("是否为目录:", os.path.isdir("directory"))

# 获取绝对路径
abs_path = os.path.abspath("relative/path")
print("绝对路径:", abs_path)

# 获取规范化路径（解决..和.）
norm_path = os.path.normpath("/path/to/../file.txt")
print("规范化路径:", norm_path)  # 输出: /path/file.txt
```

### 3.3 环境变量

```python
import os

# 获取环境变量
path = os.environ.get("PATH")
print("PATH环境变量:", path)

# 设置环境变量
eos.environ["MY_VARIABLE"] = "my_value"
print("设置的环境变量:", os.environ["MY_VARIABLE"])

# 检查环境变量是否存在
if "HOME" in os.environ:
    print("HOME环境变量存在")

# 删除环境变量
if "MY_VARIABLE" in os.environ:
    del os.environ["MY_VARIABLE"]
```

### 3.4 执行系统命令

```python
import os

# 执行系统命令
# 返回值是命令的退出状态码
status = os.system("ls -la")
print("命令退出状态码:", status)

# 使用os.popen获取命令输出
output = os.popen("echo 'Hello, World!'").read()
print("命令输出:", output)

# 使用subprocess模块（推荐）
import subprocess

# 执行命令并获取输出
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print("标准输出:", result.stdout)
print("标准错误:", result.stderr)
print("退出状态码:", result.returncode)

# 执行命令并直接打印输出
subprocess.run(["echo", "Hello, World!"])

# 交互式执行命令
subprocess.run(["python"], shell=True)
```

### 3.5 文件状态和权限

```python
import os

# 获取文件状态
try:
    stat_info = os.stat("file.txt")
    print("文件大小:", stat_info.st_size)
    print("最后修改时间:", stat_info.st_mtime)
    print("最后访问时间:", stat_info.st_atime)
    print("inode更改时间:", stat_info.st_ctime)
except FileNotFoundError:
    print("文件不存在")

# 检查文件权限
print("是否可读:", os.access("file.txt", os.R_OK))
print("是否可写:", os.access("file.txt", os.W_OK))
print("是否可执行:", os.access("file.txt", os.X_OK))

# 修改文件权限
# os.chmod("file.txt", 0o755)  # rwxr-xr-x
```

## 4. time库

`time`模块提供了处理时间的功能，如获取当前时间、格式化时间、延迟执行等。

### 4.1 时间表示

```python
import time

# 获取当前时间戳（秒）
timestamp = time.time()
print("当前时间戳:", timestamp)

# 获取当前时间的结构体
time_struct = time.localtime(timestamp)
print("本地时间结构体:", time_struct)

# 获取UTC时间的结构体
utc_time_struct = time.gmtime(timestamp)
print("UTC时间结构体:", utc_time_struct)

# 从时间戳创建时间结构体
specific_time = time.localtime(1609459200)  # 2021-01-01 00:00:00
print("指定时间:", specific_time)
```

### 4.2 时间格式化

```python
import time

# 格式化当前时间
current_time = time.localtime()

# 格式化时间为字符串
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
print("格式化时间:", formatted_time)

# 常用的时间格式化符号
# %Y: 四位数年份（如 2023）
# %m: 两位数月份（01-12）
# %d: 两位数日期（01-31）
# %H: 24小时制小时数（00-23）
# %M: 分钟数（00-59）
# %S: 秒数（00-59）
# %a: 缩写星期名（如 Mon）
# %A: 完整星期名（如 Monday）
# %b: 缩写月份名（如 Jan）
# %B: 完整月份名（如 January）

# 自定义格式示例
date_str = time.strftime("%B %d, %Y", current_time)
print("自定义格式:", date_str)  # 输出: January 01, 2023

time_str = time.strftime("%I:%M %p", current_time)
print("12小时制时间:", time_str)  # 输出: 12:00 AM

# 解析字符串为时间结构体
parsed_time = time.strptime("2023-12-25 14:30:00", "%Y-%m-%d %H:%M:%S")
print("解析的时间:", parsed_time)
```

### 4.3 时间延迟

```python
import time

# 延迟执行（秒）
print("开始")
time.sleep(2)  # 延迟2秒
print("2秒后")

# 测量代码执行时间
start_time = time.time()

# 执行一些操作
for i in range(1000000):
    pass

end_time = time.time()
execution_time = end_time - start_time
print(f"执行时间: {execution_time:.6f}秒")

# 使用timeit模块更准确地测量时间
import timeit

code_to_test = '''
for i in range(1000000):
    pass
'''

time_taken = timeit.timeit(code_to_test, number=5)
print(f"平均执行时间: {time_taken/5:.6f}秒")
```

### 4.4 时区和夏令时

```python
import time
import datetime

# 检查是否为夏令时
current_time = time.localtime()
is_dst = current_time.tm_isdst
print("是否为夏令时:", is_dst)  # 1表示是，0表示否，-1表示未知

# 获取时区信息
tz_name = time.tzname
print("时区名称:", tz_name)

# 时区偏移量（秒）
tz_offset = time.timezone
print("UTC偏移量(秒):", tz_offset)
print("UTC偏移量(小时):", tz_offset / 3600)

# 使用datetime处理时区
from datetime import timezone, timedelta

# 创建时区对象
utc_plus_8 = timezone(timedelta(hours=8))

# 创建带有时区的datetime对象
now = datetime.datetime.now(utc_plus_8)
print("带时区的当前时间:", now)

# 转换时区
utc_now = now.astimezone(timezone.utc)
print("UTC时间:", utc_now)
```

## 5. hashlib库

`hashlib`模块提供了常见的哈希算法，如MD5、SHA1、SHA256等，用于生成数据的哈希值。

### 5.1 基本哈希操作

```python
import hashlib

# 创建哈希对象（MD5）
md5_hash = hashlib.md5()

# 更新哈希对象
data = "Hello, World!"
md5_hash.update(data.encode('utf-8'))

# 获取十六进制哈希值
hex_digest = md5_hash.hexdigest()
print("MD5哈希值:", hex_digest)
# 输出: 6cd3556deb0da54bca060b4c39479839

# 一次性计算哈希值
sha256_hash = hashlib.sha256("Hello, World!".encode('utf-8')).hexdigest()
print("SHA256哈希值:", sha256_hash)

# 支持的哈希算法
print("可用的哈希算法:", hashlib.algorithms_available)
print("保证可用的哈希算法:", hashlib.algorithms_guaranteed)
```

### 5.2 文件哈希计算

```python
import hashlib

def calculate_file_hash(file_path, algorithm='sha256', chunk_size=8192):
    """计算文件的哈希值"""
    # 创建哈希对象
    hash_obj = hashlib.new(algorithm)
    
    try:
        # 分块读取文件并更新哈希对象
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
        
        # 返回十六进制哈希值
        return hash_obj.hexdigest()
    except FileNotFoundError:
        return None

# 计算文件的MD5哈希值
file_path = "example.txt"
file_md5 = calculate_file_hash(file_path, 'md5')
print(f"文件的MD5哈希值: {file_md5}")

# 计算文件的SHA256哈希值
file_sha256 = calculate_file_hash(file_path)
print(f"文件的SHA256哈希值: {file_sha256}")
```

### 5.3 加盐哈希（用于密码存储）

```python
import hashlib
import os

# 生成随机盐值
salt = os.urandom(16)  # 16字节随机盐值
print("盐值(十六进制):", salt.hex())

# 创建带盐的哈希
password = "my_secure_password"

# 方法1：使用pbkdf2_hmac（推荐）
iterations = 100000
key_length = 32
password_hash = hashlib.pbkdf2_hmac(
    'sha256',               # 哈希算法
    password.encode('utf-8'),  # 密码
    salt,                   # 盐值
    iterations,             # 迭代次数
    key_length              # 密钥长度
)

print("PBKDF2哈希值(十六进制):", password_hash.hex())

# 方法2：简单拼接（不推荐用于密码存储）
simple_hash = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
print("简单加盐哈希值:", simple_hash)

# 密码验证函数
def verify_password(stored_hash, stored_salt, password, iterations=100000):
    """验证密码是否正确"""
    # 计算输入密码的哈希值
    test_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        stored_salt,
        iterations,
        len(stored_hash)
    )
    
    # 比较哈希值（使用compare_digest防止时序攻击）
    return hashlib.compare_digest(test_hash, stored_hash)

# 验证密码
is_correct = verify_password(password_hash, salt, "my_secure_password")
print("密码正确吗?", is_correct)  # 输出: True

is_correct = verify_password(password_hash, salt, "wrong_password")
print("密码正确吗?", is_correct)  # 输出: False
```

### 5.4 其他哈希功能

```python
import hashlib

# 创建自定义哈希对象
custom_hash = hashlib.new('sha1')
custom_hash.update(b"Hello, World!")
print("自定义哈希(SHA1):", custom_hash.hexdigest())

# 获取哈希对象的位数
print("MD5位数:", hashlib.md5().digest_size * 8)  # 输出: 128
print("SHA256位数:", hashlib.sha256().digest_size * 8)  # 输出: 256

# 获取哈希对象的内部状态（用于增量更新）
h = hashlib.sha256()
h.update(b"Hello")
current_state = h.copy()  # 复制当前状态
h.update(b", World!")
print("完整哈希:", h.hexdigest())

current_state.update(b", Python!")
print("分支哈希:", current_state.hexdigest())

# HMAC（基于哈希的消息认证码）
import hmac

key = b"my_secret_key"
data = b"Hello, World!"

# 创建HMAC
hmac_obj = hmac.new(key, data, hashlib.sha256)
hmac_hex = hmac_obj.hexdigest()
print("HMAC-SHA256:", hmac_hex)

# 验证HMAC
is_valid = hmac.compare_digest(hmac_hex, hmac.new(key, data, hashlib.sha256).hexdigest())
print("HMAC验证结果:", is_valid)  # 输出: True
```

## 6. 其他常用核心库

### 6.1 collections库

`collections`模块提供了额外的数据结构，如`defaultdict`、`Counter`、`OrderedDict`等。

```python
from collections import defaultdict, Counter, OrderedDict, namedtuple, deque

# defaultdict：带有默认值的字典
# 自动为不存在的键提供默认值
def_dict = defaultdict(int)  # 默认值为0
def_dict['a'] += 1
def_dict['b'] += 2
print("defaultdict:", dict(def_dict))  # 输出: {'a': 1, 'b': 2}

# Counter：用于计数的字典
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
word_count = Counter(words)
print("Counter:", word_count)  # 输出: Counter({'apple': 3, 'banana': 2, 'orange': 1})
print("最常见的2个单词:", word_count.most_common(2))  # 输出: [('apple', 3), ('banana', 2)]

# OrderedDict：保持插入顺序的字典
ordered_dict = OrderedDict()
ordered_dict['a'] = 1
ordered_dict['b'] = 2
ordered_dict['c'] = 3
print("OrderedDict:", dict(ordered_dict))  # 输出: {'a': 1, 'b': 2, 'c': 3}

# 注意：Python 3.7+ 中，普通字典也保持插入顺序

# namedtuple：命名元组
Point = namedtuple('Point', ['x', 'y'])
p1 = Point(10, 20)
p2 = Point(x=30, y=40)
print("命名元组:", p1)  # 输出: Point(x=10, y=20)
print("p1.x:", p1.x)  # 输出: 10
print("p1[0]:", p1[0])  # 输出: 10

# deque：双端队列（高效的两端操作）
d = deque([1, 2, 3])
d.append(4)         # 从右端添加
print("添加后:", d)  # 输出: deque([1, 2, 3, 4])
d.appendleft(0)     # 从左端添加
print("左端添加后:", d)  # 输出: deque([0, 1, 2, 3, 4])
print("弹出右端:", d.pop())  # 输出: 4
print("弹出左端:", d.popleft())  # 输出: 0
print("最终deque:", d)  # 输出: deque([1, 2, 3])
```

### 6.2 random库

`random`模块提供了生成随机数的功能。

```python
import random

# 生成[0.0, 1.0)之间的随机浮点数
print("随机浮点数:", random.random())

# 生成[a, b]之间的随机整数
print("随机整数(1-10):", random.randint(1, 10))

# 生成[a, b)之间的随机整数
print("随机整数(1-9):", random.randrange(1, 10))

# 生成[a, b]之间的随机浮点数
print("随机浮点数(1-5):", random.uniform(1, 5))

# 从序列中随机选择一个元素
colors = ['red', 'green', 'blue', 'yellow']
print("随机选择颜色:", random.choice(colors))

# 从序列中随机选择多个元素（有放回）
print("随机选择3个颜色(有放回):", random.choices(colors, k=3))

# 从序列中随机选择多个元素（无放回）
print("随机选择2个颜色(无放回):", random.sample(colors, 2))

# 打乱序列（原地修改）
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print("打乱后的列表:", numbers)

# 设置随机种子（用于可重复的随机序列）
random.seed(42)
print("固定种子的随机数:", random.random())
random.seed(42)
print("相同种子的随机数:", random.random())  # 与上一个值相同
```

### 6.3 re库（正则表达式）

`re`模块提供了正则表达式操作，用于字符串匹配和处理。

```python
import re

# 基本匹配
pattern = r"hello"
text = "Hello, world! hello everyone."

# 检查是否匹配
match = re.search(pattern, text)  # 区分大小写
print("匹配结果:", match)  # None，因为区分大小写

# 不区分大小写的匹配
match = re.search(pattern, text, re.IGNORECASE)
print("匹配结果:", match.group())  # 输出: Hello

# 查找所有匹配项
matches = re.findall(r"hello", text, re.IGNORECASE)
print("所有匹配项:", matches)  # 输出: ['Hello', 'hello']

# 替换匹配项
new_text = re.sub(r"hello", "hi", text, flags=re.IGNORECASE)
print("替换后的文本:", new_text)  # 输出: hi, world! hi everyone.

# 分割字符串
parts = re.split(r"[, ]+", text)  # 按逗号和空格分割
print("分割后的部分:", parts)  # 输出: ['Hello', 'world!', 'hello', 'everyone.']

# 分组
pattern = r"(\d{4})-(\d{2})-(\d{2})"  # 匹配日期格式 YYYY-MM-DD
text = "今天是2023-12-25，明天是2023-12-26。"
matches = re.finditer(pattern, text)

for match in matches:
    print("完整匹配:", match.group())
    print("年份:", match.group(1))
    print("月份:", match.group(2))
    print("日期:", match.group(3))

# 编译正则表达式（多次使用时更高效）
pattern = re.compile(r"\d+")  # 匹配一个或多个数字
text = "有123个苹果和456个橘子。"

# 使用编译后的模式
matches = pattern.findall(text)
print("找到的数字:", matches)  # 输出: ['123', '456']

# 常用的正则表达式模式
# 邮箱
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
print("邮箱匹配:", re.match(email_pattern, "user@example.com"))

# 手机号（中国大陆）
phone_pattern = r"^1[3-9]\d{9}$"
print("手机号匹配:", re.match(phone_pattern, "13812345678"))

# URL\url_pattern = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
print("URL匹配:", re.match(url_pattern, "https://www.example.com"))
```

### 6.4 datetime库

`datetime`模块提供了处理日期和时间的类，如`date`、`time`、`datetime`、`timedelta`等。

```python
from datetime import date, time, datetime, timedelta

# 创建date对象
today = date.today()
print("今天的日期:", today)  # 输出: 2023-12-25
print("年:", today.year)
print("月:", today.month)
print("日:", today.day)

# 创建指定日期
birthday = date(1990, 1, 1)
print("生日:", birthday)

# 日期差
delta = today - birthday
print(f"已经过了{delta.days}天")

# 创建time对象
current_time = time(14, 30, 45)
print("当前时间:", current_time)
print("小时:", current_time.hour)
print("分钟:", current_time.minute)
print("秒:", current_time.second)

# 创建datetime对象
now = datetime.now()
print("当前日期时间:", now)  # 输出: 2023-12-25 14:30:45.123456
print("年:", now.year)
print("月:", now.month)
print("日:", now.day)
print("小时:", now.hour)
print("分钟:", now.minute)
print("秒:", now.second)
print("微秒:", now.microsecond)

# 创建指定日期时间
specific_datetime = datetime(2023, 12, 25, 18, 0, 0)
print("指定日期时间:", specific_datetime)

# 格式化datetime
datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
print("格式化日期时间:", datetime_str)

# 解析字符串为datetime
parsed_datetime = datetime.strptime("2023-12-25 18:00:00", "%Y-%m-%d %H:%M:%S")
print("解析的日期时间:", parsed_datetime)

# timedelta：时间间隔
one_day = timedelta(days=1)
one_hour = timedelta(hours=1)
one_minute = timedelta(minutes=1)
one_second = timedelta(seconds=1)

# 日期时间运算
tomorrow = now + one_day
print("明天的这个时候:", tomorrow)

yesterday = now - one_day
print("昨天的这个时候:", yesterday)

# 自定义时间间隔
custom_delta = timedelta(days=2, hours=3, minutes=30)
future = now + custom_delta
print(f"{custom_delta}后的时间:", future)

# 计算两个datetime之间的差异
diff = tomorrow - yesterday
print(f"两个日期之间的差异: {diff.days}天, {diff.seconds//3600}小时")

# UTC时间
utc_now = datetime.utcnow()
print("UTC当前时间:", utc_now)
```

### 6.5 logging库

`logging`模块提供了灵活的日志记录功能，用于记录程序运行时的信息、警告和错误。

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 日期格式
    handlers=[
        logging.FileHandler("app.log"),  # 写入文件
        logging.StreamHandler()  # 输出到控制台
    ]
)

# 创建logger对象
logger = logging.getLogger(__name__)

# 记录不同级别的日志
logger.debug("这是一条调试信息")  # 不会显示，因为日志级别设置为INFO
logger.info("这是一条信息")
logger.warning("这是一条警告")
logger.error("这是一条错误信息")
logger.critical("这是一条严重错误信息")

# 异常日志记录
try:
    result = 10 / 0
except ZeroDivisionError as e:
    logger.exception("发生了除零错误")  # 会自动包含异常堆栈信息

# 日志级别
# DEBUG < INFO < WARNING < ERROR < CRITICAL

# 关闭日志
# logging.shutdown()
```

### 6.6 configparser库

`configparser`模块用于处理配置文件，可以读取和写入INI格式的配置文件。

```python
import configparser

# 创建配置解析器
config = configparser.ConfigParser()

# 读取配置文件
config.read('config.ini')

# 获取配置值
# 如果配置文件不存在，可以使用默认值
if 'database' in config:
    db_host = config.get('database', 'host', fallback='localhost')
    db_port = config.getint('database', 'port', fallback=3306)
    db_user = config.get('database', 'user', fallback='root')
    db_password = config.get('database', 'password', fallback='')
    print(f"数据库配置: {db_host}:{db_port}, 用户: {db_user}")

# 写入配置文件
config['app'] = {
    'debug': 'true',
    'port': '8080',
    'host': '0.0.0.0'
}

config['logging'] = {
    'level': 'INFO',
    'file': 'app.log'
}

with open('new_config.ini', 'w') as configfile:
    config.write(configfile)

# 配置示例 (config.ini)
"""
[database]
host = localhost
port = 3306
user = root
password = secret

app_debug = true
"""
```

### 6.7 csv库

`csv`模块提供了读写CSV（逗号分隔值）文件的功能。

```python
import csv

# 读取CSV文件
with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # 获取表头
    print("表头:", header)
    
    # 读取数据行
    for row in reader:
        print("行数据:", row)  # row是列表类型

# 读取CSV到字典
with open('users.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(f"用户: {row['name']}, 年龄: {row['age']}")

# 写入CSV文件
with open('new_users.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(['name', 'age', 'city'])
    # 写入数据行
    writer.writerow(['Alice', 30, 'New York'])
    writer.writerow(['Bob', 25, 'Boston'])
    writer.writerow(['Charlie', 35, 'Chicago'])

# 从字典写入CSV
users = [
    {'name': 'David', 'age': 40, 'city': 'Dallas'},
    {'name': 'Eve', 'age': 28, 'city': 'Denver'}
]

with open('dict_users.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # 写入表头
    for user in users:
        writer.writerow(user)
```

### 6.8 smtplib库

`smtplib`模块提供了发送电子邮件的功能。

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 发送纯文本邮件
def send_text_email(sender, password, recipients, subject, body):
    # 创建邮件对象
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    
    try:
        # 连接SMTP服务器
        server = smtplib.SMTP('smtp.example.com', 587)  # 使用实际的SMTP服务器和端口
        server.starttls()  # 启用TLS加密
        server.login(sender, password)  # 登录SMTP服务器
        
        # 发送邮件
        server.sendmail(sender, recipients, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")
    finally:
        # 关闭连接
        server.quit()

# 发送带附件的邮件
def send_email_with_attachment(sender, password, recipients, subject, body, file_path):
    # 创建多部分邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    
    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    try:
        with open(file_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), Name=file_path.split('/')[-1])
            attachment['Content-Disposition'] = f'attachment; filename="{file_path.split('/')[-1]}"'
            msg.attach(attachment)
        
        # 发送邮件
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
            print("带附件的邮件发送成功")
    except Exception as e:
        print(f"带附件的邮件发送失败: {e}")

# 示例使用（需要替换为实际的邮箱信息）
# send_text_email(
#     'your_email@example.com',
#     'your_password_or_app_password',
#     ['recipient1@example.com', 'recipient2@example.com'],
#     '测试邮件',
#     '这是一封测试邮件。'
# )

# send_email_with_attachment(
#     'your_email@example.com',
#     'your_password_or_app_password',
#     ['recipient@example.com'],
#     '带附件的测试邮件',
#     '请查看附件。',
#     'document.pdf'
# )
```

### 6.9 urllib库

`urllib`模块提供了用于处理URL的功能，包括发送HTTP请求、处理URL编码等。

```python
from urllib import request, parse
import json

# 发送GET请求
def send_get_request(url, params=None):
    # 如果有参数，添加到URL
    if params:
        url = f"{url}?{parse.urlencode(params)}"
        
    try:
        # 发送请求
        with request.urlopen(url) as response:
            # 获取响应内容
            data = response.read().decode('utf-8')
            # 获取响应状态码
            status_code = response.status
            # 获取响应头
            headers = dict(response.getheaders())
            
            return {
                'status_code': status_code,
                'headers': headers,
                'data': data
            }
    except Exception as e:
        print(f"GET请求失败: {e}")
        return None

# 发送POST请求
def send_post_request(url, data=None, json_data=None, headers=None):
    req_headers = headers or {}
    req_data = None
    
    # 处理请求体
    if json_data:
        req_data = json.dumps(json_data).encode('utf-8')
        req_headers['Content-Type'] = 'application/json'
    elif data:
        req_data = parse.urlencode(data).encode('utf-8')
        req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        # 创建请求对象
        req = request.Request(url, data=req_data, headers=req_headers, method='POST')
        
        # 发送请求
        with request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            status_code = response.status
            headers = dict(response.getheaders())
            
            return {
                'status_code': status_code,
                'headers': headers,
                'data': data
            }
    except Exception as e:
        print(f"POST请求失败: {e}")
        return None

# 示例使用
# 发送GET请求
# response = send_get_request('https://httpbin.org/get', {'name': 'Alice', 'age': 30})
# if response:
#     print(f"状态码: {response['status_code']}")
#     print(f"响应头: {response['headers']}")
#     print(f"响应数据: {response['data']}")

# 发送POST请求（表单数据）
# response = send_post_request('https://httpbin.org/post', {'name': 'Bob', 'age': 25})
# if response:
#     print(f"状态码: {response['status_code']}")
#     print(f"响应数据: {response['data']}")

# 发送POST请求（JSON数据）
# response = send_post_request('https://httpbin.org/post', json_data={'name': 'Charlie', 'age': 35})
# if response:
#     print(f"状态码: {response['status_code']}")
#     print(f"响应数据: {response['data']}")

# 处理URL编码
eencoded_str = parse.quote('Hello World!')
print("编码后的字符串:", eencoded_str)  # 输出: Hello%20World%21

decoded_str = parse.unquote('Hello%20World%21')
print("解码后的字符串:", decoded_str)  # 输出: Hello World!
```

### 6.10 threading库

`threading`模块提供了多线程编程的功能，用于并行执行任务。

```python
import threading
import time

# 线程函数
def print_numbers(start, end, delay=0.1):
    """打印指定范围内的数字"""
    for i in range(start, end + 1):
        print(f"线程 {threading.current_thread().name}: {i}")
        time.sleep(delay)

# 创建线程
thread1 = threading.Thread(target=print_numbers, args=(1, 5), name="线程1")
thread2 = threading.Thread(target=print_numbers, args=(10, 15), name="线程2", daemon=True)  # 守护线程

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()  # 等待线程1结束
# thread2.join()  # 守护线程会随着主线程结束而结束

print("主线程结束")

# 线程同步 - Lock
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()  # 创建锁
    
    def increment(self):
        with self.lock:  # 使用上下文管理器获取锁
            self.value += 1
    
    def get_value(self):
        with self.lock:
            return self.value

# 线程同步 - 生产者-消费者模式
import queue

class ProducerConsumer:
    def __init__(self):
        self.queue = queue.Queue(maxsize=10)  # 创建最大容量为10的队列
        self.running = True
    
    def producer(self):
        for i in range(20):
            item = f"产品{i}"
            self.queue.put(item)  # 放入队列，如果队列满则阻塞
            print(f"生产者: 生产了 {item}, 当前队列大小: {self.queue.qsize()}")
            time.sleep(0.2)
    
    def consumer(self):
        while self.running:
            try:
                item = self.queue.get(timeout=1)  # 从队列取出，如果队列为空则阻塞，最多等待1秒
                print(f"消费者: 消费了 {item}, 当前队列大小: {self.queue.qsize()}")
                self.queue.task_done()  # 标记任务完成
                time.sleep(0.5)
            except queue.Empty:
                if not self.running:
                    break
    
    def run(self):
        # 创建生产者和消费者线程
        producer_thread = threading.Thread(target=self.producer)
        consumer_thread = threading.Thread(target=self.consumer)
        
        # 启动线程
        producer_thread.start()
        consumer_thread.start()
        
        # 等待生产者结束
        producer_thread.join()
        
        # 等待队列清空
        self.queue.join()
        
        # 停止消费者
        self.running = False
        consumer_thread.join()
        
        print("所有任务完成")

# 示例使用
# pc = ProducerConsumer()
# pc.run()
```

## 7. 总结

Python的核心库提供了丰富的功能，从基本的文件操作到高级的数据处理，从简单的时间计算到复杂的加密算法，应有尽有。本文档介绍了最常用的几个核心库：json、sys、os、time和hashlib，以及一些其他常用的库如collections、random、re、datetime、logging、configparser、csv、smtplib、urllib和threading。

掌握这些核心库的使用方法，可以帮助你更加高效地编写Python代码，避免重复造轮子。Python的核心库设计优雅，使用方便，是Python语言强大生态系统的重要组成部分。

在实际开发中，建议优先使用Python的核心库，因为它们经过了广泛的测试和优化，并且与Python解释器一起安装，无需额外配置。当核心库无法满足需求时，再考虑使用第三方库。

希望本文档能够帮助你更好地理解和应用Python的核心库，提升你的Python编程技能。