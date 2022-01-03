from selenium import webdriver
from time import sleep
import json

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://service.account.weibo.com/index?type=5&status=4&page=1')
    sleep(6)
    # 模拟点击手机扫码登录
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/div/a[2]').click()
    # 在30秒的时间内扫码登录，等待程序提示后cookie就保存到本地了
    sleep(30)
    dictCookies = driver.get_cookies()  # 获取cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
    with open('weibo_cookies.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')
    driver.close()
    driver.quit()
