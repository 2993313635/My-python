import time
import datetime
import calendar

#time模块中三种时间形式
#时间戳
print("time stamp：",time.time())
# struct_time类型的本地时间
print("local time:",time.localtime())
# struct_time类型的UTC时间
print("utc time:",time.gmtime())

#将时间形式转化为字符串
time_stamp = time.time()
print(time.ctime(time_stamp))
#其他形式同理

#本地时间转字符串  自定义格式  其余形式也相同
local_time = time.localtime()
print(time.strftime("%Y-%m-%d, %H:%M:%S, %w", local_time))


#datetime中datetime类的用法
a_datetime_local = datetime.datetime.now()  #获取datetime.datetime类型的本地时间
print(a_datetime_local)

#datetime类型转字符串
print(a_datetime_local.strftime("%Y-%m-%d, %H:%M:%S, %w"))

# datetime类型转时间戳
time_stamp = a_datetime_local.timestamp()
print(time_stamp)