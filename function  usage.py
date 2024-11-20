from operator import add
from functools import partial, reduce
def List():
#列表推导式
    a_list = [item*2 for item in range(5)]
    print(a_list)
    return a_list


def Dict():
#字典推导式
    a_dict = {"%d*2" %item: item**2 for item in range(5)}
    print(a_dict)


def Generator():
#生成器表达式
    a_generator = (item**2 for item in range(5))
    print(a_generator)
    print(next(a_generator))
    print(next(a_generator))

def Iter_list():
#iter函数
    a = List()
    list_generator = iter(a)
    print(next(list_generator))
    print(next(list_generator))
    print(next(list_generator))
    print(type(list),type(list_generator))

#匿名函数
def lambda_fun():
    a_fun =lambda x,y,z:x+y+z
    print(a_fun(1,2,3))


#map函数
def a_map():
    print(list(map(lambda x:x*2,range(5))))

#reduce函数
def a_reduce():
     print(reduce(lambda x,y:x+y,range(10)))

#filter函数
def a_filter():
    print(filter(None, range(-4, 5)))
    print(list(filter(None, range(-4, 5))))
    print(list(filter(lambda x: x > 0, range(-4, 5))))

def a_enumerate():
#enumerate函数
    for index,item in enumerate(range(10)):
        print(f"结果为{index}.{item}")


#zip函数
def a_zip():
    for a,b in zip(list(range(1,5)),["a","b","c","d"]):
        print(a,b)


#partial函数
def a_partial():
    print(int("10010", base=2))
    int_base_2 = partial(int, base=2)
    print(int_base_2("10010"))

#operator.add函数
def a_operator():
    print(reduce(add,range(10)))




