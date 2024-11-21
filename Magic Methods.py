#定义一个可以自动比较大小的类
class people(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
        return self.name + ":" +str(self.age)


    def __lt__(self, other):
        return self.name<other.name if self.name != other.name else self.age < other.age

print("\t".join([str(item) for item in sorted([people("xxx",19),people("xxx",30),people("hhh",23),people("hhh",31)])]))


#实现任意深度的赋值
#例：a[0] = 'value1'; a[1][2] = 'value2'; a[3][4][5] = 'value3'
class Mydict(dict):
    def __setitem__(self, key, value):
        print("setitem:",key,value,self)
        super(Mydict,self).__setitem__(key, value)

    def __getitem__(self, item):
        print("get:",item,self)
        if item not in self:
            temp = Mydict()
            super(Mydict,self).__setitem__(item, temp)
            return temp
        return super(Mydict,self).__getitem__(item)

#使用实例
obj = Mydict()
obj[0] = "First"
obj[1][2] = "Secend"
obj[3][4][5] = "Third"
print("over")
