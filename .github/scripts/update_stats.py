'''
Author: hiddenSharp429 z404878860@163.com
Date: 2024-11-09 13:13:34
LastEditors: hiddenSharp429 z404878860@163.com
LastEditTime: 2024-11-11 11:50:23
'''
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_csdn_stats(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)

        stats = {}
        selectors = {
            'views': "//span[contains(@class, 'user-profile-statistics-views')]//div[contains(@class, 'user-profile-statistics-num')]",
            'posts': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '原创')]]",
            'followers': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '粉丝')]]"
        }

        for key, selector in selectors.items():
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                stats[key] = int(element.text.replace(',', ''))
            except Exception:
                stats[key] = 0

        return stats

    finally:
        if 'driver' in locals():
            driver.quit()

def update_readme(stats):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 定义替换模式和对应的完整URL格式
    replacements = {
        'views': (
            r'badge/My%20Blog%20Views-\d+-blue\?style=social',
            f'badge/My%20Blog%20Views-{stats["views"]}-blue?style=social'
        ),
        'posts': (
            r'badge/Posts-\d+-green\?style=social',
            f'badge/Posts-{stats["posts"]}-green?style=social'
        ),
        'followers': (
            r'badge/Followers-\d+-orange\?style=social',
            f'badge/Followers-{stats["followers"]}-orange?style=social'
        )
    }
    
    # 执行替换
    for key, (pattern, replacement) in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    url = 'https://blog.csdn.net/Zchengjisihan'
    stats = get_csdn_stats(url)
    print(f"访问量: {stats['views']}")
    print(f"文章数: {stats['posts']}")
    print(f"粉丝数: {stats['followers']}")
    update_readme(stats)