import time

import re
import pandas as pd
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json


def init_driver(browser_driver, base_url: str):
    """
    初始化selenium浏览器驱动
    :param browser_driver:浏览器驱动
    :param base_url:目标url
    :return:返回requests库可用的cookie
    """
    browser_driver.get(base_url)
    with open('weibo_cookies.txt', 'r', encoding='utf8') as file:
        listCookies = json.loads(file.read())
    request_cookie = {}
    # 往browser里添加cookies
    for cookie in listCookies:
        request_cookie[cookie.get('name')] = cookie.get('value')
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        browser_driver.add_cookie(cookie_dict)
    sleep(1)
    browser_driver.refresh()  # 3秒后刷新网页,cookies才加载成功
    return request_cookie


if __name__ == "__main__":
    driver = webdriver.Chrome()
    url = 'https://service.account.weibo.com/index?type=5&status=4'
    # PPT上给的链接，该链接中微博时间跨度大，过早的微博没有原文信息，因此从3k数据开始可能少有点赞评论等数据
    domain_url = 'https://service.account.weibo.com'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"}

    common_cookie = init_driver(driver, url)
    with open('info_urls.txt', 'r') as f:
        target_urls = f.readlines()

    df = pd.DataFrame(columns=['content', 'time', 'forward', 'comment', 'like', 'VIP', 'link'])
    count = 0
    error_page = []

    for single_url in target_urls:

        print('共条' + str(len(target_urls)) + '微博，正在处理第' + str(count) + '条')
        count += 1

        # 每间隔100条微博保存一次
        if count == 100:
            print('正在写入csv...')
            df.to_csv('CSV/weibo_data.csv')
            print('csv写入完成！')
            df = pd.DataFrame(columns=['content', 'time', 'forward', 'comment', 'like', 'VIP', 'link'])
        elif count != 0 and count % 100 == 0:
            print('正在写入csv...')
            df.to_csv('CSV/weibo_data.csv', mode='a', header=False)
            print('csv写入完成！')
            df = pd.DataFrame(columns=['content', 'time', 'forward', 'comment', 'like', 'VIP', 'link'])

        driver.get(single_url.strip('\n'))
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        weibo_data = {'content': '', 'time': '', 'forward': 0, 'comment': 0, 'like': 0, 'VIP': 0, 'link': 0}

        # 如果没有原文信息，那么只能获得微博的基本信息
        # 首先判断是否胜诉，其次看网页中被告人微博的概述是否存在(有被屏蔽和已删除两种可能)，可以通过是否能够点击被告人的ID链接来判断
        if soup.find('div', class_='resault win') is not None and \
                soup.find('div', class_='feed bg_orange2 clearfix').find('a') is not None:
            # 是否存在查看原文按钮
            if soup.find('div', class_='feed bg_orange2 clearfix').find('div', class_='con').find('input') is None:
                weibo_data['content'] = soup.find('div', class_='feed bg_orange2 clearfix').find('div',
                                                                                                 class_='con').get_text(
                    strip=True)
            else:
                weibo_data['content'] = \
                    soup.find('div', class_='feed bg_orange2 clearfix').find('div', class_='con').find('input').get(
                        'value').strip()

            try:
                weibo_data['time'] = re.findall(r"(\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",
                                                soup.find('div', class_='item top').find('p').get_text(strip=True))[0]
            except IndexError as e:
                # 存在页面为全空的特殊情况
                print('未知错误')
                continue

            weibo_data['forward'] = -1
            weibo_data['comment'] = -1
            weibo_data['like'] = -1
            weibo_data['VIP'] = -1
            if re.findall(r'(https?://)', weibo_data['content']) is not None:
                weibo_data['link'] = 1

        # 找到胜诉且有原文的微博
        if soup.find('div', class_='resault win') is not None and soup.find('a', attrs={
            'suda-uatrack': 'key=tblog_service_account&value=original_text'}) is not None:
            driver.get(soup.find('a', attrs={
                'suda-uatrack': 'key=tblog_service_account&value=original_text'}).get('href'))

            time.sleep(0.5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                weibo_data['content'] = soup.find('div', attrs={'class': 'detail_wbtext_4CRf9'}).get_text(strip=True)
                weibo_data['time'] = soup.find('a', attrs={'class': 'head-info_time_6sFQg'}).get_text(strip=True)
            except AttributeError as e:
                print('第' + str(count - 1) + '条微博页面加载失败！存储简化微博数据')
                error_page.append(str(count - 1) + '\n')
                if weibo_data['content'] != '':
                    print(weibo_data)
                    df = df.append(pd.DataFrame(weibo_data, index=[0]), ignore_index=True)
                time.sleep(2)
                continue

            forward_and_comment = soup.find_all('span', attrs={'class': 'toolbar_num_JXZul'})
            # 存在关闭评论或转发标签的情况
            if len(forward_and_comment) >= 2:
                forward_data = forward_and_comment[0].get_text(strip=True)
                if forward_data != '转发':
                    if forward_data[-1].isdigit():
                        weibo_data['forward'] = int(forward_data)
                    elif forward_data[-1] == '万':
                        weibo_data['forward'] = float(forward_data[:-1]) * 10000

                comment_data = forward_and_comment[1].get_text(strip=True)
                if comment_data != '评论':
                    if comment_data[-1].isdigit():
                        weibo_data['comment'] = int(comment_data)
                    elif comment_data[-1] == '万':
                        weibo_data['comment'] = float(comment_data[:-1]) * 10000

            like_data = soup.find('span', attrs={'class': 'woo-like-count'}).get_text(strip=True)
            if like_data != '赞':
                if like_data[-1].isdigit():
                    weibo_data['like'] = int(like_data)
                elif like_data[-1] == '万':
                    weibo_data['like'] = float(like_data[:-1]) * 10000

            if soup.find('span', attrs={'class': 'woo-icon-wrap IconVip_icon_2tjdp'}) is not None:
                weibo_data['VIP'] = 1

            if soup.find('div', attrs={'class': 'detail_wbtext_4CRf9'}).find('a') is not None:
                weibo_data['link'] = 1

        if weibo_data['content'] != '':
            print(weibo_data)
            df = df.append(pd.DataFrame(weibo_data, index=[0]), ignore_index=True)

    with open('error_weibo_page.txt', 'w') as f:
        f.writelines(error_page)
    print('正在写入csv...')
    df.to_csv('CSV/weibo_data.csv', mode='a', header=False)
    print('csv写入完成！')
    driver.close()
    driver.quit()

# driver.close()
# driver.quit()
