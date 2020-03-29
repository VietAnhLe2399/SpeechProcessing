import requests
import urllib.request
import time
from bs4 import BeautifulSoup

urls = {}

def crawl(cat, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    article = soup.find(class_='fck_detail')
    if cat != 'goc_nhin':
        title = soup.find('h1', class_='title_news_detail mb10')
        description = soup.find(class_='description')
    else:
        title = soup.find('h1', class_='title_gn_detail')
    article_list = article.find_all('p', class_='Normal')
    with open('article/' + cat + '.txt', 'w', encoding='utf-8') as file:
        file.write(url)
        if cat != 'goc_nhin':
            file.write(title.text[:-1] + '.\n')
            file.write(description.text + '\n')
        else:
            file.write('\n' + title.text + '.\n')
        file.write('\n'.join([p.text for p in article_list[:-1]]))

with open('urls.txt', 'r') as urlFile:
    lines = urlFile.readlines()

for line in lines:
    cat, url = line.split(': ')
    urls[cat] = url[:-1]

for cat in urls:
    crawl(cat, urls[cat])