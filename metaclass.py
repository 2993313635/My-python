class Foo(object):

    def hello(self):
        print("hello world!")
        return

foo = Foo()
print(type(foo))            # <class '__main__.Foo'>
print(type(foo.hello))      # <class 'method'>
print(type(Foo))            # <class 'type'>



def init(self, name):
    self.name = name
    return


def hello(self):
    print("hello %s" % self.name)
    return

Foo = type("Foo", (object,), {"__init__": init, "hello": hello, "cls_var": 10})
foo = Foo("xxx")
print(foo.hello())
print(Foo.cls_var)
