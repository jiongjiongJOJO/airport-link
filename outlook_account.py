import asyncio
import json
import os
import random
import string

from pyppeteer import launch

# 扩展目录的路径
EXTENSION_PATH = 'CapSolver.Browser.Extension'

# 配置文件路径
CONFIG_PATH = os.path.join('', 'config.json')


def get_random_string(length=10, use_password_chars=False):
    chars = string.ascii_letters + string.digits
    if use_password_chars:
        chars += "!@#$%^&"
    return ''.join(random.choice(chars) for _ in range(length))


async def type_and_click_next(page, selector, text):
    await page.waitForSelector(selector)
    await page.type(selector, text)
    await page.keyboard.press('Enter')


async def create_outlook():
    if not os.path.exists(EXTENSION_PATH):
        print("扩展必须下载并放置在同一文件夹中。检查GitHub上的说明。")
        return

    with open(CONFIG_PATH, 'r') as f:
        config_json = json.load(f)

    if config_json.get('apiKey', '') == '':
        api_key = input("输入apiKey，如果没有则输入'no'：")
        config_json['apiKey'] = api_key
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_json, f)

    browser = await launch(headless=False, executablePath=config_json['executablePath'],
                           args=[f'--proxy-server={config_json["proxy"]}'])
    page = await browser.newPage()
    await page.goto('https://signup.live.com/signup')
    await page.waitForSelector('#nextButton')
    await page.click('#nextButton')
    await asyncio.sleep(1)
    await page.waitForSelector('#liveSwitch')
    await page.click('#liveSwitch')
    await asyncio.sleep(1)

    email_name = f'F{get_random_string()}'
    email = f"{email_name}@outlook.com"
    password = get_random_string(20, True)

    await type_and_click_next(page, "#usernameInput", email_name)
    await asyncio.sleep(1)
    await type_and_click_next(page, "#Password", password)
    await asyncio.sleep(1)
    await type_and_click_next(page, "#lastNameInput", get_random_string())
    await asyncio.sleep(1)
    await type_and_click_next(page, "#firstNameInput", get_random_string())
    await asyncio.sleep(1)

    await page.waitForSelector("#BirthMonth")
    await page.click("#BirthMonth")
    await page.keyboard.press('Enter')
    await page.keyboard.press('ArrowDown')

    await asyncio.sleep(0.5)

    await page.waitForSelector("#BirthDay")
    await page.click("#BirthDay")
    await page.keyboard.press('Enter')
    await page.keyboard.press('ArrowDown')

    await type_and_click_next(page, "#BirthYear", "2000")

    print(f"电子邮件: {email}")
    print(f"密码: {password}")

    with open("outlook_accounts.txt", "a") as file:
        file.write(f"{email}:{password}\n")

    okButton = "#id__0"
    await page.waitForSelector(okButton, timeout=6000000)
    await page.click(okButton)
    await asyncio.sleep(20)
    await page.close()
    await browser.close()


asyncio.run(create_outlook())
