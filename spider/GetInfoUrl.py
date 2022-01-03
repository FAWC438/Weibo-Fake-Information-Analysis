import json
import time
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver


# class PageGroup(threading.Thread):
#     def __init__(self, thread_id, base, offset):
#         super(PageGroup, self).__init__()
#         self.thread_id = thread_id
#         self.base = base
#         self.offset = offset


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
    url = 'https://service.account.weibo.com/index?type=5&status=4'  # 这个链接里的微博都是时间跨度大的
    url_new = 'https://service.account.weibo.com/index?type=0&status=4'  # 这个链接里的微博都是时间跨度小的（最近的）
    domain_url = 'https://service.account.weibo.com'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"}

    common_cookie = init_driver(driver, url)

    # requests库无法获得数据，因为它无法爬取未经过渲染的网页，只能使用selenium获得渲染后的网页源码
    # r_html = requests.get(url, headers=headers, cookies=common_cookie).text

    target_urls = []
    for i in range(1, 501):
        print('Now solving page ' + str(i))
        driver.get(url + '&page=' + str(i))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        div_tags = soup.find_all('div', class_='m_table_tit')
        print(type(div_tags))
        for j in div_tags:
            link = j.find('a')
            if link is not None:
                target_urls.append(domain_url + link.get('href') + '\n')

        time.sleep(0.5)
    with open('info_urls.txt', 'w') as f:
        f.writelines(target_urls)
