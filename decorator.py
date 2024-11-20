import functools

#构建不带参数的装饰器
def logging(func):
    @functools.wraps(func)       #此装饰器：用于保留被装饰函数的一些重要属性
    def decorator(*args, **kwargs):
        print("%s called" % func.__name__)
        result = func(*args, **kwargs)
        print("%s ended" % func.__name__)
        return result
    return decorator

#使用装饰器
@logging
def text0(a,b):
    print("in function test0, a=%s, b=%s" % (a, b))
    return a+b





#构建带参数的装饰器
def params_chack(*types,**kwtypes):       #*types，**kwtypes  是用于接受各种类型参数
    def outer(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            #判断位置参数类型
            result = [isinstance(_param, _type) for _param, _type in zip(args, types)]   #列表推导式     isinstance是一个内置函数，用来判断一个对象是否是某个类型，此行作用是判断接受的参数是否为整数类型
            assert all(result), "params_chack: invalid parameters"                       #检查result中元素是否全为true，否则抛出异常params_chack: invalid parameters。assert 用于判断条件是否为真
            #判断关键字参数
            result = [isinstance(kwargs[_param],kwtypes[_param]) for _param in kwargs if _param in kwtypes]
            assert all(result), "params_chack: invalid parameters"
            return func(*args, **kwargs)
        return inner
    return outer


#使用装饰器
@params_chack(int,(list,tuple))
def text1(a,b):
    print("in function test1, a=%s, b=%s" % (a, b))
    return 1

@params_chack(int,str,c=(int, str))
def text2(a,b,c):
    print("in function test2, a=%s, b=%s, c=%s" % (a, b, c))
    return 2

# 在类的成员方法中使用装饰器
class Atext:
    @params_chack(int,str)
    def text(a,b):
        print("in function test3, a=%s, b=%s" % (a, b))
        return 0

#同时使用多个装饰器
@logging
@params_chack(int, str, (list, tuple))
def test3(a, b, c):
    print("in function test05, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


#构建不带参数的装饰器类
class Decorator:
    def __init__(self,func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("%s called" % self.func.__name__)
        result = self.func(*args, **kwargs)
        print("%s ended" % self.func.__name__)
        return result


#使用装饰器

@Decorator
def text4(a,b):
    print("in function test4, a=%s, b=%s" % (a, b))
    return 1

#构建带参数的装饰器类
class ParamCheck:
    def __init__(self,*types,**kwtypes):
        self.types = types
        self.kwtypes = kwtypes
        return

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
           result = [isinstance(params,type) for params,type in zip(args, self.types)]
           assert all(result), "ParamCheck: invalid parameters"
           result = [isinstance(kwargs[params],self.kwtypes[params]) for params in kwargs if params in self.kwtypes]
           assert all(result), "ParamCheck: invalid parameters"
           return func(*args, **kwargs)
        return inner

#使用装饰器
@ParamCheck(int,int)
def text5(a,b):
    print("in function test5, a=%s, b=%s" % (a, b))
    return 1

#装饰器实例：函数缓存
def funccache(func):
    cache = {}

    @functools.wraps(func)
    def inner(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return inner

# 使用装饰器
@funccache
def test08(a, b, c):
    return a + b + c


#python自带装饰器@property
class Person(object):

    def __init__(self):
        self._name = None
        return

    def get_name(self):
        print("get_name")
        return self._name

    def set_name(self, name):
        print("set_name")
        self._name = name
        return

    name = property(fget=get_name, fset=set_name, doc="person name(可以将类中的方法当作属性来使用")

#使用方法
#包装前：
person = Person()
person.set_name("xxx")  # 调用set_name方法设置姓名
print(person.get_name())  # 调用get_name方法获取姓名，输出: Alice


#包装后：
person = Person()
person.name = "Bob"  # 等价于调用set_name方法设置姓名，会打印 "set_name"
print(person.name)    # 等价于调用get_name方法获取姓名，会打印 "get_name"，输出: Bob


