import requests
from bs4 import BeautifulSoup
import os
import random
import time

def fetch(url):
    """
    发送请求获取网页内容

    """
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    try:
        random_wait_time = random.randint(1, 5)
        time.sleep(random_wait_time)
        response = requests.get(url, headers=headers)
        response.raise_for_status()  #如果状态码不是200，抛出异常
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"请求{url}失败，错误信息：{e}")
        return None


def parse_html(html_content):
    """
    解析HTML内容，提取文本
    """

    if html_content is None:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.find_all("p")
    for text_1 in text:
        for i in text_1.find_all("a"):
            i.decompose()
    texts = [p.get_text() for p in text]
    return texts


def get_max_chapter(book_id,start_chapter):
    """
    获取指定书籍的最大章节数，通过判断页面是否显示”小说已完结“来判断边界
    """
    chapter_id = start_chapter
    while True:
        url = f"https://www.dictool.com/novel/chapter_{book_id}_1_{chapter_id}.html"
        page_text = fetch(url)
        if page_text is None:
            return 0
        soup = BeautifulSoup(page_text, "html.parser")
        if "小说已完结" in soup.text:
            break
        chapter_id += 1
    return chapter_id - start_chapter


def main():
    global_current_chapter = 1 #全局章节计数器，记录当前章节编号
    output_folder = "content_file"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_content_file = os.path.join(output_folder, "all_content.txt")
    with open(all_content_file, "w", encoding="utf-8") as f:
        for i in range(1,432):
            max_chapter = get_max_chapter(i,global_current_chapter)
            if max_chapter is not None and max_chapter > 0:
                for chapter_id in range(global_current_chapter,global_current_chapter+max_chapter):
                    url = f"https://www.dictool.com/novel/chapter_{i}_1_{chapter_id}.html"
                    page_text = fetch(url)
                    p_texts = parse_html(page_text)
                    f.write("\n".join(p_texts))
                global_current_chapter = max_chapter + global_current_chapter


if __name__ == "__main__":
    main()





