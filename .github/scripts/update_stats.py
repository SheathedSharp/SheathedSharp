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
    # 添加用户代理
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时时间
        driver.set_page_load_timeout(30)
        driver.get(url)
        
        # 增加等待时间
        time.sleep(15)

        stats = {}
        # 更新选择器以适应可能的页面结构变化
        selectors = {
            'views': "//div[contains(@class, 'user-profile-statistics-num')]",
            'posts': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '原创')]]",
            'followers': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '粉丝')]]"
        }

        for key, selector in selectors.items():
            try:
                # 增加等待时间和重试逻辑
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                # 添加JavaScript执行来确保元素可见
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(2)
                stats[key] = int(element.text.replace(',', ''))
            except Exception as e:
                print(f"Error retrieving {key}: {e}")
                stats[key] = 0

        return stats

    except Exception as e:
        print(f"Major error: {e}")
        return {'views': 0, 'posts': 0, 'followers': 0}
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