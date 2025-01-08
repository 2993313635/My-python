import re
from collections import Counter
import pymysql
import nltk
from nltk.corpus import stopwords

english_stopwords = stopwords.words('english')



def read_text_from_file(file_path):
    """
    从文件中读取文本内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text =f.read()
        return text
    except FileNotFoundError:
        print(f"文件{file_path}未找到")
        return None



def count_word_frequency(text):
    """
    统计单词出现频率，返回单词与出现次数的字典
    """
    word_count_dict = {}
    words = re.findall(r'\w+', text.lower())  #提取所有单词并小写
    filtered_words = [word for word in words if word not in english_stopwords]
    word_count_dict = Counter(filtered_words)
    return word_count_dict




def calculate_word_percentage(word_count_dict):
    """
    计算每个单词在全部中的占比(去除停用词后的）
    """
    word_percentage_dict = {}
    total_word_count = sum(word_count_dict.values())  #values()返回一个包含所有值的可迭代对象，再由sum方法对所有单词数量求和
    for word, count in word_count_dict.items():
        percentage = (count / total_word_count) *100 if total_word_count > 0 else 0
        word_percentage_dict[word] = percentage
    return word_percentage_dict


def connect_mysql():
    """
    连接MySQL数据库
    """
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='boshuo',
            database='word',
        )
        return conn
    except Exception as e:
        print(f"连接MySQL数据库失败：{e}")
        return None


def save_to_mysql(word_percentage_dict):
    """
    将单词占比数据保存到数据库，按照占比大小排序
    """
    conn = connect_mysql()
    if conn is None:
        return
    try:
        cursor = conn.cursor()

        #将字典转化为包含（单词，占比）元组的列表，并按照占比从大到小排序
        sorted_date = sorted(word_percentage_dict.items(), key=lambda x: x[1], reverse=True)
        data_to_insert = [(word,percentage) for word,percentage in sorted_date]

        insert_sql = "INSERT INTO word_percentage(word,percentage) VALUES (%s, %s)"
        cursor.executemany(insert_sql, data_to_insert)

        conn.commit()
        cursor.close()
        conn.close()

    except pymysql.MySQLError as e:
        print(f"保存失败：{e}")



def main():
    file_path = "../word statistics/content_file/all_content.txt"
    text = read_text_from_file(file_path)
    if text is None:
        return

    word_count_dict = count_word_frequency(text)
    word_percentage_dict = calculate_word_percentage(word_count_dict)

    save_to_mysql(word_percentage_dict)


if __name__ == '__main__':
    main()

