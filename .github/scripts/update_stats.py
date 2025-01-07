'''
Author: hiddenSharp429 z404878860@163.com
Date: 2024-11-09 13:13:34
LastEditors: Please set LastEditors
LastEditTime: 2025-01-07 10:51:21
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
    # 添加更多必要的 Chrome 参数
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # 打印当前页面信息以便调试
            print(f"Attempt {attempt + 1}: Accessing {url}")
            driver.get(url)
            
            # 等待页面加载完成
            time.sleep(20)  # 增加等待时间
            
            # 打印页面源代码，用于调试
            print("Page source length:", len(driver.page_source))
            
            stats = {}
            selectors = {
                'views': "//div[contains(@class, 'user-profile-statistics-num')]",
                'posts': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '原创')]]",
                'followers': "//div[contains(@class, 'user-profile-statistics-num')][following-sibling::div[contains(text(), '粉丝')]]"
            }

            for key, selector in selectors.items():
                try:
                    # 使用显式等待
                    wait = WebDriverWait(driver, 20)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    
                    # 尝试多种方法获取元素文本
                    text = element.text or element.get_attribute('textContent')
                    if not text:
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(2)
                        text = element.text or element.get_attribute('textContent')
                    
                    print(f"Found {key}: {text}")  # 调试信息
                    stats[key] = int(text.replace(',', ''))
                except Exception as e:
                    print(f"Error retrieving {key}: {e}")
                    continue

            # 如果成功获取到数据，直接返回
            if any(stats.values()):
                return stats
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # 在重试之前等待
                continue
        finally:
            if 'driver' in locals():
                driver.quit()
    
    return {'views': 0, 'posts': 0, 'followers': 0}

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