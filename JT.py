import os
from playwright.sync_api import sync_playwright
path = os.path.dirname(os.path.abspath(__file__).replace("\\", "/"))
def take_screenshot(url: str, file_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 无头模式
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=file_path)
        browser.close()

# 使用示例
take_screenshot(f'file:///{path}/template/output.html', '签到.png')
