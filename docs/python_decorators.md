# Python 装饰器语法总结

装饰器是Python中一种强大的语法特性，它允许我们在不修改原函数代码的情况下扩展或修改函数的行为。本文档将详细介绍Python装饰器的语法和使用方法。

## 1. 装饰器基础

### 装饰器的本质

装饰器本质上是一个返回函数的函数，它接收一个函数作为参数，并返回一个新的函数。

```python
# 简单的装饰器示例
def my_decorator(func):
    def wrapper():
        print("装饰器开始执行")
        func()
        print("装饰器结束执行")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")

# 调用被装饰的函数
say_hello()
```

输出结果：
```
装饰器开始执行
Hello, World!
装饰器结束执行
```

### @ 语法糖

`@my_decorator` 是 Python 的语法糖，等价于 `say_hello = my_decorator(say_hello)`。

## 2. 带参数的装饰器

### 带参数的被装饰函数

当被装饰的函数带有参数时，装饰器的 wrapper 函数需要接收这些参数。

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("装饰器开始执行")
        result = func(*args, **kwargs)
        print("装饰器结束执行")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# 调用带参数的被装饰函数
greet("Alice")
```

### 带参数的装饰器

装饰器本身也可以接收参数，这需要在原有装饰器外层再嵌套一层函数。

```python
def repeat(num_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(num_times=3)
def say_hello():
    print("Hello, World!")

# 调用被装饰的函数
say_hello()
```

## 3. 常见装饰器类型

### 3.1 函数装饰器

最基本的装饰器类型，用于装饰函数。

```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"执行函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 执行完毕")
        return result
    return wrapper

@log_execution
def add(a, b):
    return a + b
```

### 3.2 类装饰器

使用类作为装饰器，需要实现 `__call__` 方法。

```python
class Logger:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print(f"执行函数: {self.func.__name__}")
        result = self.func(*args, **kwargs)
        print(f"函数 {self.func.__name__} 执行完毕")
        return result

@Logger
def multiply(a, b):
    return a * b
```

### 3.3 装饰器链

一个函数可以同时应用多个装饰器，执行顺序是从下到上。

```python
def decorator1(func):
    def wrapper(*args, **kwargs):
        print("装饰器1开始执行")
        result = func(*args, **kwargs)
        print("装饰器1结束执行")
        return result
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("装饰器2开始执行")
        result = func(*args, **kwargs)
        print("装饰器2结束执行")
        return result
    return wrapper

@decorator1
@decorator2
def say_hello():
    print("Hello, World!")

# 执行顺序: decorator1 -> decorator2 -> say_hello -> decorator2 -> decorator1
say_hello()
```

### 3.4 保留元数据的装饰器

使用 `functools.wraps` 可以保留被装饰函数的元数据（如函数名、文档字符串等）。

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("装饰器开始执行")
        result = func(*args, **kwargs)
        print("装饰器结束执行")
        return result
    return wrapper

@my_decorator
def say_hello():
    """打印问候语"""
    print("Hello, World!")

# 查看函数名和文档字符串
print(say_hello.__name__)  # 输出: say_hello
print(say_hello.__doc__)   # 输出: 打印问候语
```

## 4. 装饰器的实际应用场景

### 4.1 计时装饰器

用于测量函数执行时间。

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    print("函数执行完毕")

slow_function()
```

### 4.2 缓存装饰器

用于缓存函数的结果，避免重复计算。

```python
import functools

def cache(func):
    cache_dict = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache_dict:
            cache_dict[args] = func(*args)
        return cache_dict[args]
    
    return wrapper

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(30))
```

### 4.3 权限验证装饰器

用于验证用户权限。

```python
import functools

def requires_permission(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get('permission') != permission:
                raise PermissionError(f"需要 {permission} 权限")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@requires_permission('admin')
def admin_operation(user, data):
    print(f"管理员 {user['name']} 操作数据: {data}")

# 使用示例
admin_user = {'name': 'Alice', 'permission': 'admin'}
regular_user = {'name': 'Bob', 'permission': 'user'}

admin_operation(admin_user, 'important data')  # 正常执行
# admin_operation(regular_user, 'important data')  # 抛出权限错误
```

### 4.4 日志记录装饰器

用于记录函数调用信息。

```python
import functools
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"调用函数: {func.__name__}, 参数: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"函数 {func.__name__} 执行成功, 结果: {result}")
            return result
        except Exception as e:
            logging.error(f"函数 {func.__name__} 执行失败: {e}")
            raise
    return wrapper

@log_function_call
def divide(a, b):
    return a / b

divide(10, 2)  # 正常执行
# divide(10, 0)  # 记录错误
```

### 4.5 重试装饰器

用于在函数执行失败时自动重试。

```python
import functools
import time
import logging

def retry(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    logging.warning(f"函数 {func.__name__} 执行失败, {retries}/{max_retries} 重试...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_retries=3, delay=2)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise Exception("随机失败")
    print("函数执行成功")

unstable_function()
```

## 5. 装饰器的高级用法

### 5.1 类方法装饰器

装饰器不仅可以装饰普通函数，还可以装饰类方法。

```python
import functools

class MyClass:
    @staticmethod
    def static_method():
        print("这是一个静态方法")
        
    @classmethod
    def class_method(cls):
        print(f"这是一个类方法，类名: {cls.__name__}")
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

# 使用示例
obj = MyClass()
MyClass.static_method()  # 调用静态方法
MyClass.class_method()   # 调用类方法
obj.value = 10          # 使用 setter
print(obj.value)        # 使用 getter
```

### 5.2 动态装饰器

在运行时动态决定是否应用装饰器。

```python
def conditional_decorator(condition, decorator):
    def wrapper(func):
        if condition:
            return decorator(func)
        else:
            return func
    return wrapper

# 根据条件决定是否应用装饰器
DEBUG = True

@conditional_decorator(DEBUG, log_execution)
def my_function():
    print("函数执行")
```

### 5.3 带状态的装饰器

装饰器可以维护状态信息。

```python
import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"函数 {func.__name__} 已调用 {wrapper.calls} 次")
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def say_hello():
    print("Hello, World!")

# 多次调用函数
say_hello()
say_hello()
say_hello()
```

## 6. 装饰器的最佳实践

1. **使用 `functools.wraps` 保留原函数的元数据**
2. **保持装饰器简单明确**，一个装饰器只负责一项功能
3. **为装饰器添加适当的文档字符串**
4. **使用装饰器类而不是嵌套函数**，当装饰器需要维护复杂状态时
5. **避免过度使用装饰器**，这会使代码难以理解和调试

## 7. 常见的内置装饰器

Python 内置了一些常用的装饰器：

- `@property`: 将方法转换为属性
- `@staticmethod`: 定义静态方法
- `@classmethod`: 定义类方法
- `@functools.lru_cache`: 实现缓存功能
- `@functools.singledispatch`: 实现单分派泛型函数

```python
import functools

# 使用 lru_cache 缓存函数结果
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 使用 singledispatch 实现函数重载
@functools.singledispatch
def process_data(data):
    print(f"处理通用数据: {data}")

@process_data.register(str)
def _(data):
    print(f"处理字符串: {data}")

@process_data.register(int)
def _(data):
    print(f"处理整数: {data}")

# 使用示例
process_data(10)       # 输出: 处理整数: 10
process_data("hello")  # 输出: 处理字符串: hello
process_data([1, 2])   # 输出: 处理通用数据: [1, 2]
```

## 8. 总结

Python 装饰器是一种强大的语法特性，它允许我们以非侵入式的方式扩展或修改函数的行为。通过合理使用装饰器，我们可以提高代码的可读性、可维护性和复用性。

装饰器的应用场景非常广泛，包括但不限于：日志记录、性能监控、缓存、权限验证、输入验证、错误处理等。掌握装饰器的使用技巧，对于编写高质量的 Python 代码非常重要。