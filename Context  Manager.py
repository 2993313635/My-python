import contextlib

#打开文件操作
class Open:
    def __init__(self,file_name):
        self.file_name = file_name
        self.file_handler = None
        return

    def __enter__(self):
        print("enter",self.file_name)
        self.file_handler = open(self.file_name,'r')
        return self.file_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit",exc_type,exc_val,exc_tb)
        if self.file_handler:
            self.file_handler.close()
        return True


# 使用实例
with Open("python_base.py") as file_in:
    for line in file_in:
        print(line)
        raise ZeroDivisionError


#内置库contextlib的使用
@contextlib.contextmanager
def open_func(file_name):
    print("open file:",file_name,"in __enter__")
    file_handler = open(file_name,'r')

    yield file_handler

#exit方法
    print("close file:",file_name,"in__exit__")
    file_handler.close()

#使用实例
with open_func("test.txt") as file_in:
    for line in file_in:
        print(line)
        break


#内置库contextlib的使用（与类结合）
class Open():
    def __init__(self,file_name):
        self.file_name = file_name
        self.file_handler = open(file_name,"r")

    def close(self):
        print("close file Open")
        if self.file_handler:
            self.file_handler.close()

#使用实例
with contextlib.closing(Open("text.txt")) as file_in:
