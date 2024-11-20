import requests.adapters

r0 = requests.get("https://www.baidu.com/")    #获取数据
r1 = requests.post("https://www.baidu.com/")    #提交数据
r2 = requests.put("https://www.baidu.com/")     #更新数据(整体）
r4 = requests.delete("https://www.baidu.com/")   #删除数据
r5 = requests.head("https://www.baidu.com/")   #获取数据（只获取头部数据）
r6 = requests.options("https://www.baidu.com/")  #获取服务器配置信息
r7 = requests.patch("https://www.baidu.com/")    #部分更新服务器数据



#URL参数传递
params = {"key":"value","key1":"value2"}
response = requests.get("URL", params=params)


#获取网页内容
r = requests.get("URL", params=params)
print(r.text)           #返回正常内容（解码后）
print(r.content)        #返回byte类型的内容（解压，未解码）
print(r.json())         #网页为json，返回一个json队像
print(r.encoding)       #返回网页编码


#获取原始套接字响应
r = requests.get("https://www.baidu.com/",stream = True)
print(r.raw)  #访问原始响应信息
print(r.raw.read(10))   #丛原始响应对象中获取前十个字节并打印处理

#一般将文本流保存到文件用以下方式
with open("text","wb") as fd:   #打开（创建）铭文text文件的文件命名为fd（以二进制写入数据）
    for chunk in r.iter_content(chunk_size=256):        #按指定块大小（256）迭代返回数据
        fd.write(chunk)


#设置请求头
headers = {"usrr-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"}
r = requests.get("https://www.baidu.com/",headers = headers)
print(r.request.headers)   #获取request头部
print(r.headers)            #获得response头部


#post请求：表单
post_dict = {"key1":"value1","key2":"value2"}
r = requests.post("https://www.baidu.com/",data=post_dict)  #向网址发送post请求，向其传递data参数


#post多部分编码的文件   用于向服务器发送文件（图片，文档等）
files = {"file":open("text","rb")}
r = requests.post("https://www.baidu.com/",files=files)

#状态响应码
r = requests.post("https://www.baidu.com/")
print(r.status_code)                            #200
print(r.status_code == requests.codes.ok)      #True

#如果发生了一个错误请求，可以通过Response.raise_for_status() ;来抛出异常
bad_r = requests.get("https://www.baidu.com/")
print(bad_r.status_code)      #错误响应
bad_r.raise_for_status()      #抛出错误


#Cookies
#发送你的cookie到服务器
cookies = {"cookies":"working"}
r = requests.get("https://www.baidu.com/",cookies = cookies)

#会话对象：可以跨请求保持某些参数，会在同一个session实例中发出的所有请求之间保持cookie
s = requests.Session()
s.get("https://www.baidu.com/")
for cookie in s.cookies:
    print(cookie)


#超时，设置timeout参数
requests.get("https://www.baidu.com/",timeout = 0.001)
requests.get("https://www.baidu.com/",timeout = (3,27))     #分别用作connect和read二者的timeout


#代理设置
proxies = {"http": "http://10.10.1.10:3128",
          "https": "http://10.10.1.10:1080",}

requests.get("https://www.baidu.com/",proxies = proxies)