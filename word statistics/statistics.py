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




def calculate_word_percentage(word_count_dict,total_word_count):
    """
    计算每个单词在全部中的占比(去除停用词后的）
    """
    word_percentage_dict = {}
    for word, count in word_count_dict.items():
        percentage = (count / total_word_count) * 100 if total_word_count > 0 else 0
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


def save_article_to_mysql(article_text):
    """
    将文章内容保存在article表中，返回文章id
    """
    conn = connect_mysql()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO articles(article_text) VALUES (%s)"
        cursor.execute(sql, article_text)
        article_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return article_id

    except pymysql.MySQLError as e:
        print(f"保存文章失败：{e}")


def save_word_to_mysql(word):
    """
    将单词保存到words表中，返回单词id
    """
    conn = connect_mysql()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        #查询是否已存在该单词
        check_sql = "SELECT word_id FROM words WHERE word = %s"
        cursor.execute(check_sql, (word,))
        result = cursor.fetchone()
        if result:
            return result[0]

        #如果result不存在，执行插入操作
        sql = "INSERT INTO words(word) VALUES (%s)"
        cursor.execute(sql,(word,))
        word_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return word_id
    except pymysql.MySQLError as e:
        print(f"保存单词到数据库失败：{e}")
        return None


def save_word_article_counts_to_mysql(article_id,word_count_dict,total_word_count):
    """
    将单词在当前文章中出现的次数和占比数据保存到word_article_counts表中
    """
    conn = connect_mysql()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        for word, count in word_count_dict.items():
            percentage = (count / total_word_count) * 100 if total_word_count > 0 else 0
            word_id = save_word_to_mysql(word)
            if word_id is None:
                continue
            sql = "INSERT INTO word_article_counts(article_id,word_id,count,percentage) VALUES (%s, %s,%s,%s)"
            cursor.execute(sql,(article_id,word_id,count,percentage))
        conn.commit()
        cursor.close()
        conn.close()
    except pymysql.MySQLError as e:
        print(f"保存单词在文章中的统计数据失败：{e}")


def save_word_total_counts_to_mysql(word_count_dict,total_all_words):
    """
    将单词在所有文章中出现的总次数和总站比保存到数据库
    """
    conn = connect_mysql()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        for word, count in word_count_dict.items():
            total_percentage = (count / total_all_words) * 100 if total_all_words > 0 else 0
            word_id = save_word_to_mysql(word)
            if word_id is None:
                continue
            sql = "INSERT INTO word_total_counts(word_id,total_count,total_percentage) VALUES (%s, %s, %s)"
            cursor.execute(sql, (word_id,count,total_percentage))
        conn.commit()
        cursor.close()
        conn.close()
    except pymysql.MySQLError as e:
        print(f"保存单词在所有文章中的数据到数据库失败：{e}")


def main():
    file_path = "../word statistics/content_file/all_content.txt"
    text = read_text_from_file(file_path)
    if text is None:
        return

    articles = text.split("\n\n")  #文章之间通过两个换行符相隔
    all_words_count = Counter()    #统计所有文章中的单词总数（去除停用词后的）
    total_all_words = 0  #所有文章的总单词数

    for article in articles:
        article_text = article.strip()
        if not article_text:
            continue
        article_id = save_article_to_mysql(article_text)
        if article_id is None:
            continue

        word_count_dict = count_word_frequency(article_text)
        all_words_count.update(word_count_dict)
        total_word_count = sum(word_count_dict.values())
        total_all_words += total_word_count

        save_word_article_counts_to_mysql(article_id,word_count_dict,total_word_count)
    save_word_total_counts_to_mysql(all_words_count,total_all_words)



if __name__ == '__main__':
    main()


