import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# 该代码用于获取普通微博数据

if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'https://m.weibo.cn/'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"}
    df = pd.DataFrame(columns=['content'])
    count = 0

    driver.get(url)
    while count < 200:
        time.sleep(2)
        count += 1
        print('正在爬取第' + str(count) + '页微博')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for single_weibo in soup.find_all('div', class_='weibo-text'):
            df = df.append(pd.DataFrame({'content': single_weibo.get_text(strip=True)}, index=[0]), ignore_index=True)
        driver.refresh()

    df.to_csv('CSV/weibo_data_contrast.csv')
    print('写入csv完成！')
    driver.close()
    driver.quit()
