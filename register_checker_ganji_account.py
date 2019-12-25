# -*- coding: utf-8 -*-
# __author__ = "zok"  362416272@qq.com
# Date: 2019-10-6  Python: 3.7
# 赶集网注册判断
import time
import random
import asyncio
import pyppeteer


class RegisterGanji:
    """
    类异步
    """
    pyppeteer.DEBUG = True
    page = None

    async def _injection_js(self):
        """注入js
        """
        await self.page.evaluateOnNewDocument(
            '() =>{ Object.defineProperties(navigator, { webdriver:{ get: () => false } }) }')  # 本页刷新后值不变

    async def _init(self):
        """初始化浏览器
        """
        browser = await pyppeteer.launch({'headless': False,
                                          # 'userDataDir': './userdata',
                                          'args': [
                                              '--window-size={1300},{600}'
                                              '--disable-extensions',
                                              '--hide-scrollbars',
                                              '--disable-bundled-ppapi-flash',
                                              '--mute-audio',
                                              '--no-sandbox',
                                              '--disable-setuid-sandbox',
                                              '--disable-gpu',
                                              '--disable-infobars'
                                          ],
                                          'dumpio': True
                                          })
        self.page = await browser.newPage()
        # 设置浏览器头部
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        # 设置浏览器大小
        await self.page.setViewport({'width': 1200, 'height': 600})

    async def main(self, username):
        """
        注册
        """
        # 初始化浏览器
        await self._init()
        # 注入js
        await self._injection_js()
        # 注册页面
        await self.page.goto('https://passport.ganji.com/register.php')

        time.sleep(0.5)

        # 输入手机号码
        await self.page.type('.t_reg_username', username, {'delay': random.randint(100, 151) - 50})

        # 回车
        await self.page.keyboard.press('Enter')

        # 直到validatorPhone标签出现,
        await asyncio.sleep(0.5)

        # 获取span的validatorPhone的值
        tip_username = await self.page.querySelectorEval('#tip_username', 'node => node.textContent')
        print(tip_username)

        if tip_username == '用户名已存在，请更换':
            return True
        return False


if __name__ == '__main__':
    ls = [
        {"username": "sdsadas", "is_register": True},
        {"username": "ssdsasdfdee", "is_register": False},
    ]
    register = RegisterGanji()
    loop = asyncio.get_event_loop()

    for dic in ls:
        task = asyncio.ensure_future(register.main(dic['username']))
        loop.run_until_complete(task)
        res = task.result()
        print("username:%s is register: %s" % (dic['username'], res))
        assert res == dic['is_register'], [res, dic]
