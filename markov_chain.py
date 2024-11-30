

import nltk
import random


with open('walden.txt',"r",encoding="utf-8") as file:
    walden = file.read()
    walden = walden.split()


def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr) - 1:        #这里是防止索引错误，如果不减一在i取最后一个值时，下面取i+1会导致索引错误
            temp = (arr[i], arr[i + 1])
            pairs.append(temp)         #将temp添加到pairs中，获得在列表中的一串数组
    return pairs


def generate(cfd, word='the', num=500):      #cfd代表文本的条件分布频率情况，word表示起始单词默认值为“the”，num为指定生成的单词数量默认值为500
    for i in range(num):                    #循环控制生成文本
        arr = []
        for j in cfd[word]:                 #循环单词word后续可能出现的词并存放在j中
            for k in range(cfd[word][j]):   #循环word后续单词是j的次数，并按次数添加到arr中
                arr.append(j)
        print(word, end=' ')

        word = arr[int((len(arr)) * random.random())]  #用文本长度乘以0~1之间的数获取索引来随机获取word

pairs = makePairs(walden)
cfd = nltk.ConditionalFreqDist(pairs)  #用于记录在pairs这个数组下以某个已知单词作为条件时，其他单词出现的频率
generate(cfd)