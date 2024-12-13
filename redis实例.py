
import sys
import time

import redis

# 全局变量
conn_pool = redis.ConnectionPool(host="localhost", port=6379, db=1)  #创建一个本地连接池，使用编号1数据库


conn_inst = redis.Redis(connection_pool=conn_pool)  #创建一个redis实例化对象用于后续操作
channel_name = "fm-1"        #定义一个频道名

def public_test():
    """
    消息发布函数
    """
    while True:
        # 发布消息
        conn_inst.publish(channel_name, "hello " + str(time.time()))  #每隔十秒向频道发布一次消息，内容为”hello加当前时间戳的字符串形式
        if int(time.time()) % 10 == 1:             #当前时间戳（秒数）除以是10的余数为1（相当于每过十秒）发布一个over信息
            conn_inst.publish(channel_name, "over")
        time.sleep(1)   #程序暂停一秒


def subscribe_test(_type=0):
    """
    消息订阅函数
    """
    pub = conn_inst.pubsub()    #创建一个订阅对象
    pub.subscribe(channel_name)   #让该对象订阅fm-1频道

    if _type == 0:
        # 订阅消息
        for item in pub.listen():
            print("Listen on channel: %s" % item)
            if item["type"] == "message" and item["data"].decode() == "over":  
                print(item["channel"].decode(), "已停止发布")
                break
    else:
        # 另一种订阅模式
        while True:
            item = pub.parse_response()
            print("Listen on channel: %s" % item)
            if item[0].decode() == "message" and item[2].decode() == "over":
                print(item[1].decode(), "已停止发布")
                break

    # 取消订阅
    pub.unsubscribe()
    return


if __name__ == '__main__':
    if sys.argv[1] == "public":
        public_test()
    else:
        subscribe_test(int(sys.argv[1]))